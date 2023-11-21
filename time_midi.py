""" The point of this script is to calculate rtaes and timings...
"""

import time_signature as time_signature
import time_string as time_string

def main(max_datapoint,
         max_bars ='',
         time_length_str='',
         time_bpm = 120,
         time_signature_str='4/4',
         floating_points=0,
         verbose=False):
    
    # Initialize lists to store MIDI message attributes
    if time_length_str == '':   # meaning, that no argument has been passed
        print("HERE A GUI SHOULD ALLOW FOR ENTERING THE LENGTH ACCORDING TO A GIVEN FORMAT")
    else:                   # meaning that an explicit length was passed as an argument
        time_length, time_components = time_string.main(time_length_str)
        # print("time_components:", time_components)


    datapoints_per_second = max_datapoint/time_length
    dps_rounded = int(round(datapoints_per_second, floating_points))

    signature_tuple = time_signature.main(time_signature_str)   # (7, 4)

    if verbose:
        print("If there are around", max_bars, "bars in total.")
        print("and each bar has", signature_tuple[0], "beats (", signature_tuple[0]*max_bars, "in total )")
        print("then thre are about", max_datapoint/(signature_tuple[0]*max_bars), "datapoints per beat")
        print("and about", datapoints_per_second, "datapoints per second.")
        print("which, round up to", dps_rounded)

    return dps_rounded


if __name__ == "__main__":
    max_datapoint = 454831
    main(max_datapoint,
         time_length_str = '39:32.032', 
         max_bars = 1186,
         time_bpm = 120,
         time_signature_str='4/4',
         verbose=True)