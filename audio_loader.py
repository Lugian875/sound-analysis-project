from tkinter import filedialog, messagebox
from os import path
from pydub import AudioSegment

def load_audio():
    # This is Issacs code, i just slightly modified and moved the metadata and mono conversion stuff to a separate script
    audio_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
    if not audio_path:
        messagebox.showwarning("No File Selected", "Please choose an audio file.")
        return None

    if not audio_path.endswith(".wav"):
        converted_path = audio_path.rsplit('.', 1)[0] + "_converted.wav"
        sound = AudioSegment.from_file(audio_path)
        sound.export(converted_path, format='wav')
        audio_path = converted_path
        messagebox.showinfo("File Converted", f"Converted to WAV: {converted_path}")

    return audio_path
