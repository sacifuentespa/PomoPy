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

        if self.is_running:
            self.is_running = False
            logging.info("Timer paused.")
        else:
            logging.warning("Timer is already paused.")

    def reset(self):
        """Resets the timer back to the original duration based on the current state."""
        if self.current_state == "work":
            self.time_left = self.work_duration
        elif self.current_state == "break":
            self.time_left = self.break_duration
        self.is_running = False
        logging.info(f"The session {self.current_state} was reset!")

    def get_formatted_time(self) -> str:
        """Returns the remaining time in minutes and seconds format."""
        try:
            minutes, seconds = divmod(self.time_left, 60)
            return f"{minutes:02d}:{seconds:02d}"
        except Exception as e:
            logging.error(f"Error formatting time: {e}")
            return "00:00"


if __name__ == "__main__":
    # 1. Create a timer with short durations for testing (1 min work, 1 min break)
    test_timer = PomodoroTimer(work_duration=1, break_duration=1)

    print(f"Initial time: {test_timer.get_formatted_time()}")
    print(f"Initial state: {test_timer.current_state}")

    # 2. Start the timer (we will let it run for just 3 seconds to test)
    import threading

    # We run the timer in a thread just for this test so our script doesn't freeze
    timer_thread = threading.Thread(target=test_timer.start)
    timer_thread.start()

    # Watch it count down for 3 seconds
    for _ in range(3):
        time.sleep(1)
        print(f"Counting down... {test_timer.get_formatted_time()}")

    # 3. Test the pause button
    test_timer.pause()
    print("Paused! Waiting 2 seconds to prove it stopped...")
    time.sleep(2)
    print(f"Time after waiting: {test_timer.get_formatted_time()}")

    # 4. Test the reset button
    test_timer.reset()
    print(f"After reset: {test_timer.get_formatted_time()}")
