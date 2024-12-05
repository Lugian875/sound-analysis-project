# import tkinter as tk
from tkinter import filedialog, messagebox
import librosa
import soundfile as sf
from pydub import AudioSegment

audio_path = ""


def load_audio(callback):
    # Asks user for audio file
    global audio_path
    audio_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
    if not audio_path:
        callback("No File Selected: Please choose an audio file")
        return

    try:
        # Convert the file type to ".wav" if necessary
        sound = AudioSegment.from_file(audio_path)
        converted_path = audio_path.rsplit('.', 1)[0] + "_converted.wav"
        sound.export(converted_path, format='wav')
        if not audio_path.endswith(".wav"):
            callback(f"File converted from .mp3, to .wav\n Saved at {converted_path}" )
        else:
            callback(f"File duplicated for the program\nSaved at {converted_path}" )
        audio_path = converted_path
        return audio_path
    except Exception as e:
        callback("Error", f"Audio processing failed: {e}")

def audio_tinkering(callback):
    # This first bit prevents big boy error
    if audio_path == "":
        return
    else:
        try:
            # Data Validation
            audio_data, sample_rate = librosa.load(audio_path, sr=None)
            if audio_data.size == 0:
                raise ValueError("Selected audio file is empty")
            callback("Audio file passed validation")

            # Remove metadata
            sf.write(audio_path, audio_data, sample_rate)
            callback("Metadata Removed")

            # Converts dual-channel to single-channel audio
            audio_data, sample_rate = librosa.load(audio_path, sr=None, mono=True)
            sf.write(audio_path, audio_data, sample_rate)
            callback("Converted to single-channel audio")
        # Handles all exceptions
        except Exception as e:
             callback("Error", f"Audio processing failed: {e}")