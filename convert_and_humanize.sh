#!/bin/bash

# Check if an argument was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path-to-sid-file>"
    exit 1
fi

# Get the input SID file path from the first argument
input_sid_path="$1"
# Extract the filename without the extension to use for output
base_name=$(basename -- "$input_sid_path")
file_name="${base_name%.*}"

# Use sidtool to convert the SID file to a temporary MIDI file
temp_midi_path="/tmp/${file_name}.mid"

# Convert .sid to .mid using sidtool
sidtool --out "$temp_midi_path" --format midi "$input_sid_path"

# Check if sidtool was successful
if [ $? -eq 0 ]; then
    # If sidtool succeeded, run the humanize_velocity.py script
    output_midi_path="${file_name}_Humanized.mid"
    python3 humanize_velocity.py "$temp_midi_path" "$output_midi_path"
    
    # Remove the temporary MIDI file
    rm "$temp_midi_path"
    
    echo "Conversion and humanization complete. Output saved to $output_midi_path"
else
    echo "sidtool conversion failed."
    exit 1
fi
