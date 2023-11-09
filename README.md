MIDI Humanizer README

Overview

This Python script, named "MIDI Humanizer", is designed to humanize MIDI files, adding a more natural and less mechanical feel to them. 
The script applies slight variations in note velocity and timing, ensuring that the modifications are within MIDI's standard data range. 
Additionally, it provides functionality to convert SID (Commodore 64 sound file) songs to MIDI format and then apply the humanization process.

Features

    Humanize MIDI Files: Adds natural feel by slightly varying the velocity and timing of notes in a MIDI file.
    SID to MIDI Conversion: Converts SID files to MIDI format.
    Metadata Extraction: Extracts metadata such as name, author, and release year from SID files.
    MIDI Validation: Ensures all MIDI messages are within valid MIDI data ranges.
    Logging: Logs original and modified MIDI message attributes for tracking changes.

Requirements

    Python 3.x
    mido Python library for working with MIDI files.
    subprocess module for executing external commands (for SID to MIDI conversion).
    random module for generating random variations.

Installation

Ensure you have Python 3.x installed, then install the required mido library using pip:

bash

pip install mido

Usage

    Humanize Existing MIDI File:

    bash

python script.py <path-to-midi-file> <output-path>

Convert and Humanize SID File:

bash

    python script.py <path-to-sid-file> <output-directory>

    This will convert each song in the SID file to a MIDI file and apply humanization.

Functions

    humanize_velocity: Adjusts the velocity of MIDI notes to vary their intensity.
    apply_timing_variation: Slightly alters the timing of MIDI messages.
    sanitize_message: Ensures all MIDI message attributes are within the valid MIDI data range.
    log_message: Logs attributes of MIDI messages.
    is_message_valid: Checks if a MIDI message has valid values.
    validate_midi_file: Validates all messages in a MIDI file.
    humanize_midi: Main function to apply humanization to a MIDI file.
    extract_metadata: Extracts metadata from a SID file.
    extract_info: Helper function to extract specific information from a text.
    convert_and_humanize: Converts SID songs to MIDI and applies humanization.

Disclaimer

This script is provided as-is without any warranty. The user is responsible for ensuring compatibility with their MIDI and SID files.
Author

This script was created by Ulf Bertilsson.
