import time
import simpleclock


def test_sleep(duration=0.1):
    clock = simpleclock.Clock.started()
    time.sleep(duration)

    assert clock.elapsed_since_last_call() >= duration
    assert clock.elapsed_since_start() >= duration

    time.sleep(duration)

    assert clock.elapsed_since_start() >= 2 * duration


def test_silent_sleep(duration=0.1):
    clock = simpleclock.Clock.started()
    time.sleep(duration)

    assert clock.silent.elapsed_since_start() > duration
    assert clock.silent.elapsed_since_last_call() > duration

    time.sleep(duration)

    assert clock.elapsed_since_last_call() > 2 * duration


def test_get():
    timer_values = iter((1, 2, 3, 4))
    clock = simpleclock.Clock(_timer=lambda: next(timer_values))
    clock.start(base_time=0)

    # .__call__() is defined as .get()
    assert clock.silent.elapsed_since_start() == 1
    assert clock.silent.elapsed_since_last_call() == 2
    assert clock.elapsed_since_start() == 3
    assert clock.elapsed_since_last_call() == 1


def test_print(capsys):
    timer_values = iter((0, 0, 2.82, 10))
    clock = simpleclock.Clock(_timer=lambda: next(timer_values), default_rounding_precision=0)
    clock.start()
    clock.elapsed_since_start()

    clock.elapsed_since_last_call.print("Test", rounding_precision=2)
    assert capsys.readouterr().out == "Test: 2.82s" + "\n"

    clock.elapsed_since_last_call.print("Another test")
    assert capsys.readouterr().out == "Another test: 7s" + "\n"


def test_default_comment(capsys):
    clock = simpleclock.Clock(_timer=lambda: 5, default_comment_start="it has been running for")
    clock.start(base_time=0)
    clock.elapsed_since_start.print()
    assert capsys.readouterr().out == "it has been running for: 5.00s" + "\n"
