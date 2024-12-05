# import tkinter as tk
from tkinter import filedialog, messagebox
import librosa
import soundfile as sf
from pydub import AudioSegment

# Issac wrote the code, despite what the commits says

def load_audio():
    # print("Audio Loader triggered")
    # Asks user for audio file
    audio_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
    if not audio_path:
        # If this is triggered, the "Load Audio" button should return
        messagebox.showwarning("No File Selected", "Please choose an audio file.")
        return

    try:
        # Convert the file type to ".wav" if necessary
        sound = AudioSegment.from_file(audio_path)
        converted_path = audio_path.rsplit('.', 1)[0] + "_converted.wav"
        sound.export(converted_path, format='wav')
        if not audio_path.endswith(".wav"):
            messagebox.showinfo ("File converted from .mp3, to .wav", f"Saved at {converted_path}" )
        else:
            messagebox.showinfo ("File duplicated for the program", f"Saved at {converted_path}" )
        audio_path = converted_path

        # Data Validation
        audio_data, sample_rate = librosa.load(audio_path, sr=None)
        if audio_data.size == 0:
            raise ValueError("Selected audio file is empty.")
        messagebox.showinfo("Validation Success", "Audio file passed validation.")

        # Remove metadata
        # cleaned_path = audio_path.rsplit('.', 1)[0] + "_no_metadata.wav"
        sf.write(audio_path, audio_data, sample_rate)
        messagebox.showinfo("Metadata Removed", f"Metadata-free file saved")

        # Converts dual-channel to single-channel audio
        # mono_path = cleaned_path.rsplit('.', 1)[0] + "_mono_channel.wav"
        audio_data, sample_rate = librosa.load(audio_path, sr=None, mono=True)
        sf.write(audio_path, audio_data, sample_rate)
        messagebox.showinfo("Processing Complete", f"Mono file saved")
    # Handles all exceptions
    except Exception as e:
         messagebox.showerror("Error", f"Audio processing failed: {e}")
