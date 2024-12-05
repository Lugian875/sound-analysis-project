import tkinter as tk
from tkinter import filedialog, messagebox
from audio_loader import load_audio
from data_cleaner import clean_audio
from data_analysis import analyze_audio
from reporting import generate_report
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AudioAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Analysis Application")

        # 2 Buttons at the Top
        self.load_button = tk.Button(root, text="Load Audio", command=self.load_audio)
        self.load_button.pack(pady=10)

        self.analyze_button = tk.Button(root, text="Analyze Audio", command=self.analyze_audio, state="disabled")
        self.analyze_button.pack(pady=10)

        # Create a canvas for scrolling
        # In hindsight, making this just show all of the graphs dynamically without the need of the scrollwheel would prob be better than this 
        self.canvas = tk.Canvas(root)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Add a scrollbar for the canvas
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame that holds the results (this will be placed inside of the canvas itself)
        self.results_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.results_frame, anchor="nw")

        # Placeholder for audio path
        self.audio_path = None


    def load_audio(self):
        self.audio_path = load_audio()
        if self.audio_path:
            self.analyze_button.config(state="normal")

    def analyze_audio(self):
        if not self.audio_path:
            messagebox.showwarning("No File", "Please load an audio file first.")
            return

        cleaned_path = clean_audio(self.audio_path)
        results = analyze_audio(cleaned_path)

        # Generate the report
        generate_report(results)

        # Display all of the graphs in the GUI
        self.display_waveform(results["waveform_fig"])
        self.display_rt60_graphs(results["rt60_figures"])
        self.display_overlap_rt60_graph(results["overlap_rt60_fig"])
        self.display_amplitude_histogram(results["amplitude_histogram_fig"])

        # Update the scrollable region after adding the content so it actually works
        self.results_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def display_waveform(self, waveform_fig):
        # Embed the waveform plot in the Tkinter window so it actually shows
        canvas = FigureCanvasTkAgg(waveform_fig, master=self.results_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    def display_rt60_graphs(self, rt60_figures):
        # Embed the RT60 scatter plots in the Tkinter window so it once again gets it to actually show
        for rt60_fig in rt60_figures:
            canvas = FigureCanvasTkAgg(rt60_fig, master=self.results_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)

    def display_overlap_rt60_graph(self, overlap_rt60_fig):
        # Embed the overlapping RT60 scatter plot in the Tkinter window, you get the drift
        canvas = FigureCanvasTkAgg(overlap_rt60_fig, master=self.results_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    def display_amplitude_histogram(self, amplitude_histogram_fig):
        # Embed the amplitude histogram in the Tkinter window, same here
        canvas = FigureCanvasTkAgg(amplitude_histogram_fig, master=self.results_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioAnalysisApp(root)
    root.mainloop()
