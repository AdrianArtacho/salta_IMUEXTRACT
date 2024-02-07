import mido
import pandas as pd
import time_string as time_string
import time_signature as time_signature
import time_midi as time_midi
import time_stamps as time_stamps

def main(midi_file = 'Anna-RAW.mid',
         input_path='INPUT/',
         output_path='OUTPUT/',
         streams_path='stream_data/',
         time_length_str = '',
         time_signature_str = '',
         verbose=False):
    
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

    # exit()
    # Create separate DataFrames for each CC stream
    for control_number, data in cc_data.items():
        cc_df = pd.DataFrame(data)

        # Group by 'Timestamp' and keep the last entry of each group
        cc_df = cc_df.groupby('Timestamp').last().reset_index()

        csv_filename = f'{streams_path}CC{control_number}_data.csv'
        cc_df.to_csv(csv_filename, index=False)

        print(f'Saved CC{control_number} data as {streams_path+csv_filename}')

    # print("cc_data:")
    # print(cc_data.items())
        
    # Iterate through the MIDI file and print its contents
    # for i, track in enumerate(mid.tracks):
    #     print(f"Track {i}:")
    #     for msg in track:
    #         print(msg)


    # # Iterate through the MIDI file and extract relevant CC information
    # for track in mid.tracks:
    #     time_elapsed = 0  # Initialize time elapsed in ticks
        
    #     for msg in track:
    #         time_elapsed += msg.time
    #         if msg.type == 'control_change':
    #             timestamps.append(time_elapsed)
    #             control_numbers.append(msg.control)
    #             control_values.append(msg.value)

    # # Create a DataFrame from the extracted CC data
    # data = {
    #     'Timestamp': timestamps,
    #     'Control_Number': control_numbers,
    #     'Control_Value': control_values
    # }

    # df = pd.DataFrame(data)

    # if verbose:
    #     # Print the DataFrame
    #     print(df)

    # df = pd.DataFrame(data)
    # df.to_csv(output_path+'blah.csv', index=False)

    


if __name__ == '__main__':
    main(midi_file = 'Anna-RAW.mid',
         time_length_str = '39:32.032',
         time_signature_str = '4/4',
         verbose=True)
    