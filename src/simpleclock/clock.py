import time


class Clock:
    """
    Simple class for monitoring execution time. Relies on python standard library time (using .perf_counter).
    attr:
    -- elapsed_since_start, elapsed_since_last_call: Reader objects, yieling methods: get, print, call. (
    "since_last_call" means since last non silent method call)
    -- silent: TimeReader pair (elapsed_since_start, elapsed_since_last_call) yielding silent versions of TimeReader
    methods.
    TimeReader methods:
        get, print: get/print elapsed time. TimeReader.__call__ bound to TimeReader.get
        call: reset elapsed_since_last_call

    Example:
        clock = Clock.started()
        # some code 1
        clock.elapsed_since_start.print()  # "elapsed since start: <duration1>s"
        # some code 2
        clock.silent.elapsed_since_last_call.print("some code 2 took")  # "some code 2 took: <duration2>s"
        # some code 3
        clock.elapsed_since_last_call.get()  # ~ duration2 + duration3
        clock.elapsed_since_last_call.get()  # ~ 0
                                             # clock.elapsed_since_last_call() would work too
    """

    def __init__(self, default_rounding_precision=2, _timer=time.perf_counter,
                 default_comment_last_call="elapsed since last call", default_comment_start="elapsed since start"):
        self._timer = _timer
        self.default_rounding_precision = default_rounding_precision
        self.default_comment_start = default_comment_start
        self.default_comment_last_call = default_comment_last_call

        self._times = {
            "init": None,
            "last": None
        }
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
        self.elapsed_since_start = UpdatingReader(self, "init", self.default_comment_start)
        self.elapsed_since_last_call = UpdatingReader(self, "last", self.default_comment_last_call)
        self.silent = ReaderPair(SilentReader(self, "init", self.default_comment_start),
                                 SilentReader(self, "last", self.default_comment_last_call))

    def restart(self, base_time=None):
        self._times["init"] = self._timer() if base_time is None else base_time
        self._times["last"] = self._times["init"]


class TImeReader:
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

    def __call__(self):
        return self.get()


class UpdatingReader(TImeReader):

    def call(self):
        self._update(self.clock._timer())

    def get(self):
        now = self.clock._timer()
        elapsed = self._get(now)
        self._update(now)
        return elapsed


class SilentReader(TImeReader):
    def get(self):
        return self._get(self.clock._timer())


class ReaderPair:
    def __init__(self, since_start, since_last_call):
        self.elapsed_since_start: TImeReader = since_start
        self.elapsed_since_last_call: TImeReader = since_last_call


def format_time(t: float, rounding_precision) -> str:
    return f"{t:.{rounding_precision}f}s"


def print_comment(elapsed, comment, rounding_precision):
    print(f"{comment}:", format_time(elapsed, rounding_precision))
