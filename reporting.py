def generate_report(audio_path, callback):
    # This displays in the status box
    callback("Analysis Report")

    duration = audio_path["duration"]
    res_freq = audio_path["resonance frequency"]
    rt60 = audio_path["rt60"]
    rt60_diff = audio_path["rt60_difference"]
    
    callback(
        f'Audio Duration: {duration:.2f} seconds\n'
        f'Resonance Frequency: {round(res_freq)} Hz\n'
        f'RT60 Values:\n'
        f'Low Frequency: {rt60["Low"]["RT60 Value"]} seconds\n'
        f'Mid Frequency: {rt60["Mid"]["RT60 Value"]} seconds\n'
        f'High Frequency: {rt60["High"]["RT60 Value"]} seconds\n'
        f'RT60 Difference vs .5 seconds: {rt60_diff} seconds\n'
    )
