import random
import logging
from mido import MidiFile, MidiTrack, Message, MetaMessage

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Define parameters
MIN_NOTE = 60  # MIDI note value for C4
MAX_NOTE = 72  # MIDI note value for C5
NOTE_DURATION = 120  # Duration of each note in ticks (120 ticks per beat)
NUM_NOTES = 20  # Number of notes in the sequence

# Create a function to generate a random MIDI note sequence
def generate_midi_sequence():
    try:
        # Create a new MIDI file
        midi_file = MidiFile()
        track = MidiTrack()
        midi_file.tracks.append(track)

        # Set tempo (120 BPM)
        ticks_per_beat = midi_file.ticks_per_beat
        microseconds_per_beat = int(60 * 10**6 / 120)  # 120 BPM
        tempo_message = MetaMessage('set_tempo', tempo=microseconds_per_beat)
        track.append(tempo_message)

        # Generate random notes and add them to the track
        for _ in range(NUM_NOTES):
            note_value = random.randint(MIN_NOTE, MAX_NOTE)
            track.append(Message('note_on', note=note_value, velocity=64, time=0))
            track.append(Message('note_off', note=note_value, velocity=64, time=NOTE_DURATION))

        # Save the MIDI file with a unique filename
        filename = f'random_sequence_{random.randint(1000, 9999)}.mid'
        midi_file.save(filename)
        logging.debug(f"Generated MIDI file: {filename}")

        return filename
    except Exception as e:
        logging.error(f"Failed to generate MIDI file: {e}")
        return None
