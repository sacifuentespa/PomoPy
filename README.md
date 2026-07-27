# PomoPy: A Python Pomodoro Timer

A lightweight, cross-platform desktop Pomodoro timer built with Python and Tkinter. Features multi-threading for accurate countdowns and native OS audio integration for zero-dependency alarms.

## Features
* Customizable Work and Break intervals.
* Background threading ensures the UI never freezes.
* Native system audio integration (Windows, macOS, Linux) without heavy libraries.
* Auto-transitions between Work and Break phases.

## Prerequisites

**Windows / macOS:**
Python 3.8+ is required. Tkinter is included by default.

**Linux (Ubuntu/Debian):**
Tkinter and aplay are required. Install them via:
`sudo apt update && sudo apt install python3-tk alsa-utils`

## Installation

1. Clone the repository:
   `git clone https://github.com/sacifuentespa/PomoPy.git`
2. Navigate to the directory:
   `cd PomoPy`
3. The alarm sound:

    Alarm from Sound Effect by <a href="https://pixabay.com/users/universfield-28281460/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=151927">Universfield</a> from <a href="https://pixabay.com/sound-effects//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=151927">Pixabay</a>
   
   If you want to change the alarm, ensure an `.wav` file is located inside the `assets/` folder and change the sound_file = os.path.join(current_dir,"assets", "universfield-digital-alarm-clock.wav") name apropiately in main.py play_alarm method.

## Usage
Run the application from the terminal:
`python main.py`
