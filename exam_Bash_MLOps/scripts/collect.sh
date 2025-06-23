#!/bin/bash
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

get_sales () {
	local category="$1"  # Get the first parameter
	local url="http://localhost:5000/$category"
	local response=$(curl -s $url)
	echo $response
	#output_file="data/raw/sales_${timestamp}.csv"
}

log() {
	timestamp=$(date +"%Y%m%d_%H%M")
	echo $timestamp 
}

for gc in "${categories[@]}"; do
    get_sales "$gc"
done

log
