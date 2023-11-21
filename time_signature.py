""" The purpose of this script is to parse the time signature (entered as a string)"""

def main(time_signature_str,
         verbose=False):
    
    # Split the time signature string by '/'
    numerator_str, denominator_str = time_signature_str.split('/')

    # Convert the parts to integers
    numerator = int(numerator_str)
    denominator = int(denominator_str)

    if verbose:
        print(f'Numerator: {numerator}')
        print(f'Denominator: {denominator}')
        
    return (numerator, denominator)

if __name__ == "__main__":
    time_signature_str = '7/4'
    main(time_signature_str,
         verbose=True) 