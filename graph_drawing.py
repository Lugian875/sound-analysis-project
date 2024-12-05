from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# For displaying the waveform graph (Plot 1)
def display_waveform(graph_frame,waveform_fig):
    canvas = FigureCanvasTkAgg(waveform_fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# For displaying the RT60 graphs (Plots 2-4)
def display_rt60_graphs(graph_frame,rt60_figures, plot_num):
    canvas= None
    match plot_num:
        case 2:
            canvas = FigureCanvasTkAgg(rt60_figures[0], master=graph_frame) # Displays low frequency graph
        case 3:
            canvas = FigureCanvasTkAgg(rt60_figures[1], master=graph_frame) # Displays mid-frequency graph
        case 4:
            canvas = FigureCanvasTkAgg(rt60_figures[2], master=graph_frame) # Displays high frequency graph

    canvas.draw()
    canvas.get_tk_widget().pack()

# For displaying the combined RT60 graphs (Plot 5)
def display_overlap_rt60_graph(graph_frame, overlap_rt60_fig):
    canvas = FigureCanvasTkAgg(overlap_rt60_fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# For displaying the amplitude histogram (Plot 6)
def display_amplitude_histogram(graph_frame, amplitude_histogram_fig):
    canvas = FigureCanvasTkAgg(amplitude_histogram_fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()