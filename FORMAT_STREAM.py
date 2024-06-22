import pandas as pd
import gui.gui_browse as gui_browse
import math
import pyt.paths.create_folder as create_folder

def main(output_dir = 'OUTPUT',
         output_subdir = 'CtrlStream',
         verbose=False):
    # output_dir = 'OUTPUT'

    file_path = gui_browse.main(params_title='Browse files', 
            params_initbrowser='INPUT',
            params_extensions='.csv',               # E.g. '.csv'
            size=(40,20),
            verbose=False)

    if verbose:
        print(file_path)
    # exit()

    # Step 1: Read the file line by line to identify rows with inconsistent column count
    expected_columns = None
    bad_lines = []
    correct_lines = []

    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            if verbose:
                print("i:", i, "line:", line)
            columns = line.strip().split(',')
            if verbose:
                print("columns:", columns)
            if expected_columns is None:
                expected_columns = len(columns)
                if verbose:
                    print("expected_columns:", expected_columns)
                # exit()
            if len(columns) != expected_columns:
                bad_lines.append((i + 1, line))
            else:
                correct_lines.append(columns)

    # exit()
    # Log bad lines
    if verbose:
        print("Bad lines:")
        for line_num, content in bad_lines:
            print(f"Line {line_num}: {content}")

    # Step 2: Create a DataFrame from the correct lines
    df = pd.DataFrame(correct_lines)

    if verbose:
        print(df.head())
    # exit()
    # Step 3: Process the DataFrame
    num_columns = float(df.shape[1])
    split_point = float(num_columns) / 2.
    split_point_rounded_up = math.ceil(split_point)

    if verbose:
        print("num_columns:", num_columns, "split_point:", split_point, "split_point_rounded_up:", split_point_rounded_up)
    # exit()
    # Define the headers
    headers = ['CC16', 'CC17', 'CC18', 'CC19', 'CC20', 'CC21', 'CC22', 'CC23', 'CC24']

    # Split the DataFrame into two halves
    df_left = df.iloc[:, :split_point_rounded_up]
    df_right = df.iloc[:, split_point_rounded_up:]

    if verbose:
        print(df_left.head())
        print(df_right.head())
    # exit()
    # Add headers to each part
    df_left.columns = headers[:split_point_rounded_up]
    df_right.columns = headers[:df_right.shape[1]]

    if verbose:
        print(df_left.head())
        print(df_right.head())
    # exit()

    # Create folder if non-existent
    create_folder.main(output_subdir, local_folder = output_dir, verbose=False)
    # exit()

    # Save to new files
    save_out_path = output_dir+"/"+output_subdir+"/"
    df_left.to_csv(save_out_path+'Left_file.csv', index=False)
    df_right.to_csv(save_out_path+'Right_file.csv', index=False)

    print("Files have been successfully split and saved with headers in", save_out_path)

if __name__ == "__main__":
    main()