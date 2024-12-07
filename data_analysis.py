import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, butter, filtfilt


# For finding the target frequency closest to the target
def find_target_frequency(freqs, target):
    return freqs[np.abs(freqs-target).argmin()]

# For filtering the audio through a band-pass filter (for legibility?)
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

# For calculating RT60 time and finding points for the graph (it's complicated)
def rt60_calculation_and_points(data_in_db,t):
    # Finds index of maximum dB value
    index_of_max = np.argmax(data_in_db)
    value_of_max = data_in_db

    # Slices array from maximum value
    sliced_array = data_in_db[index_of_max:]
    value_of_max_less_5 = value_of_max - 5
    value_of_max_less_25 = value_of_max - 25

    # For finding the nearest value in the array
    def find_nearest_value(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    # Finding the nearest value for max-5dB and its index
    value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
    index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)[0][0]

    # Finding the nearest value for max-25dB and its index
    value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
    index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)[0][0]

    # Points on the RT60 plot for graphing
    max_pt = t[index_of_max], data_in_db[index_of_max], 'go'
    max_less_5pt = t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo'
    max_less_25pt = t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro'

    rt60 = 3 * (t[index_of_max_less_5] - t[index_of_max_less_25])

    return max_pt, max_less_5pt, max_less_25pt, rt60


def analyze_audio(audio_path):
    # Loads the audio
    audio_data, sample_rate = librosa.load(audio_path, sr=None)

    # Time vector. Used for graph plotting
    t = np.linspace(0, len(audio_data) / sample_rate, len(audio_data), endpoint=False)

    # Finds duration
    duration = librosa.get_duration(y=audio_data, sr=sample_rate)

    # Finds resonant frequency
    frequencies, power = welch(audio_data,sample_rate,nperseg=4096)
    resonance_freq = frequencies[np.argmax(power)]

    # For calculating RT60 Values
    # low freq: 100 Hz
    # mid freq: 1000 Hz
    # high freq: 10000 Hz

    # Fourier Transform of the signal (idk what that is)
    fft_result = np.fft.fft(audio_data)
    spectrum = np.abs(fft_result)  # Get magnitude spectrum
    freqs = np.fft.fftfreq(len(audio_data), d=1 / sample_rate)

    # Positive frequencies
    freqs = freqs[:len(freqs) // 2]
    spectrum = spectrum[:len(spectrum) // 2]

    # Finds target frequencies
    target_frequencies = {
        "low" : find_target_frequency(freqs, 100),
        "mid" : find_target_frequency(freqs, 1000),
        "high" : find_target_frequency(freqs, 10000)
    }

    # Band-pass filter over the target frequencies
    filtered_data = { }
    for x,y in target_frequencies.items():
        filtered_data[x] = bandpass_filter(
            audio_data, y - 50, y + 50, sample_rate)

    # Converts the filtered audio signal to decibel scale
    data_in_db = { }
    for x,y in filtered_data.items():
        data_in_db[x] = 10 * np.log10(np.abs(y) + 1e-10)


    # rt60_values = {
    #     "low": np.random.normal(0.6, 0.1, 8),
    #     "mid": np.random.normal(0.8, 0.1, 8),
    #     "high": np.random.normal(1.0, 0.1, 8)
    # }

    # Calculate differences from target RT60 of 0.5 seconds
    # target_rt60 = 0.5
    # rt60_differences = {
    #     freq: [value - target_rt60 for value in values]
    #     for freq, values in rt60_values.items()
    # }
    
    # Plots the waveform
    plt.figure(2)
    librosa.display.waveshow(audio_data, sr=sample_rate)
    plt.title("Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    waveform_fig = plt.gcf()
    plt.close()

    # Plots the RT60 scatter plots for each frequency range.
    rt60_figures = []

    # for freq, rt60_data in rt60_values.items():
    #     plt.figure(figsize=(8, 6))
    #     plt.scatter(range(len(rt60_data)), rt60_data, label=f"RT60 - {freq}")
    #     plt.plot(range(len(rt60_data)), rt60_data, color='black', linestyle='-', alpha=0.5)
    #     plt.title(f"RT60 Values for {freq} Frequency Range")
    #     plt.xlabel("Data Points")
    #     plt.ylabel("RT60 (seconds)")
    #     rt60_figures.append(plt.gcf())
    #     plt.close()

    # Create the overlapping RT60 scatter plot thats needed
    plt.figure(figsize=(8, 6))
    # for freq, rt60_data in rt60_values.items():
    #     plt.scatter(range(len(rt60_data)), rt60_data, label=f"{freq} RT60")
    #     plt.plot(range(len(rt60_data)), rt60_data, linestyle='-', alpha=0.5)
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
        # "rt60": rt60_values,
        # "rt60_differences": rt60_differences,
        "waveform_fig": waveform_fig,
        "rt60_figures": rt60_figures,
        "overlap_rt60_fig": overlap_rt60_fig,
        "amplitude_histogram_fig": amplitude_histogram_fig,
    }
