import tkinter as tk
import audio_handler as ah

root = tk.Tk()

#Title, Default Window Size, and it is r
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

# Widgets
# Title Label (centered at top)
title = tk.Label(
    root, text='Python Interactive Data Modeling Project', font='Arial 32 bold', fg='black')
title.grid(column=1, row=0, sticky='N')

# Load Audio Button
load_audio_btn = tk.Button(
    root, text = "Load Audio", font='Arial 12', fg='black',command=lambda:[ah.load_audio()]
)
load_audio_btn.grid(column=1,row=0,pady='80',sticky='N')
# Cleaner button?

# Summary stats button

# Plot switcher button

root.mainloop() # Do not remove this line, as it is necessary for the window to pop up
