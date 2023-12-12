#!/bin/bash
# A bash script that takes a string of a 7z file online and outputs a download link
# Usage: ./script.sh kit-sdk@file_name_as_found_in_kit-sdk.packman.xml_including_final.7z

# The base URL of the cloudfront server
base_url="https://d4i3qtqj3r0z5.cloudfront.net/"

# The file name to be encoded
file_name="$1"

# Use sed to encode the file name
encoded_file_name="$(echo "$file_name" | sed -e 's/[\/&]/\\&/g' -e 's/@/%40/g' -e 's/\./%2E/g' -e 's/+/%2B/g')"

# Append the encoded file name to the base URL
download_link="${base_url}${encoded_file_name}"

# Print the download link
echo "$download_link"
