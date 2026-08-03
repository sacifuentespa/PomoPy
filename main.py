# main.py
import os
import tkinter as tk
import threading
import subprocess
import platform
from core.timer import PomodoroTimer
from ui.main_window import PomodoroUI


class PomodoroController:
    def __init__(self, root: tk.Tk):
        self.root = root

        # Variable to hold audio
        self.audio_process = None

        # Instantiate the Engine and the Face
        self.timer = PomodoroTimer(work_duration=25, break_duration=5)
        self.ui = PomodoroUI(root)

        # Wire the buttons
        self.ui.start_btn.config(command=self.start_timer)

        self.ui.pause_btn.config(command=self.pause_timer)
        self.ui.reset_btn.config(command=self.reset_timer)

        self.ui.stop_alarm_btn.config(command=self.stop_alarm)
        self.ui.skip_btn.config(command=self.skip_phase)

        #  Start the continuous UI update loop
        self.update_ui_loop()

    def play_alarm(self):
        """Plays a file using the OS's native audio player."""
        os_name = platform.system()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        sound_file = os.path.join(
            current_dir, "assets", "universfield-digital-alarm-clock.wav"
        )

        try:
            if os_name == "Windows":
                import winsound

                winsound.PlaySound(
                    sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC
                )
            elif os_name == "Darwin":
                # Save the process to our leash variable!
                self.audio_process = subprocess.Popen(["afplay", sound_file])
            elif os_name == "Linux":
                # Save the process to our leash variable!
                self.audio_process = subprocess.Popen(["aplay", "-q", sound_file])
        except Exception as e:
            print(f"Failed to play alarm: {e}")

    def stop_alarm(self):
        """Kills the currently playing alarm audio."""
        os_name = platform.system()
        
        if os_name == "Windows":
            # On Windows, passing None to PlaySound stops the current asynchronous sound
            try:
                import winsound
                winsound.PlaySound(None, winsound.SND_ASYNC)
            except Exception:
                pass
        else:
            # On Linux/Mac, we terminate the subprocess if it exists
            if self.audio_process is not None:
                self.audio_process.terminate()
                self.audio_process = None

    def skip_phase(self):
        """Immediately transitions to the next phase without ringing the alarm."""
        
        # Stop the alarm just in case it is currently ringing!
        self.stop_alarm()
        
        # Manually toggle the states
        if self.timer.current_state == "work":
            self.timer.current_state = "break"
            new_time = self.timer.break_duration
        else:
            self.timer.current_state = "work"
            new_time = self.timer.work_duration
            
        # The existing background thread will automatically start counting down from this new number.
        self.timer.time_left = new_time
        
        # Instantly update the UI so it doesn't wait a full second to visually update
        self.ui.update_display(self.timer.get_formatted_time())
        
        # If the timer was paused when they clicked Skip, we need to kickstart it.
        # Otherwise, we do absolutely nothing and let the current thread keep running.
        if not self.timer.is_running:
            self.start_timer()

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
        status_text = (
            "Work Session" if self.timer.current_state == "work" else "Break Time!"
        )
        if not self.timer.is_running:
            status_text += " (Paused)"
        self.ui.status_string.set(status_text)

        # AUTO-TRANSITION LOGIC
        # If the clock hits 0, AND the thread has officially stopped:
        if self.timer.time_left == 0 and not self.timer.is_running:
            # ---> RING THE ALARM <---
            self.play_alarm()

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
