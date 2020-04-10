import time
import simpleclock


def test_sleep(duration=0.1):
    clock = simpleclock.Clock.started()
    ref = clock.get()
    time.sleep(duration)

    assert clock.get_since(ref) >= duration
    assert clock.get_since_start() >= duration

    time.sleep(duration)

    assert clock.get_since_start() >= 2 * duration


def test_get(duration=0.1):
    clock = simpleclock.Clock.started()
    time.sleep(duration)

    ref = clock.get()
    assert clock.get_since_start() > clock.get_since(ref)


def test_get_since():
    def cnst():
        return cnst.value
    cnst.value = 0
    clock = simpleclock.Clock(timer=cnst)
    clock.start()
    ref0 = clock.get()

    # .__call__() is defined as .get()
    cnst.value += 1
    assert clock.get_since_start() == 1
    cnst.value += 1
    assert clock.get_since(ref0) == 2
    cnst.value += 1
    assert clock.get_since_start() == 3
    ref1 = clock.get()
    cnst.value += 1
    assert clock.get_since(ref1) == 1


def test_print(capsys):
    timer_values = iter((0, 2.82, 10, 10))
    clock = simpleclock.Clock(timer=lambda: next(timer_values),
                              default_time_fmt=".0f")
    ref0 = clock.start()

    clock.print_since(ref0, "Test", time_fmt=".2f")
    assert capsys.readouterr().out == "Test: 2.82s" + "\n"

    ref1 = 2.83

    clock.print_since(ref1, "Another test")
    assert capsys.readouterr().out == "Another test: 7s" + "\n"


def test_default_comment(capsys):
    clock = simpleclock.Clock(timer=lambda: 5,
                              default_comment_start="it has been running for")
    clock.start(base_time=0)
    clock.print_since_start()
    assert capsys.readouterr().out == "it has been running for: 5.00s" + "\n"
