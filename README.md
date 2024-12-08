Project Description:
  The Scientific Python Interactive Data Acoustic Modeling (SPIDAM) project exists to analyze and model auditory data captured in enclosed spaces. It measures reverberation time (RT60) in low, mid, and high frequencies. This data is used to craft visual representations as graphs. The project Utilizes various libraries, calculations, visuals, and an easy to use GUI to accurately and simply display data. 

Project Purpose:
	The SPIDAM project aims to combat excess reverberation in enclosed spaces to increase intelligibility. It does this by analyzing data in uploaded audio recordings. From there, it singles out outlying frequencies that could interfere with comprehension. These inconsistencies are adjusted and the RT60 values of before and after the change are recorded and modeled. 

Usage Instructions:
  Prerequisites:
    Python 3.8+
    pip for dependency management.
    
Steps:
  Clone the repository:
    git clone https://github.com/Lugian875/sound-analysis-project/tree/testing
  Navigate to the project directory:
    cd main-repo
  Install dependencies:
    pip install -r requirements.txt
    
Usage:
  Launch the application
    python3 gui.py
  Use the GUI to:
    Load audio files.
    Analyze and visualize RT60 data.
    Play audio files.
