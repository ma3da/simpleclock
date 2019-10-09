import time
import simpleclock


def test_sleep(duration=0.1):
    clock = simpleclock.Clock.started()
    time.sleep(duration)

    assert clock.elapsed_since_last_call.get() >= duration
    assert clock.elapsed_since_start.get() >= duration

    time.sleep(duration)

    assert clock.elapsed_since_start.get() >= 2 * duration


def test_silent_sleep(duration=0.1):
    clock = simpleclock.Clock.started()
    time.sleep(duration)

    assert clock.silent.elapsed_since_start.get() > duration
    assert clock.silent.elapsed_since_last_call.get() > duration

    time.sleep(duration)

    assert clock.elapsed_since_last_call.get() > 2 * duration


def test_get():
    timer_values = iter((1, 2, 3, 4))
    clock = simpleclock.Clock(_timer=lambda: next(timer_values))
    clock.start(base_time=0)

    assert clock.silent.elapsed_since_start.get() == 1
    assert clock.silent.elapsed_since_last_call.get() == 2
    assert clock.elapsed_since_start.get() == 3
    assert clock.elapsed_since_last_call.get() == 1


def test_print(capsys):
    timer_values = iter((0, 0, 2.82, 10))
    clock = simpleclock.Clock(_timer=lambda: next(timer_values), default_rounding_precision=0)
    clock.start()
    clock.elapsed_since_start.get()

    clock.elapsed_since_last_call.print("Test", rounding_precision=2)
    assert capsys.readouterr().out == "Test: 2.82s" + "\n"

    clock.elapsed_since_last_call.print("Another test")
    assert capsys.readouterr().out == "Another test: 7s" + "\n"
