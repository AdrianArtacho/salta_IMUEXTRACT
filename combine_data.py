""" The objective of this script is to:
    1. gather the csv files
    2. Combine them
    3. fill in the blanks
"""

import os
import pandas as pd

# Define a custom function to conditionally cast values to integers
def cast_to_int(value):
    if isinstance(value, float):
        return int(value)
    return value

def main(folder_path = 'stream_data/',
         output_path='OUTPUT/',
         verbose=False):

    # Initialize an empty DataFrame to store the combined data
    # combined_df = pd.DataFrame()
    # print("combined_df:", combined_df.head())
    # exit()

    # Create an empty DataFrame with the 'Timestamp' column
    # empty_df = pd.DataFrame(columns=['Timestamp'])
    combined_df = pd.DataFrame()

    # Print the empty DataFrame
    print(combined_df)
    # exit()

    # Iterate through the CSV files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            
               
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # Extract the first part of the file name ('CC16' before the underscore)
            column_name = filename.split('_')[0]
            print("column_name:", column_name)

            # Rename the 'Control_Value' column
            df.rename(columns={'Control_Value': column_name}, inplace=True)

            # Convert the column to integer data type
            # df[column_name] = df[column_name].astype(int)
        
            # Set 'Timestamp' as the index for merging
            df.set_index('Timestamp', inplace=True)
        
            # Merge the data based on the index (Timestamp), filling missing values with the previous values
            combined_df = combined_df.join(df, how='outer', rsuffix='_' + filename[:-4])

            # Apply the custom function to the column
            combined_df = combined_df.apply(cast_to_int)
            print(combined_df.head())

    

    # Forward-fill missing values within each column
    combined_df.fillna(method='ffill', inplace=True)

    print(combined_df.head())

    

    # Reset the index to make 'Timestamp' a regular column
    combined_df.reset_index(inplace=True)

    if verbose:
        # Print the resulting combined DataFrame
        print(combined_df.head())

    combined_df.to_csv(output_path+'CC-combined.csv')


if __name__ == "__main__":
    main(folder_path = 'stream_data/',
         output_path='OUTPUT/',
         verbose=True)
