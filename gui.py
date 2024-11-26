import tkinter as tk

root = tk.Tk()

root.title('SPIDAM Project')
root.geometry('1366x768+300+300')
root.resizable(True,True)

# Widgets
title = tk.Label(
    root, text = 'Python Interactive Data Modeling Project', font = ('Arial 16 bold'), bg= 'white', fg= 'black'
).grid(column=0, row=0)

words = tk.Label(
    root, text = "Help me please :(", font=('Arial 12'), bg='white',fg='black'
).grid(column=0,row=1)

root.mainloop() # Do not remove this line, as it is necessary for the window to pop up
