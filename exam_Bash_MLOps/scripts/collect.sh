##!/bin/bash
# ==============================================================================
# Script: collect.sh
# Description:
#   This script queries an API to retrieve sales data for the following graphics card models:
#     - rtx3060
#     - rtx3070
#     - rtx3080
#     - rtx3090
#     - rx6700
#
#   The collected data is appended to a copy of the file:
#     data/raw/sales_data.csv
#
#   The output file is saved in the format:
#     data/raw/sales_YYYYMMDD_HHMM.csv
#   with the following columns:
#     timestamp, model, sales
#
#   Collection activity (requests, queried models, results, errors)
#   is recorded in a log file:
#     logs/collect.logs
#
#   The log should be human-readable and must include:
#     - The date and time of each request
#     - The queried models
#     - The retrieved sales data
#     - Any possible errors
# ==============================================================================

categories=("rtx3060" "rtx3070" "rtx3080" "rtx3090" "rx6700")

log_request () {
	local timestamp="$1"  # Get the first parameter: timestamp
	local category="$2"  # Get the second parameter: product category
	local response="$3"  # Get the third parameter: API response
	local request="$4" # Get the fourth parameter: cURL request

	local log_file="../logs/collect.logs"
	local log_header="timestamp,category,response,request"

	# If file doesn't exist or is empty, write header
    if [[ ! -s "$log_file" ]]; then
        echo "$log_header" > "$log_file"
    fi

	# Create log entry
	local log_entry="$timestamp,$category,$response,$request"

	# Append log entry to the log file
	echo "$log_entry" >> "$log_file"
}

get_and_save_sales () {
	local category="$1"  # Get the first parameter: product category
	local output_file_path="$2"  # Get the second parameter: output file path
	local timestamp_i=$(timestamps "ISO 8601")

	local url="http://localhost:5000/$category"
	local response=$(curl -s "$url")
	log_request "$timestamp_i" "$category" "$response" "$url"

	# Save sales data to the output file
	local new_row="$timestamp_i,$category,$response"
	echo "$new_row" >> "$output_file_path"
}

timestamps() {
	local format="$1"
	if [[ "$format" = "ISO 8601" ]]
	then
	timestamp_ISO_8601=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
	echo $timestamp_ISO_8601
	else
	timestamp_basic=$(date -u +"%Y%m%d_%H%M")
	echo $timestamp_basic
	fi
}


input_file_path="../data/raw/sales_data.csv"

# Create output file path with basic timestamp
timestamp_b=$(timestamps)
output_file_path="../data/raw/sales_${timestamp_b}.csv"

# Copy input file to output file
cp "$input_file_path" "$output_file_path"

# Add a newline if the file doesn't end with one
if [[ $(tail -c1 "$output_file_path" | wc -l) -eq 0 ]]; then
    echo >> "$output_file_path"
fi

for gc in "${categories[@]}"; do # gc as in "graphics card"
    get_and_save_sales "$gc" "$output_file_path"
done
