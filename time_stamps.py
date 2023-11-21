""" This script takes timestamps (int) and a rate (timestamps per second)
    and yields time in seconds
"""

def main(timestamp,
         rate=192):

    time_in_seconds = timestamp / rate

    return time_in_seconds

if __name__ == "__main__":
    main()