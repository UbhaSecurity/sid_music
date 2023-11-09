import sys
from mido import MidiFile

def is_message_valid(msg):
    """Check if a MIDI message is valid."""
    valid_range = range(0, 128)
    attributes = ['note', 'velocity', 'value', 'control', 'program', 'channel', 'data1', 'data2']
    for attr in attributes:
        if hasattr(msg, attr):
            value = getattr(msg, attr)
            if isinstance(value, int) and value not in valid_range:
                return False
    return True

def validate_midi_file(file_path):
    """Validate all messages in a MIDI file."""
    try:
        # Open the MIDI file with debug enabled
        mid = MidiFile(file_path, debug=True)
    except Exception as e:
        print(f"Error opening MIDI file {file_path}: {e}")
        return False

    for i, track in enumerate(mid.tracks):
        for j, msg in enumerate(track):
            if not is_message_valid(msg):
                print(f"Invalid message found in track {i+1}, position {j}: {msg}")
                return False
    return True

def main(file_path):
    """Main function to validate a MIDI file."""
    if validate_midi_file(file_path):
        print(f"MIDI file {file_path} is valid.")
    else:
        print(f"MIDI file {file_path} contains invalid data.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_midi.py <path-to-midi-file>")
        sys.exit(1)

    midi_file_path = sys.argv[1]
    main(midi_file_path)
