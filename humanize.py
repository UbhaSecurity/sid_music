import os
import subprocess
import sys
import random
from mido import MidiFile, MidiTrack, Message, MetaMessage

def humanize_velocity(velocity, strength=0.2):
    """Humanize velocity to add a natural feel without exceeding MIDI limits."""
    variation_range = int(127 * strength)
    variation = random.randint(-variation_range, variation_range)
    new_velocity = max(0, min(127, velocity + variation))
    return new_velocity

def apply_timing_variation(msg, strength=0.01):
    """Apply slight timing variations."""
    if msg.time > 0:
        variation = int(msg.time * strength)
        msg.time += random.randint(-variation, variation)
    return msg

def sanitize_message(msg):
    """Ensure all message attributes are within MIDI data range."""
    attributes = ['note', 'velocity', 'value', 'control', 'program', 'channel', 'data1', 'data2']
    for attr in attributes:
        if hasattr(msg, attr):
            value = getattr(msg, attr)
            if isinstance(value, int):
                sanitized_value = max(0, min(127, value))
                setattr(msg, attr, sanitized_value)
    return msg

def log_message(msg, prefix="Message"):
    """Log all attributes of a MIDI message."""
    attrs = ['type', 'channel', 'note', 'velocity', 'time', 'control', 'value', 'program', 'data1', 'data2']
    attr_values = {attr: getattr(msg, attr, None) for attr in attrs}
    print(f"{prefix}: {attr_values}")

def is_message_valid(msg):
    """Check if a MIDI message is valid."""
    valid_range = range(0, 128)
    attributes = ['note', 'velocity', 'value', 'control', 'program', 'channel', 'data1', 'data2']
    for attr in attributes:
        if hasattr(msg, attr):
            value = getattr(msg, attr)
            if value not in valid_range:
                return False
    return True

def validate_midi_file(mid):
    """Validate all messages in a MIDI file before saving."""
    for i, track in enumerate(mid.tracks):
        for j, msg in enumerate(track):
            if not is_message_valid(msg):
                print(f"Invalid message found in track {i+1}, position {j}: {msg}")
                return False
    return True

def humanize_midi(input_path, output_path, velocity_strength, timing_strength, name, author, released):
    """Apply humanization to a MIDI file."""
    try:
        mid = MidiFile(input_path)
        print(f"Processing MIDI file: {input_path}")
    except OSError as e:
        print(f"Error opening MIDI file: {e}")
        return

    new_mid = MidiFile(ticks_per_beat=mid.ticks_per_beat)

    for i, track in enumerate(mid.tracks):
        new_track = MidiTrack()
        print(f"Processing Track {i + 1}/{len(mid.tracks)}")
        for msg in track:
            try:
                log_message(msg, "Original")
                if msg.type == 'note_on':
                    msg.velocity = humanize_velocity(msg.velocity, velocity_strength)
                msg = apply_timing_variation(msg, timing_strength)
                msg = sanitize_message(msg)
                log_message(msg, "Modified")
                new_track.append(msg)
            except Exception as e:
                print(f"Error processing message: {e}")
                continue

        new_mid.tracks.append(new_track)

    if validate_midi_file(new_mid):
        try:
            new_mid.save(output_path)
            print(f"Humanized MIDI file saved to: {output_path}")
        except Exception as e:
            print(f"Error saving MIDI file: {e}")
    else:
        print("MIDI file validation failed, file not saved.")

def extract_metadata(sid_path):
    """Extract metadata from a SID file."""
    try:
        result = subprocess.run(['sidtool', '--info', sid_path], capture_output=True)
        # Decode the output as a string. If it contains binary data, use 'replace' or 'ignore'
        metadata = result.stdout.decode('utf-8', errors='replace')
    except Exception as e:
        print(f"Error running sidtool: {e}")
        return None

    # Now metadata is a string and can be used with regular expressions in extract_info
    name = extract_info(metadata, 'Name:')
    author = extract_info(metadata, 'Author:')
    released = extract_info(metadata, 'Released:')
    num_songs = extract_info(metadata, 'Songs:', int)
    return name, author, released, num_songs

def extract_info(text, key, cast_type=str):
    """Extract specific information from text using a key."""
    import re
    if cast_type is int:
        match = re.search(f"{key} (\\d+)", text)
    else:
        match = re.search(f"{key} (.*)", text)
    
    if match:
        return cast_type(match.group(1))
    return None

def convert_and_humanize(sid_path, output_dir):
    """Convert SID songs to MIDI and apply humanization."""
    name, author, released, num_songs = extract_metadata(sid_path)
    if num_songs is None:
        print("Could not determine the number of songs in the SID file.")
        return

    base_name = os.path.splitext(os.path.basename(sid_path))[0]
    for song in range(1, num_songs + 1):
        temp_midi_path = f"{output_dir}/{base_name}_song{song}.mid"
        output_midi_path = f"{output_dir}/{base_name}_song{song}_Humanized.mid"

        result = subprocess.run(['sidtool', '--out', temp_midi_path, '--format', 'midi', '--song', str(song), sid_path, '-f', '20000'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"sidtool conversion failed for song {song}: {result.stderr}")
            continue

        humanize_midi(temp_midi_path, output_midi_path, 0.2, 0.01, name, author, released)
        os.remove(temp_midi_path)
        print(f"Conversion and humanization of song {song} complete. Output saved to {output_midi_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <path-to-sid-file> <output-directory>")
        sys.exit(1)

    sid_file_path = sys.argv[1]
    output_directory = sys.argv[2]
    convert_and_humanize(sid_file_path, output_directory)
