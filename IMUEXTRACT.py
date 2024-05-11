import mido
import pandas as pd
import time_string as time_string
import time_signature as time_signature
import time_midi as time_midi
import time_stamps as time_stamps
import pyt.df.resampling as resampling
import gui.gui_browse as gui_browse
import pyt.paths.empty_folder as empty_folder
import pyt.paths.create_folder as create_folder
import os
import combine_plot
import time_length
import analyze_midi as analyze_midi
import gui.gui_enterstring as gui_enterstring
import meta_json

def main(midi_file = '',
         input_path='INPUT/',
         output_path='OUTPUT/',
         streams_path='INTER/',
         aggr_ref_midi_file = '',
         time_length_str = '',
         beats_per_bar = '',
         default_bpm = 120,
         resampling_rate = 30,
         verbose=False):

    if midi_file == '':
        # print("We need to browse")
        midi_file_path = gui_browse.main(params_title='Browse files [→TAB]',
                                    params_initbrowser='INPUT/',
                                    params_extensions=('.mid', '.midi'),               # E.g. '.csv'
                                    size=(40,20),
                                    verbose=False)
        # exit()
    else:
        # midi_file = midi_file
        midi_file_path = input_path+midi_file

    # Specify the path to your MIDI file
    
    if verbose:
        print("midi_file_path:", midi_file_path)

    # exit()
    ### EMPTY INTER/ FOLDER
    empty_folder.main('INTER/', verbose=True)
    
    ### NEW FOLDER NAME
    filename_without_extension = os.path.splitext(os.path.basename(midi_file_path))[0]
    if verbose:
        print("filename_without_extension:", filename_without_extension)

    ### CREATE NEW FOLDER
    create_folder.main(filename_without_extension, local_folder = 'OUTPUT')
    

    

    ### ASKING TO CONFIRM THE LENGTH!!!
    # time_str, time_str_list = time_length(time_str=time_length_str)
    # print(time_str)

    if aggr_ref_midi_file == '':
        analyze_file_path = ''
        # print(midi_file_path,"=",input_path,"+",aggr_ref_midi_file)
    else:
        analyze_file_path = input_path+aggr_ref_midi_file

    if verbose:
        print("analyze_file_path", analyze_file_path)
    # exit()

    print("CHOOSE 'all' AGGREGATED MIDI FILE CORRESPONDING TO", filename_without_extension)
    number_of_tracks, ticks_per_beat, total_beats, total_ticks, cc_messages, track_all_messages, total_seconds, minutes, seconds, reference_file = analyze_midi.main(midi_file_path=analyze_file_path,
                                                                                                                                                     default_bpm = default_bpm, 
                                                                                                                                                     params_title="→'all' FILE FOR "+filename_without_extension, 
                                                                                                                                                     verbose=False)   #midi_file_path=midi_file_path
    print(number_of_tracks, ticks_per_beat, total_beats, total_ticks, cc_messages, track_all_messages)

    if time_length_str == '':
        print("time_length_str was none") 
        length_manually_entered = gui_enterstring.main("Enter the length of the capture (E.g.: '12:34.567')", "mm:ss.ms", "Capture Langth", 
            font = ("Arial", 16), default_text= str(minutes)+':'+str(seconds), 
            verbose=False)
    else:
        print("time_length_str was", time_length_str)
        length_manually_entered = time_length_str
    
    print("Manually entered length:",length_manually_entered)
    # exit()

    entered_total_sec, (entered_min, entered_sec, entered_ms) = time_string.main(length_manually_entered)

    total_bars = round(total_beats) / beats_per_bar
    print("total_bars", total_bars, "(",round(total_beats),"/",beats_per_bar,")")

    # exit()
    max_datapoint = total_ticks # 454831      # ????????
    dps_rounded = time_midi.main(max_datapoint,
                                time_length_str = length_manually_entered, #'39:32.032', 
                                max_bars = total_bars,
                                time_bpm = default_bpm)
    
    if verbose:
        print("dps_rounded:", dps_rounded, "(It should be about 192)")
    
    # exit()
    # exit()
    # Initialize a dictionary to store CC data for different streams
    cc_data = {}

    # Open the MIDI file for reading
    mid = mido.MidiFile(midi_file_path)
    if verbose:
        print("just checking...", midi_file_path)

    # exit()
    # Iterate through the MIDI file and extract relevant CC information
    for track in mid.tracks:
        # if verbose:
        #     print("track:", track)
        time_elapsed = 0  # Initialize time elapsed in ticks
        
        for msg in track:
            time_elapsed += msg.time
            if msg.type == 'control_change':
                control_number = msg.control
                
                # Create a new list for the CC stream if it doesn't exist in the dictionary
                if control_number not in cc_data:
                    cc_data[control_number] = {
                        'Timestamp': [],
                        'Control_Value': []
                    }
                
                # if control_number == 18:
                #     print("control_number:", control_number,"time_elapsed:", time_elapsed)

                # Append data to the respective CC stream
                cc_data[control_number]['Timestamp'].append(time_elapsed)
                cc_data[control_number]['Control_Value'].append(msg.value)

                # if verbose:
                #     print(cc_data[control_number])

    
    list_of_streams = []
    
    # exit()
    # Create separate DataFrames for each CC stream
    for control_number, data in cc_data.items():
        cc_df = pd.DataFrame(data)

        # Group by 'Timestamp' and keep the last entry of each group
        cc_df = cc_df.groupby('Timestamp').last().reset_index()

        csv_filename = f'{streams_path}CC{control_number}_data.csv'
        cc_df.to_csv(csv_filename, index=False)
        list_of_streams.append(csv_filename)
        print(f'Saved CC{control_number} data as {csv_filename}')

    # exit()
    if verbose:
        print(list_of_streams)  # csv files
    # exit()

    print("Resampling files...")
    # exit()

    # Initialize an empty DataFrame for the result; it will be populated in the loop
    combined_df = None

    
    print(list_of_streams)
    # exit()
    list_of_resampled_streams = []
    # exit()
    for stream in list_of_streams:
        resampled_stream = resampling.main(file_name = stream,
                        total_duration_seconds = entered_total_sec,
                        file_path='',
                        rel_path='',
                        fps = resampling_rate,   # 30
                        include_timestamp=False,
                        verbose=False)
        list_of_resampled_streams.append(resampled_stream)
        if verbose:
            print(type(resampled_stream))
            print(resampled_stream.head())

    # exit()
    if verbose:
        print(len(list_of_resampled_streams))
 

        
    # Combine DataFrames
    # Ensure the index of each DataFrame; if not, set it before this step
    combined_df = pd.concat(list_of_resampled_streams, axis=1)

    # Optional: if you want 'Timestamp' back as a column instead of the index
    # combined_df.reset_index(inplace=True)

    # Save the combined DataFrame to a CSV file
    composite_filename = filename_without_extension+'_'+'CC-combined.csv'
    csv_file_path = output_path+filename_without_extension+'/'+composite_filename  # Specify your desired file path and name
    combined_df.to_csv(csv_file_path, index=False)

    print(f"Combined DataFrame saved to {csv_file_path}")

    # Assuming combined_df is your DataFrame
    row_count = combined_df.shape[0]
    print("Number of rows in combined_df:", row_count)
    
    # print(combined_df.head())

    # exit()
    # combine_plot.main(csv_file_path,OUTPUT/Elda-RAW/CC-combined.csv
    combine_plot.main(composite_filename,
                      output_path='OUTPUT/'+filename_without_extension+'/',
                      string_prefix=filename_without_extension+'_',
                      verbose=True)
    
    # print("...now the JSON")
    meta_json.main(subfolder=filename_without_extension,
                   output_folder='OUTPUT',
                   midi_file_path=midi_file_path,
                   reference_file = reference_file,
                   number_of_tracks = number_of_tracks, 
                   ticks_per_beat = ticks_per_beat, 
                   total_beats = total_beats,
                   total_ticks = total_ticks, 
                   cc_messages = cc_messages, 
                   track_all_messages = track_all_messages, 
                   length_manually_entered = length_manually_entered,
                   entered_total_sec = entered_total_sec,
                   total_seconds = total_seconds, 
                   minutes = minutes, 
                   seconds = seconds,
                   resampling_rate = resampling_rate,
                   row_count = row_count)

    # main('CC-combined.csv',
    #      output_path='OUTPUT/',
    #      verbose=True)


if __name__ == '__main__':
    main(midi_file = '',                        # browsing
        #  midi_file = 'exp9f-E.mid',           # REMOVE VALUE 
         aggr_ref_midi_file = '',
        #  aggr_ref_midi_file = 'exp9f-all.mid',  # REMOVE VALUE
         time_length_str = '',
        #  time_length_str = '02:09.000',         # REMOVE VALUE
         beats_per_bar = 4,
         resampling_rate = 30,      # Just to make it fit the framerate from video, MPIPE...
         verbose=True)
    