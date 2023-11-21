import pandas as pd
import matplotlib.pyplot as plt


def main(csv_file_path):
### PLOT
    # Read the CSV file into the existing 'combined_df' DataFrame
    combined_df = pd.read_csv(csv_file_path)

    # Get a list of column names representing different 'Control_Value' streams
    control_columns = [col for col in combined_df.columns if col.startswith('Control_Value')]

    # Create a plot
    plt.figure(figsize=(12, 6))  # Adjust the figure size as needed

    # Plot each 'Control_Value' stream
    for control_column in control_columns:
        plt.plot(combined_df.index, combined_df[control_column], label=control_column)

    # Add labels and a legend
    plt.xlabel('Timestamp')
    plt.ylabel('Control Value')
    plt.legend()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    csv_file_path = 'OUTPUT/CC-combined.csv'
    main(csv_file_path)