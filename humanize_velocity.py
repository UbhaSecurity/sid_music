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

def add_metadata_to_track(track, name, author, released):
    """Add metadata as text messages to the MIDI track."""
    if name:
        track.append(MetaMessage('text', text=f"Name: {name}"))
    if author:
        track.append(MetaMessage('text', text=f"Author: {author}"))
    if released:
        track.append(MetaMessage('text', text=f"Released: {released}"))

def humanize_midi(input_path, output_path, velocity_strength, timing_strength, name, author, released):
    try:
        mid = MidiFile(input_path)
    except OSError as e:
        print(f"Error processing MIDI file: {e}")
        return  # Return early since 'mid' is not set

    new_mid = MidiFile(ticks_per_beat=mid.ticks_per_beat)

    # Create a new track for metadata
    metadata_track = MidiTrack()
    add_metadata_to_track(metadata_track, name, author, released)
    new_mid.tracks.append(metadata_track)

    for track in mid.tracks:
        new_track = MidiTrack()
        for msg in track:
            if msg.type == 'note_on':
                # Humanize only the velocity of 'note_on' messages
                new_velocity = humanize_velocity(msg.velocity, velocity_strength)
                new_msg = Message('note_on', note=msg.note, velocity=new_velocity, time=msg.time, channel=msg.channel)
                # Apply timing variation
                new_msg = apply_timing_variation(new_msg, timing_strength)
                new_track.append(new_msg)
            else:
                # Copy all other messages directly
                new_track.append(msg)

        new_mid.tracks.append(new_track)

    # Save the modified MIDI file
    new_mid.save(output_path)

def main(input_file, output_file, velocity_strength, timing_strength, name, author, released):
    """Process a MIDI file with humanization and metadata."""
    humanize_midi(input_file, output_file, velocity_strength, timing_strength, name, author, released)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python humanize_velocity.py <input_midi> <output_midi> [velocity_strength] [timing_strength] [name] [author] [released]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    vel_strength = float(sys.argv[3]) if len(sys.argv) > 3 else 0.2
    timing_strength = float(sys.argv[4]) if len(sys.argv) > 4 else 0.01
    name = sys.argv[5] if len(sys.argv) > 5 else ""
    author = sys.argv[6] if len(sys.argv) > 6 else ""
    released = sys.argv[7] if len(sys.argv) > 7 else ""

    main(input_path, output_path, vel_strength, timing_strength, name, author, released)
