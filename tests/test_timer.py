import time
import threading
from core.timer import PomodoroTimer


def test_timer_pause_and_reset():
    """Test the pause and reset state controls."""
    timer = PomodoroTimer(work_duration=25, break_duration=5)

    # Simulate starting the timer by manually flipping the boolean
    timer.is_running = True
    timer.time_left = 1000  # Let's pretend 500 seconds have passed

    # pause test
    timer.pause()

    # Then write an assert statement to verify timer.is_running is False!
    assert timer.is_running is False

    # reset test

    timer.reset()

    assert timer.is_running is False
    assert timer.time_left == 1500


def test_timer_start():
    """Test that the start method actively counts down in a thread."""
    # 1 minute work duration = 60 seconds
    timer = PomodoroTimer(work_duration=1, break_duration=1)

    # Background thread so pytest doesn't freeze
    timer_thread = threading.Thread(target=timer.start)
    timer_thread.start()

    # 2. Let it run for 2 seconds
    time.sleep(2)

    # 3. Assertions: It should be running, and time should have decreased!
    assert timer.is_running is True
    assert timer.time_left < 60  # Should be around 58 seconds now

    # Pause the timer so the background thread dies cleanly!
    timer.pause()
    assert timer.is_running is False

    # Checking resuming the timer
    resume_thread = threading.Thread(target=timer.start)
    resume_thread.start()

    for _ in range(6):
        time.sleep(1)

    assert timer.is_running is True
    assert timer.time_left < 55

    timer.pause()
    assert timer.is_running is False
