"""  The purpose of this script is to parse a
    time expressed as Minutes: Seconds. Milliseconds
    to obtain the time length in seconds
    """


def main(time_str,
         verbose=False):
   

    # Split the time string into minutes, seconds, and milliseconds
    minutes_str, rest_str = time_str.split(':')
    seconds_str, milliseconds_str = rest_str.split('.')

    # Convert the parts to integers
    minutes = int(minutes_str)
    seconds = int(seconds_str)
    milliseconds = int(milliseconds_str)

    # Calculate the total time in seconds
    total_seconds = minutes * 60 + seconds + milliseconds / 1000.0

    if verbose:
        print(f'Total time in seconds: {total_seconds}, ({minutes} minutes, {seconds} seconds and {milliseconds} ms)')
    
    return total_seconds, (minutes, seconds, milliseconds)

if __name__ == '__main__':
    main('39:32.032',
         verbose=True)