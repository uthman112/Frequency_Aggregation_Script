import os
import sys
import glob
import pandas as pd

all_csv_files=[]

def copy_last_row(file_path):
    df= pd.read_csv(file_path)
    last_row= df.iloc[[-1]]
    last_row.to_csv('Compiled_average.csv', mode='a', header=False)

# --- Expand wildcards if passed literally (for Windows CMD) ---
def expand_args(args):
    expanded = []
    for arg in args:
        if "*" in arg or "?" in arg:
            expanded.extend(glob.glob(arg))
        else:
            expanded.append(arg)
    return expanded


#-- Main --
if __name__ == "__main__":
    if len(sys.argv) > 1:
        csv_files = expand_args(sys.argv[1:])
    else:
        folder = os.path.join(os.getcwd(), "data")
        csv_files = glob.glob(os.path.join(folder, "*.csv"))

    if not csv_files:
        print(" No CSV files found. Pass them as args or put them in a 'data' folder.")
        sys.exit(1)

    if os.path.exists("Compiled_average.csv"):
        os.remove("Compiled_average.csv")

    for csv_file in csv_files:
        print(f"Processing {csv_file}...")
        copy_last_row(csv_file)
        print(f" {csv_file} completed!")
        all_csv_files.append(csv_file)
    num_of_csv_files= len(all_csv_files)
    print(f"There are {num_of_csv_files} CSV files in the folder")

