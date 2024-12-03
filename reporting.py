from tkinter import messagebox

def generate_report(results):
    # This is the box that appears when you click analyze. Needed for a requirement
    duration = results["duration"]
    amplitude = results["amplitude"]
    rt60 = results["rt60"]

    message = (
        f"Audio Duration: {duration:.2f} seconds\n"
        f"Peak Amplitude: {amplitude:.2f}\n"
        f"RT60 Values:\n"
        f"  Low Frequency: {rt60['low']} seconds\n"
        f"  Mid Frequency: {rt60['mid']} seconds\n"
        f"  High Frequency: {rt60['high']} seconds\n"
    )
    messagebox.showinfo("Analysis Report", message)
