import tkinter as tk
from tkinter import ttk
import logging


class PomodoroUI:
    def __init__(self, root: tk.Tk):
        """
        Initialize the main user interface window.
        """
        self.root = root
        self.root.title("Python Pomodoro")
        self.root.geometry("350x250")  # Width x Height
        self.root.resizable(False, False)  # Keep the window fixed size

        # Configure styling for a cleaner look
        self.style = ttk.Style()
        self.style.theme_use("clam")  # 'clam' allows for better color customization

        # --- THE MAIN CONTAINER ---
        # We use a main frame with padding to keep widgets away from the window edges
        self.main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        self.main_frame.pack(expand=True, fill="both")

        # --- WIDGET SETUP ---
        self._create_widgets()

    def _create_widgets(self):
        """Creates and places all visual elements on the screen."""
        # 1. THE TIME DISPLAY
        # We use a StringVar so we can dynamically update the label text later
        self.time_string = tk.StringVar(value="25:00")

        # Create a ttk.Label widget assigned to self.time_label.

        self.time_label = ttk.Label(
            self.main_frame,
            textvariable=self.time_string,
            font=("Helvetica", 48, "bold"),
        )

        self.time_label.pack(pady=20)

        # A horizontal frame to hold our buttons side-by-side

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        # TODO 2: Create three ttk.Button widgets inside self.button_frame:
        #   - self.start_btn with text="Start"
        self.start_btn = ttk.Button(self.button_frame, text="Start")
        self.start_btn.pack(side="left", padx=5)
        #   - self.pause_btn with text="Pause"
        self.pause_btn = ttk.Button(self.button_frame, text="Pause")
        self.pause_btn.pack(side="left", padx=5)
        #   - self.reset_btn with text="Reset"
        self.reset_btn = ttk.Button(self.button_frame, text="Reset")
        self.reset_btn.pack(side="left", padx=5)
        # For now, do NOT assign any 'command' parameter to them!
        # Place each button using .pack(side="left", padx=5).

    def update_display(self, formatted_time: str):
        """
        This method will be called by the Conductor (main.py) to update the time shown on screen.
        """
        # TODO 3: Update the self.time_string with the new formatted_time.
        self.time_string.set(formatted_time)        

if __name__ == "__main__":
    # Create the base Tkinter window
    root = tk.Tk()
    # Initialize our UI class
    app = PomodoroUI(root)
    # Start the Tkinter infinite loop (this keeps the window open and draws it!)
    root.mainloop()

