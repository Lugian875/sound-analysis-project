import tkinter as tk
from tkinter import scrolledtext

import audio_handler as ah

audio_path = "" #saves path for audio file used in project for future use

root = tk.Tk()

#Title, Default Window Size
root.title('SPIDAM Project')
root.geometry('1280x720+300+300')
root.resizable(True,True)

#Configures Window Frame and Grid for Widget Organization
frame = tk.Frame(root)
root.rowconfigure(0,weight=1)
root.columnconfigure(0,weight=1)
frame.grid(column=0,row=0,sticky='NESW')
grid = tk.Frame(frame)
grid.grid(column=0,row=7,sticky='NESW',columnspan=2)
root.rowconfigure(7,weight=1)
root.columnconfigure(7,weight=1)

# For updating the status box with new status messages
def update_status(message):
    status_box.insert(tk.END,message + "\n")
    status_box.see(tk.END)

# Function chain for loading audio
def load_audio():
    global audio_path
    load_audio_btn["state"] = 'disabled' #Disables audio button
    status_box.delete(1.0,tk.END) #Clears status box
    audio_path = ah.load_audio(update_status) #Runs audio loader,
    ah.audio_tinkering(update_status)
    load_audio_btn["state"] = 'normal'
    print(audio_path)

# Widgets
# Title Label (centered at top)
title = tk.Label(
    root, text='Python Interactive Data Modeling Project', font='Arial 32 bold', fg='black')
title.grid(column=1, row=0, sticky='N')

# Load Audio Button
load_audio_btn = tk.Button(
    root, text="Load Audio", font='Arial 12', fg='black',command=lambda:[load_audio()]
)
load_audio_btn.grid(column=1,row=0, pady=80, sticky='N')

# Audio Analysis Button
audio_analysis_btn = tk.Button(
    root, text="Analyze Audio", font='Arial 12',fg='black', state="disabled"
)
audio_analysis_btn.grid(column=1,row=0,pady=130, sticky='N')

#Text Box that displays status
status_box = scrolledtext.ScrolledText (
    root,font='Arial 10',width=50,height=10,wrap=tk.WORD
)
status_box.grid(column=1,row=2)

# Plot switcher button

root.mainloop() # Do not remove this line, as it is necessary for the window to pop up
