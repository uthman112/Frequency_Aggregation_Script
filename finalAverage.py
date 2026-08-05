import pandas as pd
import sys
import re

def extract_percentage(value):
    # Use regex to extract numeric part from the percentage string
    match = re.search(r'\d+(\.\d+)?', value)
    if match:
        return float(match.group())
    return None

def calculate_column_averages(file_path):
    df = pd.read_csv(file_path)

    # Check if the file has already been processed (contains "AVERAGE" row)
    if "AVERAGE" in df.iloc[-1].values:
        print(f"The file {file_path} has already been processed. Skipping...")
        return
        
    numeric_df = df.map(extract_percentage)

    column_averages = numeric_df.mean().to_frame().transpose()
    column_averages = column_averages.rename(index={0: "AVERAGE"})

    df_with_average = df._append(column_averages, ignore_index=True)
    df_with_average.to_csv(file_path, index=False)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_to_process.csv>")
        sys.exit(1)

    for csv_file in sys.argv[1:]:
        print(f"Processing {csv_file}...")
    
        calculate_column_averages(csv_file)        
        print(f"{csv_file} processing completed. Successful!")
   
