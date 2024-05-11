import json
import time_string

def write_json_file(file_path, data):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main(output_folder='OUTPUT',
         subfolder='',
         midi_file_path='',
         reference_file = '',
         number_of_tracks = '',
         ticks_per_beat = '',
         total_beats = '',
         total_ticks = '',
         cc_messages = '',
         track_all_messages = '',
         length_manually_entered = '',
         entered_total_sec = '',
         total_seconds = '',
         minutes = '',
         seconds = '',
         resampling_rate = '',
         row_count = '',
         verbose=False):
    
    # entered_total_sec, (entered_min, entered_sec, entered_ms) = time_string.main(length_manually_entered)
    
    # if verbose:
        # print(entered_total_sec, entered_min, entered_sec, entered_ms)
    # exit()
    
    data = {
        "subset": subfolder,
        "midi_file_path": midi_file_path,
        "reference_file": reference_file,
        "number_of_tracks": number_of_tracks,
        "ticks_per_beat": ticks_per_beat,
        "total_beats": total_beats,
        "total_ticks": total_ticks, 
        "cc_messages":cc_messages,
        "track_all_messages": track_all_messages,
        "time": [
            {"length_manually_entered": length_manually_entered, "(entered_seconds)": entered_total_sec},
            {"length_estimated": str(minutes)+':'+str(seconds), "(estimated seconds)": total_seconds}
        ],
        "resampling":[
            {"new_rate": resampling_rate,
            "highest_row": row_count},
            {"(original_rate)": total_ticks/entered_total_sec,
            "(highest_timecode)": total_ticks}
        ]
    }

    file_path = output_folder+"/"+subfolder+"/"+subfolder+"_metadata.json"
    write_json_file(file_path, data)
    print(f"JSON file has been created at: {file_path}")

if __name__ == "__main__":
    main()
