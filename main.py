# main.py
import tkinter as tk
import threading
from core.timer import PomodoroTimer
from ui.main_window import PomodoroUI


class PomodoroController:
    def __init__(self, root: tk.Tk):
        self.root = root

        # Instantiate the Engine and the Face
        self.timer = PomodoroTimer(work_duration=25, break_duration=5)
        self.ui = PomodoroUI(root)

        # Wire the buttons
        self.ui.start_btn.config(command=self.start_timer)

        self.ui.pause_btn.config(command=self.pause_timer)
        self.ui.reset_btn.config(command=self.reset_timer)

        #  Start the continuous UI update loop
        self.update_ui_loop()

    def start_timer(self):
        """Triggered when the Start button is clicked."""

        try:
            ui_work = int(self.ui.work_var.get()) * 60
            ui_break = int(self.ui.break_var.get()) * 60
        except ValueError:
            ui_work, ui_break = 25 * 60, 5 * 60

        # SMART CHECK: Only update and reset if the user ACTUALLY changed the numbers
        if ui_work != self.timer.work_duration or ui_break != self.timer.break_duration:
            self.timer.pause()
            self.timer.work_duration = ui_work
            self.timer.break_duration = ui_break
            self.timer.reset()
            self.ui.update_display(self.timer.get_formatted_time())

        # Safely spawn the background thread
        if not self.timer.is_running:
            timer_thread = threading.Thread(target=self.timer.start)
            timer_thread.daemon = True 
            timer_thread.start()

    def pause_timer(self):
        """Triggered when the Pause button is clicked."""
        self.timer.pause()

    def reset_timer(self):
        """Triggered when the Reset button is clicked."""
    #  Pause the timer first just in case it is currently running
        self.timer.pause()
        
    #  Grab the numbers from our UI Spinboxes
        try:
            # We convert the string values to integers
            new_work = int(self.ui.work_var.get())
            new_break = int(self.ui.break_var.get())
        except ValueError:
            # Fallback just in case the user typed letters instead of numbers
            new_work, new_break = 25, 5
            
        # 3. Update the Engine's baseline durations
        # (Assuming your Engine stores work_duration in minutes. If your engine stores 
        # seconds, you will need to multiply these by 60!)
        self.timer.work_duration = new_work * 60
        self.timer.break_duration = new_break * 60
        
        # 4. Reset the engine to apply the new time and update the UI!
        self.timer.reset()
        self.ui.update_display(self.timer.get_formatted_time())

    def update_ui_loop(self):
        """Constantly polls the timer and updates the UI."""
        # Update the clock numbers
        self.ui.update_display(self.timer.get_formatted_time())
        
        # Update the text label
        status_text = "Work Session" if self.timer.current_state == "work" else "Break Time!"
        if not self.timer.is_running:
            status_text += " (Paused)"
        self.ui.status_string.set(status_text)
        
        # AUTO-TRANSITION LOGIC
        # If the clock hits 0, AND the thread has officially stopped:
        if self.timer.time_left == 0 and not self.timer.is_running:
            
            # Swap the states and apply the correct time
            if self.timer.current_state == "work":
                self.timer.current_state = "break"
                self.timer.time_left = self.timer.break_duration
            else:
                self.timer.current_state = "work"
                self.timer.time_left = self.timer.work_duration
                
            # Spawn a fresh thread to start the next phase!
            self.start_timer()

        # Loop again in 100ms
        self.root.after(100, self.update_ui_loop)


if __name__ == "__main__":
    main_window = tk.Tk()
    app = PomodoroController(main_window)
    main_window.mainloop()