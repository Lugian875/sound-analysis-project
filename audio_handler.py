# import tkinter as tk
from tkinter import filedialog, messagebox
import librosa
import soundfile as sf

# Issac wrote the code, despite what the commits says

def load_audio():
    # print("Audio Loader triggered")

    # Asks user for audio file
    audio_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.aac")])
    if not audio_path:
        messagebox.showwarning("No File Selected", "Please choose an audio file.")
        return

    try:
        # Convert the file type to ".wav" if necessary
        if not audio_path.endswith(".wav"):
            converted_path = audio_path.rsplit('.', 1)[0] + "_converted.wav"
            audio_data, sample_rate = librosa.load(audio_path, sr=None, mono=False)
            sf.write(converted_path, audio_data, sample_rate)
            audio_path = converted_path
            messagebox.showinfo("Conversion Done", f"File converted to WAV: {audio_path}")

        # Data Validation
        audio_data, sample_rate = librosa.load(audio_path, sr=None)
        if audio_data.size == 0:
            raise ValueError("Selected audio file is empty.")
        messagebox.showinfo("Validation Success", "Audio file passed validation.")

        # Remove metadata
        cleaned_path = audio_path.rsplit('.', 1)[0] + "_no_metadata.wav"
        sf.write(cleaned_path, audio_data, sample_rate)
        messagebox.showinfo("Metadata Removed", f"Metadata-free file saved: {cleaned_path}")

        # Converts dual-channel to single-channel audio
        mono_path = cleaned_path.rsplit('.', 1)[0] + "_mono_channel.wav"
        audio_data, sample_rate = librosa.load(cleaned_path, sr=None, mono=True)
        sf.write(mono_path, audio_data, sample_rate)
        messagebox.showinfo("Processing Complete", f"Mono file saved: {mono_path}")

    # Handles all exceptions
    except Exception as e:
         messagebox.showerror("Error", f"Audio processing failed: {e}")
