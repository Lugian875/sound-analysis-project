import tkinter as tk

from audio_handler import load_audio, audio_tinkering
from data_analysis import analyze_audio
from reporting import generate_report

root = tk.Tk() #Initializes something tkinter related

#Title, Default Window Size
root.title('SPIDAM Project')
root.geometry('1280x720+300+300')
root.resizable(True,True)

# Global Variables
audio_path = "" # Saves path for audio file used in project for future use
results = "" # Saves results for future use

# Functions

# For updating the status box with new status messages
def update_status(message):
    status_box['state'] = 'normal'
    status_box.insert(tk.END,message + "\n")
    status_box['state'] = 'disabled'

# For clearing the status box
def clear_status():
    status_box['state'] = 'normal'
    status_box.delete(1.0,tk.END) # Clears status box
    status_box['state'] = 'disabled'

# For loading and tinkering an audio file
def audio_handler():
    global audio_path
    audio_load_btn["state"] = 'disabled' # Disables load audio button
    status_box['state'] = 'normal'
    clear_status()
    audio_path = load_audio(update_status) # Runs audio loader
    audio_tinkering(update_status) # Runs audio tinkerer
    audio_load_btn["state"] = 'normal' # Enables load audio button again
    audio_analysis_btn["state"] = 'normal' # Enables the audio analysis button
    print(audio_path)

# For analyzing audio
def audio_analysis():
    global audio_path
    global results
    audio_analysis_btn["state"] = 'disabled' # Disables analysis button
    clear_status()
    results = analyze_audio(audio_path) # Calculates results
    generate_report(results,update_status) # Prints results
    plot_switcher_btn["state"] = 'normal' # Enables the plot switcher button


def plot_switcher():
    pass


# GUI Layout

# Title Label (centered at top)
title = tk.Label(
    root, text='Python Interactive Data Modeling Project', font='Arial 32 bold', fg='black')
title.pack(side=tk.TOP, pady=10)

# Frame to store the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Load Audio Button
audio_load_btn = tk.Button(
    button_frame, text="Load Audio", font='Arial 12', fg='black',command=lambda:[audio_handler()]
)
audio_load_btn.pack(side=tk.LEFT,padx=10)

# Audio Analysis Button
audio_analysis_btn = tk.Button(
    button_frame, text="Analyze Audio", font='Arial 12',fg='black', state="disabled", command=lambda:[audio_analysis()]
)
audio_analysis_btn.pack(side=tk.LEFT, padx=10)

# Plot Switcher Button(s)
plot_switcher_btn = tk.Button(
    button_frame, text= "Next Plot", font='Arial 12', fg='black', state='disabled', command=lambda:[plot_switcher()]
)
plot_switcher_btn.pack(padx=10)

#Status Box
status_box = tk.Text (
    root,font='Arial 10',width=100,height=10,wrap=tk.WORD, state='disabled'
)
status_box.pack(pady=50)

# Canvas for graph drawing?

root.mainloop() # Do not remove this line, as it is necessary for the window to pop up
