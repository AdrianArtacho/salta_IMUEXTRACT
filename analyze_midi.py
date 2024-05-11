import mido
import gui.gui_browse as gui_browse

def analyze_midi_file(file_path, verbose=False):
    if verbose:
        print("now anal_ DEF")
    
    # Load the MIDI file
    midi = mido.MidiFile(file_path)
    
    # Extract and print general information
    number_of_tracks = len(midi.tracks)
    print("Number of Tracks:", number_of_tracks)

    ticks_per_beat = midi.ticks_per_beat
    print("Ticks per Beat:", ticks_per_beat)
    
    # Initialize counters
    total_ticks = 0
    cc_messages = 0
    last_tick = 0

    # Analyze each track
    for i, track in enumerate(midi.tracks):
        current_ticks = 0
        track_cc_messages = 0
        track_all_messages = 0

        # Accumulate ticks and count CC messages
        for msg in track:
            current_ticks += msg.time
            track_all_messages += 1
            if msg.type == 'control_change':
                track_cc_messages += 1

        # Update the last tick position
        if current_ticks > last_tick:
            last_tick = current_ticks

        print("Last tick:", last_tick)
        # Update CC messages count
        cc_messages += track_cc_messages

        print(f"Track {i+1} - {track.name}: {current_ticks} ticks, {track_cc_messages} CC messages")

    # Calculate total duration in beats and total ticks
    total_beats = last_tick / midi.ticks_per_beat
    total_ticks = last_tick  # This is the position of the last event across all tracks

    # Print overall information
    print("Total Beats in the MIDI File:", total_beats)
    print("Total Ticks in the MIDI File:", total_ticks)
    print("Total CC Messages:", cc_messages)
    print("Track ALL messages", track_all_messages)

    return number_of_tracks, ticks_per_beat, total_beats, total_ticks, cc_messages, track_all_messages

def calculate_midi_length(file_path, bpm=120):
    # Load the MIDI file
    midi = mido.MidiFile(file_path)
    
    # Calculate the duration in seconds
    total_ticks = sum(msg.time for track in midi.tracks for msg in track)
    seconds_per_beat = 60 / bpm
    total_beats = total_ticks / midi.ticks_per_beat
    total_seconds = total_beats * seconds_per_beat
    
    # Convert to minutes and seconds for better readability
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    
    print(f"Total Length: {minutes} minutes and {seconds:.2f} seconds","(estimated for ",str(bpm),"bpm)")

    return total_seconds, minutes, seconds




def main(midi_file_path='', 
         aggr_ref_midi_file = '',
         params_title="SELECT 'all' MIDI FILE", 
         default_bpm = 120, verbose=False):
    if verbose:
        print("now analyze MAIN")

    if midi_file_path == '':
        if verbose:
            print("need to browse")
        
        midi_file_path = gui_browse.main(params_title=params_title,
                                    params_initbrowser='INPUT/',
                                    params_extensions=('.mid', '.midi'),               # E.g. '.csv'
                                    size=(40,20),
                                    verbose=False)
    else:
        if verbose:
            print("the path is provided:")

    print(midi_file_path)

    # Path to your MIDI file
    total_seconds, minutes, seconds = calculate_midi_length(midi_file_path, bpm=default_bpm)


    number_of_tracks, ticks_per_beat, total_beats, total_ticks, cc_messages, track_all_messages = analyze_midi_file(file_path=midi_file_path)
    # print(number_of_tracks, ticks_per_beat, total_beats, total_ticks, cc_messages, track_all_messages)
    return number_of_tracks, ticks_per_beat, total_beats, total_ticks, cc_messages, track_all_messages, total_seconds, minutes, seconds, midi_file_path

if __name__ == "__main__":
    # midi_file_path = 'INPUT/exp9f-E.mid'
    # main(midi_file_path=midi_file_path)
    main(verbose=False)