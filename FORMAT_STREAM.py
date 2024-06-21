import pandas as pd
import gui.gui_browse as gui_browse

output_dir = 'OUTPUT'

file_path = gui_browse.main(params_title='Browse files', 
         params_initbrowser='INPUT',
         params_extensions='.csv',               # E.g. '.csv'
         size=(40,20),
         verbose=False)

# Step 1: Read the file line by line to identify rows with inconsistent column count
expected_columns = None
bad_lines = []
correct_lines = []

with open(file_path, 'r') as file:
    for i, line in enumerate(file):
        columns = line.strip().split(',')
        if expected_columns is None:
            expected_columns = len(columns)
        if len(columns) != expected_columns:
            bad_lines.append((i + 1, line))
        else:
            correct_lines.append(columns)

# Log bad lines
print("Bad lines:")
for line_num, content in bad_lines:
    print(f"Line {line_num}: {content}")

# Step 2: Create a DataFrame from the correct lines
df = pd.DataFrame(correct_lines)

# Step 3: Process the DataFrame
num_columns = df.shape[1]
split_point = num_columns // 2

# Define the headers
headers = ['CC16', 'CC17', 'CC18', 'CC19', 'CC20', 'CC21', 'CC22', 'CC23', 'CC24']

# Split the DataFrame into two halves
df_left = df.iloc[:, :split_point]
df_right = df.iloc[:, split_point:]

print(df_left)
exit()
# Add headers to each part
df_left.columns = headers[:split_point]
df_right.columns = headers[:df_right.shape[1]]


# Save to new files
df_left.to_csv(output_dir+'/Left_file.csv', index=False)
df_right.to_csv(output_dir+'/Right_file.csv', index=False)

print("Files have been successfully split and saved with headers.")
