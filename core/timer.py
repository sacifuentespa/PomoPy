# core/timer.py
import time
import logging

# Basic logging setup to help us debug without printing everything to the console
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class PomodoroTimer:
    def __init__(
        self, work_duration: int = 25, break_duration: int = 5, on_complete=None
    ):
        """
        Initialize the timer with default durations in minutes.
        """
        self.work_duration = work_duration * 60  # Convert to seconds
        self.break_duration = break_duration * 60
        self.time_left = self.work_duration
        self.is_running = False

        # We can track the state: 'work' or 'break'
        self.current_state = "work"

        # Hold a function triggered when the timer hits zero
        self.on_complete = on_complete

    def start(self):
        """Starts or resumes the countdown."""
        if self.is_running:
            logging.warning("Timer is already running.")
            return

        self.is_running = True
        logging.info("Timer started.")

        while self.is_running and self.time_left > 0:
            time.sleep(1)
            self.time_left -= 1
            # print(f"Time left: {self.time_left} seconds")

        if self.time_left <= 0:
            self.is_running = False
            logging.info(f"The session {self.current_state} is complete!")
            # Swap the state and reset the timer for the next phase
            if self.current_state == "work":
                self.current_state = "break"
                self.time_left = self.break_duration
            else:
                self.current_state = "work"
                self.time_left = self.work_duration

            # 2. Trigger the callback so the main app can ring the alarm!
            if self.on_complete:
                self.on_complete()

    def pause(self):
        """Pauses the timer."""
        # TODO: Implement the logic to stop the countdown loop.
        pass

    def reset(self):
        """Resets the timer back to the original duration based on the current state."""
        # TODO: Implement logic to stop the timer and reset self.time_left.
        pass

    def get_formatted_time(self) -> str:
        """Returns the remaining time in MM:SS format."""
        try:
            # TODO: Convert self.time_left (which is in seconds) into minutes and seconds.
            # Return it as a formatted string, e.g., "25:00".
            return "00:00"  # Placeholder
        except Exception as e:
            logging.error(f"Error formatting time: {e}")
            return "00:00"
