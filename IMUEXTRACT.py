import mido
import pandas as pd
import time_string as time_string
import time_signature as time_signature
import time_midi as time_midi
import time_stamps as time_stamps
import pyt.df.resampling as resampling

def main(midi_file = 'Anna-RAW.mid',
         input_path='INPUT/',
         output_path='OUTPUT/',
         streams_path='INTER/',
         time_length_str = '',
         time_signature_str = '',
         verbose=False):

    if midi_file == '':
        print("We need to browse")
        exit()
    else:
        midi_file = midi_file

    # Specify the path to your MIDI file
    midi_file_path = input_path+midi_file
    if verbose:
        print("midi_file_path:", midi_file_path)

    max_datapoint = 454831      # ???
    dps_rounded = time_midi.main(max_datapoint,
                                time_length_str = time_length_str, #'39:32.032', 
                                max_bars = 1186,
                                time_bpm = 120)
    
    if verbose:
        print("dps_rounded:", dps_rounded, "(It should be about 192)")
    
    # exit()
    # Initialize a dictionary to store CC data for different streams
    cc_data = {}

    # Open the MIDI file for reading
    mid = mido.MidiFile(midi_file_path)

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
    
    # Create separate DataFrames for each CC stream
    for control_number, data in cc_data.items():
        cc_df = pd.DataFrame(data)

        # Group by 'Timestamp' and keep the last entry of each group
        cc_df = cc_df.groupby('Timestamp').last().reset_index()

        csv_filename = f'{streams_path}CC{control_number}_data.csv'
        cc_df.to_csv(csv_filename, index=False)
        list_of_streams.append(csv_filename)
        print(f'Saved CC{control_number} data as {csv_filename}')


    if verbose:
        print(list_of_streams)  # csv files
    # exit()

    print("Resampling files...")

    # Initialize an empty DataFrame for the result; it will be populated in the loop
    combined_df = None

    
    print(list_of_streams)
    list_of_resampled_streams = []
    for stream in list_of_streams:
        resampled_stream = resampling.main(file_name = stream,
                        total_duration_seconds = 2*60 + 16,
                        file_path='',
                        rel_path='',
                        fps = 30,
                        include_timestamp=False,
                        verbose=False)
        list_of_resampled_streams.append(resampled_stream)
        if verbose:
            print(type(resampled_stream))
            print(resampled_stream.head())

    if verbose:
        print(len(list_of_resampled_streams))
 

        
    # Combine DataFrames
    # Ensure the index of each DataFrame; if not, set it before this step
    combined_df = pd.concat(list_of_resampled_streams, axis=1)

    # Optional: if you want 'Timestamp' back as a column instead of the index
    # combined_df.reset_index(inplace=True)

    # Save the combined DataFrame to a CSV file
    csv_file_path = output_path + 'CC-combined.csv'  # Specify your desired file path and name
    combined_df.to_csv(csv_file_path, index=False)

    print(f"Combined DataFrame saved to {csv_file_path}")
    
    # print(combined_df.head())

    
    


if __name__ == '__main__':
    main(midi_file = 'Anna-RAW.mid',
         time_length_str = '39:32.032',
         time_signature_str = '4/4',
         verbose=False)
    