import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

# this is voodoo magic
def analyze_audio(audio_path):
    # Loads the audio
    audio_data, sample_rate = librosa.load(audio_path, sr=None)

    # Finds duration
    duration = librosa.get_duration(y=audio_data, sr=sample_rate)

    # Finds resonant frequency
    frequencies, power = welch(audio_data,sample_rate,nperseg=4096)
    resonance_freq = frequencies[np.argmax(power)]

    # Compute all of the RT60 values (i just have placeholder values here atm)
    rt60_values = {
        "low": np.random.normal(0.6, 0.1, 8),  # This Generates 8 data points for the graph, this can be edited to be more or less if preferred
        "mid": np.random.normal(0.8, 0.1, 8),
        "high": np.random.normal(1.0, 0.1, 8)
    }

    # Calculate differences from target RT60 of 0.5 seconds
    target_rt60 = 0.5
    rt60_differences = {
        freq: [value - target_rt60 for value in values]
        for freq, values in rt60_values.items()
    }
    
    # Plots the waveform
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(audio_data, sr=sample_rate)
    plt.title("Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    waveform_fig = plt.gcf()
    plt.close()

    # Plots the RT60 scatter plots for each frequency range. I think this works
    rt60_figures = []
    for freq, rt60_data in rt60_values.items():
        plt.figure(figsize=(8, 6))
        plt.scatter(range(len(rt60_data)), rt60_data, label=f"RT60 - {freq}")
        plt.plot(range(len(rt60_data)), rt60_data, color='black', linestyle='-', alpha=0.5)
        plt.title(f"RT60 Values for {freq} Frequency Range")
        plt.xlabel("Data Points")
        plt.ylabel("RT60 (seconds)")
        rt60_figures.append(plt.gcf())
        plt.close()

    # Create the overlapping RT60 scatter plot thats needed
    plt.figure(figsize=(8, 6))
    for freq, rt60_data in rt60_values.items():
        plt.scatter(range(len(rt60_data)), rt60_data, label=f"{freq} RT60")
        plt.plot(range(len(rt60_data)), rt60_data, linestyle='-', alpha=0.5)
    plt.title("Overlapping RT60 Values for All Frequencies")
    plt.xlabel("Data Points")
    plt.ylabel("RT60 (seconds)")
    overlap_rt60_fig = plt.gcf()
    plt.close()

    # Generate a Histogram of Amplitudes because we are required to have at least 6 graphs and we needed one more (was easy to do)
    plt.figure(figsize=(8, 6))
    plt.hist(audio_data, bins=50, color='c', alpha=0.75)
    plt.title("Histogram of Amplitudes")
    plt.xlabel("Amplitude")
    plt.ylabel("Frequency")
    amplitude_histogram_fig = plt.gcf()
    plt.close()

    return {
        "duration": duration,
        "resonance frequency": resonance_freq,
        "rt60": rt60_values,
        "rt60_differences": rt60_differences,
        "waveform_fig": waveform_fig,
        "rt60_figures": rt60_figures,
        "overlap_rt60_fig": overlap_rt60_fig,
        "amplitude_histogram_fig": amplitude_histogram_fig,
    }
