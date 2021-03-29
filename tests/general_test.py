import time
import simpleclock as sc


def test_sleep(duration=0.1):
    since = sc.Since()
    ts = sc.ts()

    time.sleep(duration)

    assert since(ts).duration >= duration

    time.sleep(duration)

    assert since(ts).duration >= 2 * duration


def test_print(capsys):
    since = sc.Since(precision=0)
    ts = sc.ts("start")

    time.sleep(0.01)

    since(ts).print()
    assert capsys.readouterr().out == "start: 0s\n"

    time.sleep(.5)

    since(ts).print("and now")
    assert capsys.readouterr().out == "and now: 1s\n"
