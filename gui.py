import tkinter as tk
from pickle import FALSE

from audio_handler import load_audio, audio_tinkering
from data_analysis import analyze_audio
from reporting import generate_report
from graph_drawing import display_waveform, display_rt60_graphs, display_overlap_rt60_graph, display_amplitude_histogram

root = tk.Tk() #Initializes something tkinter related

#Title, Default Window Size
root.title('SPIDAM Project')
root.geometry('1000x1000+500+0')
root.resizable(True,True)

# Global Variables
audio_path = None # Saves path for audio file used in project for future use
results = {} # Saves results for future use
plot_num = 0 # Iterating through plots?

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

# For analyzing audio
def audio_analysis():
    global audio_path
    global results
    audio_analysis_btn["state"] = 'disabled' # Disables analysis button
    clear_status()
    results = analyze_audio(audio_path) # Calculates results
    generate_report(results,update_status) # Prints results
    plot_switcher_next_btn["state"] = 'normal' # Enables the plot switcher buttons
    plot_switcher_prev_btn["state"] = 'normal'

# For switching plots
def plot_switcher(direction):
    global results
    global plot_num

    # Iterating the plot number
    if direction:
        plot_num = plot_num + 1
    else:
        plot_num = plot_num - 1

    # For keeping the plot number between the ranges of 1-6
    if plot_num > 6:
        plot_num = 1
    if plot_num < 1:
        plot_num = 6

    # For destroying the current plot
    for widget in graph_frame.winfo_children():
        widget.destroy()

    # For determining which plot to display
    match plot_num:
        case 1:
            display_waveform(graph_frame,results["waveform_fig"])
        case 2 | 3 | 4:
            display_rt60_graphs(graph_frame, results["rt60_figures"],plot_num)
        case 5:
            display_overlap_rt60_graph(graph_frame,results["overlap_rt60_fig"])
        case 6:
            display_amplitude_histogram(graph_frame,results["amplitude_histogram_fig"])


# GUI Widgets

# Title Label (centered at top)
title = tk.Label(
    root, text='Python Interactive Data Modeling Project', font='Arial 32 bold', fg='black')
title.pack(side=tk.TOP, pady=10)

# Frames to store the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
button_frame_2 = tk.Frame(root)
button_frame_2.pack(pady=10)

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

# Delete Audio Button?

# Plot Switcher Buttons
plot_switcher_prev_btn = tk.Button(
    button_frame_2, text= "Prev Plot", font='Arial 12', fg='black', state='disabled', command=lambda:[plot_switcher(False)]
)
plot_switcher_prev_btn.pack(side= tk.LEFT, padx=10)

plot_switcher_next_btn = tk.Button(
    button_frame_2, text= "Next Plot", font='Arial 12', fg='black', state='disabled', command=lambda:[plot_switcher(True)]
)
plot_switcher_next_btn.pack(padx=10)

#Status Box
status_box = tk.Text (
    root,font='Arial 10',width=100,height=10,wrap=tk.WORD, state='disabled'
)
status_box.pack(pady=30)

# Canvas for Graphs
graph_canvas = tk.Canvas(root)
graph_canvas.pack(side='left', fill='both',expand=True)
graph_frame = tk.Frame(graph_canvas) # Frame for holding graphs on the canvas
graph_canvas.create_window((0,0),window=graph_frame,anchor='nw')

root.mainloop() # Do not remove this line, as it is necessary for the window to pop up
