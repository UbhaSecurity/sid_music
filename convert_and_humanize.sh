#!/bin/bash

# Check if an argument was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path-to-sid-file>"
    exit 1
fi

input_sid_path="$1"
base_name=$(basename -- "$input_sid_path")
file_name="${base_name%.*}"

# Get metadata from sidtool
metadata=$(sidtool --info "$input_sid_path")
name=$(echo "$metadata" | grep -oP 'Name: \K.*')
author=$(echo "$metadata" | grep -oP 'Author: \K.*')
released=$(echo "$metadata" | grep -oP 'Released: \K.*')
num_songs=$(echo "$metadata" | grep -oP 'Songs: \K\d+')

if [ -z "$num_songs" ]; then
    echo "Could not determine the number of songs in the SID file."
    exit 1
fi

for ((song=1; song<=num_songs; song++)); do
    temp_midi_path="/tmp/${file_name}_song${song}.mid"
    output_midi_path="${file_name}_song${song}_Humanized.mid"

    sidtool --out "$temp_midi_path" --format midi --song $song "$input_sid_path" -f 20000
    if [ $? -eq 0 ]; then
        python3 humanize_velocity.py "$temp_midi_path" "$output_midi_path" 0.2 0.01 "$name" "$author" "$released"
        rm "$temp_midi_path"
        echo "Conversion and humanization of song $song complete. Output saved to $output_midi_path"
    else
        echo "sidtool conversion failed for song $song."
    fi
done
