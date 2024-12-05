def generate_report(audio_path, callback):
    # This displays in the status box
    callback("Analysis Report")

    duration = audio_path["duration"]
    amplitude = audio_path["amplitude"]
    rt60 = audio_path["rt60"]
    rt60_diff = audio_path["rt60_differences"]
    
    callback(
        f"Audio Duration: {duration:.2f} seconds\n"
        f"Peak Amplitude: {amplitude:.2f}\n"
        f"RT60 Values:\n"
        f"Low Frequency: {rt60['low']} seconds\n"
        f"Mid Frequency: {rt60['mid']} seconds\n"
        f"High Frequency: {rt60['high']} seconds\n"
        f"RT60 Differences (Target = 0.5s):\n"
        f"Low Frequency: {rt60_diff['low']}\n"
        f"Mid Frequency: {rt60_diff['mid']}\n"
        f"High Frequency: {rt60_diff['high']}\n"
    )
