import tkinter as tk

root = tk.Tk()

#Title, Default Window Size, and it is r
root.title('SPIDAM Project')
root.geometry('1366x768+300+300')
root.resizable(True,True)

#idk what this does
frame = tk.Frame(root)
root.rowconfigure(0,weight=1)
root.columnconfigure(0,weight=1)
frame.grid(column=0,row=0,sticky='NESW')
grid = tk.Frame(frame)
grid.grid(column=0,row=7,sticky='NESW',columnspan=2)
root.rowconfigure(7,weight=1)
root.columnconfigure(7,weight=1)

# Widgets
title = tk.Label(
    root, text = 'Python Interactive Data Modeling Project', font = ('Arial 16 bold'), bg= 'white', fg= 'black'
).grid(column=1,row=0,sticky='N')

load_audio_btn = tk.Button(
    root, text = "Load Audio", font=('Arial 12'), bg='white',fg='black'
).grid(column=1,row=0,pady='40',sticky='N')


root.mainloop() # Do not remove this line, as it is necessary for the window to pop up
