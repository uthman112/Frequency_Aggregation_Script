import csv
import sys
import pandas as pd

def sort_csv_columns(file_path):
    df = pd.read_csv(file_path, header=None, dtype=str) 
  
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

  
    if df.iloc[-1].str.contains('Utilization Percentage').all():
        print(f"Utilization Percentage values already exist for all columns. Skipping... for {file_path}")
        return

 
    transposed_data = list(map(list, zip(*data)))  
    sorted_data = [sorted(column, key=lambda x: float(x) if x.isdigit() else x) for column in transposed_data]
    sorted_data = list(map(list, zip(*sorted_data)))


    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sorted_data)

def mark_cells_above_thresholds(file_path, thresholds):

    df = pd.read_csv(file_path, header=None, dtype=str)  
    if len(thresholds) != len(df.columns):
        print(f"Number of thresholds must match the number of columns:{file_path}")
        return
        
    for col, threshold in zip(df.columns, thresholds):
        df[col] = df[col].apply(lambda x: f'{x}*' if pd.to_numeric(x, errors='coerce') >= threshold else x)
    percentages = df.apply(lambda col: col.astype(str).str.endswith('*').mean() * 100)
    df.to_csv(file_path, index=False, header=False)  
    
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if not df.iloc[-1].str.contains('Utilization Percentage').any():
            writer.writerow([f"Utilization Percentage: {value}%" for value in percentages])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_to_process.csv>")
        sys.exit(1)

    thresholds = [
    -71, -75, -75, -101, -101, -101, -101, -101, -101, -81.2, -81.2, -81.2,
    -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2,
    -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2,
    -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2,
    -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2,
    -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2, -81.2,
    -81.2, -81.2, -81.2, -81.2, -81.2, -81.2,
    -102, -102, -102, -102, -102, -102, -102, -102, -102, -102, -102, -102,
    -102, -102, -102, -102, -102, -102, -102, -102, -102, -102, -102, -102,
    -102, -102, -102, -102, -102, -102, -102, -102, -102, -102, -102, -102,
    -102, -102, -102, -102, -102, -102, -102, -102, -102, -102, -102, -102,
    -102, -102, -102, -102, -102, -102, -102, -102, -102, -102, -102, -102,
    -102, -102, -102, -102, -102, -102, -102, -102, -102, -102, -102, -102,
    -102, -102, -102, -102, -102, -102, -102, -102,
    -118, -118, -118, -118, -118, -118, -118, -118, -118, -118, -118, -118,
    -118, -118, -118, -118, -118, -118, -118, -118, -118,
    -96, -96, -96,-96,-96,
    -96, -96, -96, -96, -96, -96, -96, -96, -96, -96, -96, -96, -96, -96,
    -96, -96, -96, -96, -96, -96, -96, -96, -96, -96, -96, -96, -96, -96,
    -96, -96, -96, -96, -96, -96, -96, -96, -96, -96, -96, -96, -96, -96,
    -96, -96, -96, -96, -96, -96, -96, -96, -96, -96, -96, -96, -96, -96,
    -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94,
    -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94,
    -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94,
    -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94,
    -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94,
    -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94,
    -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94,
    -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94,
    -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94,
    -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94,
    -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94,
    -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94,
    -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94,
    -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94,
    -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94,
    -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94, -94,
    -94, -94, -94, -94, -94, -94, -94
    ]
    for csv_file in sys.argv[1:]:
        print(f"Processing {csv_file}...")
        sort_csv_columns(csv_file)
        mark_cells_above_thresholds(csv_file, thresholds)
        print(f"{csv_file} processing completed. Successful!")
