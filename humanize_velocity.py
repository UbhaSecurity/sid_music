import sys
import random
from mido import MidiFile, MidiTrack, Message

def humanize_velocity(velocity, strength=0.2):
    """ Humanize velocity to add a natural feel without exceeding MIDI limits. """
    variation_range = int(127 * strength)
    variation = random.randint(-variation_range, variation_range)
    new_velocity = max(0, min(127, velocity + variation))
    return new_velocity

def humanize_midi(input_path, output_path, strength=0.2):
    """ Read a MIDI file, humanize the velocity of note-on events, and save to a new file. """
    mid = MidiFile(input_path)
    new_mid = MidiFile(ticks_per_beat=mid.ticks_per_beat)  # Maintain original timing

    for track in mid.tracks:
        new_track = MidiTrack()
        for msg in track:
            # Ensure we are copying all non-note_on messages directly
            if msg.type != 'note_on':
                new_track.append(msg)
            else:
                # Humanize only the velocity of 'note_on' messages
                new_velocity = humanize_velocity(msg.velocity, strength)
                # Create a new message with the same parameters except for the modified velocity
                new_msg = Message('note_on', note=msg.note, velocity=new_velocity, time=msg.time, channel=msg.channel)
                new_track.append(new_msg)
        new_mid.tracks.append(new_track)

    # Save the modified MIDI file
    new_mid.save(output_path)

def main(input_file, output_file, strength=0.2):
    # Humanize velocities in the MIDI file
    humanize_midi(input_file, output_file, strength)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python humanize_velocity.py <input_midi> <output_midi> [strength]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    strength_arg = float(sys.argv[3]) if len(sys.argv) > 3 else 0.2

    main(input_path, output_path, strength_arg)
