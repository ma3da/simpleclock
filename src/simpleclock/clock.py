import time

default_comment_last_call = "elapsed since last call"
default_comment_start = "elapsed since start"


class Clock:
    """
    Simple class for monitoring execution time. Relies on python standard library time (using .perf_counter).
    times: elapsed_since_start and elapsed_since_last_call, call meaning one of the following functions call (or start
    of the clock)
    functions:
        get, print: get/print elapsed time
        call: silent method to reset elapsed_since_last_call
    the silent version of a function does not trigger a call (i.e. does not reset elapsed_since_last_call)
    """

    def __init__(self, default_rounding_precision=2, _timer=time.perf_counter):
        self._timer = _timer
        self._times = {
            "init": None,
            "last": None
        }
        self.default_rounding_precision = default_rounding_precision
        self.elapsed_since_start: UpdatingReader = None
        self.elapsed_since_last_call: UpdatingReader = None
        self.silent: ReaderPair = None

    @classmethod
    def started(cls, default_rounding_precision=2):
        clock = cls(default_rounding_precision)
        clock.start()
        return clock

    def start(self, base_time=None):
        self._times["init"] = self._timer() if base_time is None else base_time
        self._times["last"] = self._times["init"]
        self.elapsed_since_start = UpdatingReader(self, "init", default_comment_start)
        self.elapsed_since_last_call = UpdatingReader(self, "last", default_comment_last_call)
        self.silent = ReaderPair(SilentReader(self, "init", default_comment_start),
                                 SilentReader(self, "last", default_comment_last_call))

    def restart(self, base_time=None):
        self._times["init"] = self._timer() if base_time is None else base_time
        self._times["last"] = self._times["init"]


class BaseReader:
    def __init__(self, clock, ref_target, default_comment):
        self.clock = clock
        self.ref_target = ref_target
        self.default_comment = default_comment

    def _update(self, now):
        self.clock._times["last"] = now

    def _get(self, now):
        return now - self.clock._times[self.ref_target]

    def get(self):
        raise NotImplementedError

    def _print_since(self, elapsed, comment, rounding_precision):
        print_comment(elapsed,
                      self.default_comment if comment is None else comment,
                      self.clock.default_rounding_precision if rounding_precision is None else rounding_precision)
        return elapsed

    def print(self, comment=None, rounding_precision=None) -> float:
        return self._print_since(self.get(), comment, rounding_precision)


class UpdatingReader(BaseReader):

    def call(self):
        self._update(self.clock._timer())

    def get(self):
        now = self.clock._timer()
        elapsed = self._get(now)
        self._update(now)
        return elapsed


class SilentReader(BaseReader):
    def get(self):
        return self._get(self.clock._timer())


class ReaderPair:
    def __init__(self, since_start, since_last_call):
        self.elapsed_since_start: BaseReader = since_start
        self.elapsed_since_last_call: BaseReader = since_last_call


def format_time(t: float, rounding_precision) -> str:
    return f"{t:.{rounding_precision}f}s"


def print_comment(elapsed, comment, rounding_precision):
    print(f"{comment}:", format_time(elapsed, rounding_precision))
