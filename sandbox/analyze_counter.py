import mido
import gui.gui_browse as gui_browse

def analyze_midi_cc_beats(file_path):
    # Load the MIDI file
    midi = mido.MidiFile(file_path)
    print("Ticks per Beat:", midi.ticks_per_beat)

    # Initialize a dictionary to store total ticks for each CC number
    cc_ticks = {}

    # Analyze each track
    for track in midi.tracks:
        # Maintain a running total of ticks since the last event
        running_ticks = 0
        for msg in track:
            # Update running total with delta time
            running_ticks += msg.time
            if msg.type == 'control_change':
                # If this CC number hasn't been encountered yet, initialize it
                if msg.control not in cc_ticks:
                    cc_ticks[msg.control] = 0
                # Add running ticks to the CC number and reset
                cc_ticks[msg.control] += running_ticks
                running_ticks = 0  # Reset running ticks after counting for a CC

    print("cc_ticks")
    print(cc_ticks)
    exit()
    sum_of_beats = 0
    # Calculate total beats for each CC and print
    for cc, ticks in cc_ticks.items():
        total_beats = ticks / midi.ticks_per_beat
        print(f"Total Beats for CC{cc}: {total_beats}")
        sum_of_beats = sum_of_beats + total_beats
   
    print("sum_of_beats", sum_of_beats)
    # return total_beats, cc_ticks, midi.ticks_per_beat

def main(midi_file_path=''):
    if midi_file_path == '':
        print("need to browse")
        midi_file_path = gui_browse.main(params_title='Browse files [→TAB]',
                                    params_initbrowser='INPUT/',
                                    params_extensions='.mid',               # E.g. '.csv'
                                    size=(40,20),
                                    verbose=False)
    else:
        print("the path is provided:")

    print(midi_file_path)
    analysis_count = analyze_midi_cc_beats(midi_file_path)
    print(analysis_count) 
    return analysis_count

if __name__ == "__main__":
    # Path to your MIDI file
    # midi_file_path = 'INPUT/exp9f-A.mid'
    midi_file_path = 'INPUT/exp9f-E.mid'
    main(midi_file_path=midi_file_path)
    # main(midi_file_path='')