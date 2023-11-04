import mido
from mido import MidiFile, MidiTrack, Message
import random

def humanize_velocity(velocity, strength=0.2):
    """ Humanize velocity to add a natural feel without exceeding MIDI limits """
    # Calculate the range for random variation
    variation_range = int(127 * strength)  
    # Apply random variation within the range
    variation = random.randint(-variation_range, variation_range)
    # Make sure the new velocity is within MIDI velocity range 0-127
    new_velocity = max(0, min(127, velocity + variation))
    return new_velocity

def modify_midi_velocity(midi_path, output_path):
    mid = MidiFile(midi_path)
    new_mid = MidiFile(ticks_per_beat=mid.ticks_per_beat)  # Maintain original timing

    for track in mid.tracks:
        new_track = MidiTrack()
        for msg in track:
            # Only modify the velocity of 'note_on' messages
            if msg.type == 'note_on':
                msg.velocity = humanize_velocity(msg.velocity)
            new_track.append(msg)
        new_mid.tracks.append(new_track)

    # Save the modified MIDI file
    new_mid.save(output_path)

input_midi_path = 'Delta.mid'  # Replace with your MIDI file's path
output_midi_path = 'output.mid'  # Replace with the desired output file's path

# Modify the MIDI file
try:
    modify_midi_velocity(input_midi_path, output_midi_path)
    print(f'Modified MIDI saved as {output_midi_path}')
except EOFError:
    print("The MIDI file might be incomplete or corrupted.")
except IOError as e:
    print(f"I/O error({e.errno}): {e.strerror}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
