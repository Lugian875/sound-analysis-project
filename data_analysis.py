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
    value_of_max = data_in_db[index_of_max]

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
    max_pt = t[index_of_max], data_in_db[index_of_max], 'green'
    max_less_5pt = t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yellow'
    max_less_25pt = t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'red'

    rt60 = 3 * (t[index_of_max_less_5] - t[index_of_max_less_25])

    return max_pt, max_less_5pt, max_less_25pt, rt60


# The main code block  (really gross)
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
        "Low" : find_target_frequency(freqs, 100),
        "Mid" : find_target_frequency(freqs, 1000),
        "High" : find_target_frequency(freqs, 10000)
    }

    # Band-pass filter over the target frequencies
    filtered_data = { }
    for x,tf in target_frequencies.items():
        filtered_data[x] = bandpass_filter(
            audio_data, tf - 50, tf + 50, sample_rate)

    # Converts the filtered audio signal to decibel scale
    data_in_db = { }
    for x,fd in filtered_data.items():
        data_in_db[x] = 10 * np.log10(np.abs(fd) + 1e-10)

    # For calculating RT60 time and points for RT60 plots
    rt60_values_and_points = { } # Nested dictionary contains the necessary data
    for freq_label,val in data_in_db.items():
        max_pt, max_less_5pt, max_less_25pt, rt60 = rt60_calculation_and_points(val,t)

        # Dictionary for each frequency (low, mid, high) that stores graph points and RT60 time
        freq_data= {
            "maxdB" : max_pt,
            "max-5dB" : max_less_5pt,
            "max-25dB" : max_less_25pt,
            "RT60 Value" : np.round(np.abs(rt60),2)
        }
        rt60_values_and_points[freq_label] = freq_data

    # Difference in RT60 Value to reduce to .5 seconds
    rt60_difference = ((rt60_values_and_points["Low"]["RT60 Value"] +
                       rt60_values_and_points["Mid"]["RT60 Value"] +
                       rt60_values_and_points["High"]["RT60 Value"])
                        / 3 ) - .5
    
    # Waveform Plot
    plt.figure(figsize=(10,5))
    librosa.display.waveshow(audio_data, sr=sample_rate)
    plt.title("Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    waveform_fig = plt.gcf()
    plt.close()

    # RT60 Plot (also very complex)
    rt60_figures = []
    for freq_label, data in rt60_values_and_points.items():
        x_coords = [] # x-coordinate data
        y_coords = [] # y-coordinate data
        colors = []  #color data

        # For making sure that the right data is being read
        def has_enough_data(point_data):
            # Check if point_data is a tuple with exactly 3 elements (x, y, color) and not RT60 value
            if isinstance(point_data, tuple) and len(point_data) == 3:
                return True
            else:
                return False

        for data_point, point_data in data.items():
            if not has_enough_data(point_data):
                continue

            # Extracts data
            x,y,color = point_data
            x_coords.append(x)
            y_coords.append(y)
            colors.append(color)

        plt.figure(figsize=(10,5))
        # Plots the filtered signal in decibel scale
        plt.plot(t,data_in_db[freq_label],linewidth=1,alpha=0.7)

        plt.scatter(x_coords, y_coords, c=colors, marker = 'o') #Plots data

        plt.title(f'RT60 Plot for {freq_label} frequencies')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (db)')
        plt.grid()
        rt60_figures.append(plt.gcf())
        plt.close()

    #Combined RT60 Plot
    plt.figure(figsize=(10,5))
    for freq_label, data in data_in_db.items():
        plt.plot(t, data_in_db[freq_label], linewidth=1, alpha=0.7, label=freq_label)
    plt.title("Combined RT60 Value Graph")
    plt.xlabel("Data Points")
    plt.ylabel("RT60 (seconds)")
    plt.legend()
    overlap_rt60_fig = plt.gcf()
    plt.close()

    #Extra Graph: Amplitude Histogram
    plt.figure(figsize=(10,5))
    plt.hist(audio_data, bins=50, color='c', alpha=0.75)
    plt.title("Histogram of Amplitudes")
    plt.xlabel("Amplitude")
    plt.ylabel("Frequency")
    amplitude_histogram_fig = plt.gcf()
    plt.close()

    return {
        "duration": duration,
        "resonance frequency": resonance_freq,
        "rt60": rt60_values_and_points,
        "rt60_difference": rt60_difference,
        "waveform_fig": waveform_fig,
        "rt60_figures": rt60_figures,
        "overlap_rt60_fig": overlap_rt60_fig,
        "amplitude_histogram_fig": amplitude_histogram_fig,
    }
