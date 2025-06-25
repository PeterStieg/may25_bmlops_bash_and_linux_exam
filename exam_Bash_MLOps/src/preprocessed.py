"""
-------------------------------------------------------------------------------
This script `preprocessed.py` retrieves data from the latest CSV file created
in the 'data/raw/' directory.

1. It applies preprocessing to the data.

2. The results of the preprocessing are saved in a new CSV file
   in the 'data/processed/' directory, with a name formatted as
   'sales_processed_YYYYMMDD_HHMM.csv'.

3. All preprocessing steps are logged in the
   'logs/preprocessed.logs' file to ensure detailed tracking of the process.

Any errors or anomalies are also logged to ensure traceability.
-------------------------------------------------------------------------------
"""

import os
import pandas as pd

sales_data_path = "../data/raw/"
sales_data_all_files = os.listdir(sales_data_path)  # Get all files in the directory
sales_data_csv_files = [
    x for x in sales_data_all_files if x.endswith(".csv")
]  # Filter for CSV files


# Loop through each CSV file, read it into a DataFrame, and append it to the list

dataframes = []

for f in sales_data_csv_files:  # f as in "file"

    f_path = os.path.join(sales_data_path, f)

    df = pd.read_csv(f_path)

    df["timestamp"] = pd.to_datetime(
        df["timestamp"], format="ISO8601", utc=True, errors="coerce"
    )
    df.sort_values(by="timestamp", ascending=False, inplace=True)

    dataframes.append(df)

# Concatenate all DataFrames
df = pd.concat(dataframes, ignore_index=True)

# Remove duplicates based on subset of columns
df.drop_duplicates(subset=["timestamp", "model", "sales"], inplace=True)

# Create folder for processed data if it doesn't exist
processed_sales_data_path = "../data/processed/"
os.makedirs(processed_sales_data_path, exist_ok=True)

# Save cleaned data to a new CSV file
timestamp_basic = pd.Timestamp.utcnow().strftime("%Y%m%d_%H%M")
f_name = "sales_processed_" + timestamp_basic + ".csv"
f_path = os.path.join(processed_sales_data_path, f_name)
df.to_csv(f_path, index=False)

# Log the preprocessing steps
log_file_path = "../logs/preprocessed.logs"
log_file_header = "timestamp;nr_of_files;nr_of_rows;processed_files\n"

# Check if the log file exist, if not create it and write header
# Check if the log file is empty, if so, write the header
if (not os.path.exists(log_file_path)) or (os.path.getsize(log_file_path) == 0):
    with open(log_file_path, "w") as log_file:
        log_file.write(log_file_header)

with open(log_file_path, "a") as log_file:
    log_file.write(
        f"{timestamp_basic};{len(sales_data_csv_files)};{df.shape[0]};{','.join(sales_data_csv_files)}\n"
    )
