import time
import simpleclock


def test_sleep(duration=0.1):
    clock = simpleclock.Clock.started()
    time.sleep(duration)

    assert clock.get_elapsed_since_last_call() >= duration
    assert clock.get_elapsed_since_start() >= duration

    time.sleep(duration)

    assert clock.get_elapsed_since_start() >= 2 * duration
