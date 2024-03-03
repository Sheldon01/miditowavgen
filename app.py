import subprocess
from flask import Flask, render_template, send_file, request
from random_generated_midi import generate_midi_sequence

app = Flask(__name__, template_folder='/home/sheldonwest/Music Generation Website/musicgenerationwebsite/templates')

# Define the path to the SoundFont file
SOUNDFONT_PATH = '/home/sheldonwest/Music Generation Website/musicgenerationwebsite/templates/Full Grand.sf2'

def convert_midi_to_wav(midi_file, output_file):
    subprocess.run(['fluidsynth', '-T', 'wav', '-F', output_file, SOUNDFONT_PATH, midi_file])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/random_generated_midi', methods=['GET'])
def generate_random_midi():
    # Generate a random MIDI file with a dynamic filename
    midi_file_path = generate_midi_sequence()
    
    if midi_file_path is not None:
        # Extract the filename from the path
        filename = midi_file_path.split('/')[-1]
        # Convert MIDI to WAV
        wav_file_path = midi_file_path.replace('.mid', '.wav')
        convert_midi_to_wav(midi_file_path, wav_file_path)
        # Send the generated WAV file to the client
        return send_file(wav_file_path, as_attachment=True, mimetype='audio/wav',)
    else:
        return "Failed to generate MIDI file", 500

if __name__ == '__main__':
    app.run(debug=True)

