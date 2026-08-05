import os
import glob
import sys
import csv
import pandas as pd

# --- Thresholds (full list, unchanged) ---
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

#---Clean CSV file to read just 461 columns--#
def clean_csv(file_path, expected_columns=461):
    cleaned_lines = []
    with open(file_path, 'r') as f:
        for line in f:
            fields = line.rstrip("\n").split(",")
            while fields and fields[-1] == "":
                fields.pop()
            if len(fields)> expected_columns:
                fields = fields[:expected_columns]
            cleaned_lines.append(",".join(fields))
    with open(file_path, 'w', newline="") as f:
        f.write("\n".join(cleaned_lines)+"\n")


def sort_csv_columns(file_path):
    df = pd.read_csv(file_path, header=None, dtype=str) 
    df= df.dropna(axis=1, how='all')
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


# --- Expand wildcards if passed literally (for Windows CMD) ---
def expand_args(args):
    expanded = []
    for arg in args:
        if "*" in arg or "?" in arg:
            expanded.extend(glob.glob(arg))
        else:
            expanded.append(arg)
    return expanded


# --- Main ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        csv_files = expand_args(sys.argv[1:])
    else:
        folder = os.path.join(os.getcwd(), "data")
        csv_files = glob.glob(os.path.join(folder, "*.csv"))

    if not csv_files:
        print(" No CSV files found. Pass them as args or put them in a 'data' folder.")
        sys.exit(1)

    for csv_file in csv_files:
        print(f"Processing {csv_file}...")
        clean_csv(csv_file, expected_columns=461)
        sort_csv_columns(csv_file)
        mark_cells_above_thresholds(csv_file, thresholds)
        print(f" {csv_file} completed!")
