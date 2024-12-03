import librosa
import soundfile as sf

def clean_audio(audio_path):
    # This is the code a separated from Issacs code earlier just to make stuff neater for me.

    audio_data, sample_rate = librosa.load(audio_path, sr=None)
    cleaned_path = audio_path.rsplit('.', 1)[0] + "_cleaned.wav"

    # Removes the metadata and prompty saves the clean audio
    sf.write(cleaned_path, audio_data, sample_rate)

    # Converts the audio to mono per the requirements
    mono_data = librosa.to_mono(audio_data)
    mono_path = cleaned_path.rsplit('.', 1)[0] + "_mono.wav"
    sf.write(mono_path, mono_data, sample_rate)
    return mono_path
