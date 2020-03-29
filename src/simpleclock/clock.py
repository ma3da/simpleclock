import time
import collections

ReadersTuple = collections.namedtuple("ReadersTuple", [
    "elapsed_since_start",
    "elapsed_since_last_call",
])


class Clock:
    """
    Simple class for monitoring execution time. Relies on python standard library time (using .perf_counter).
    attr:
    -- elapsed_since_start, elapsed_since_last_call: Reader objects, yieling methods: get, print, call. (
    "since_last_call" means since last non silent method call)
    -- silent: ReadersTuple yielding silent versions of DurationReader
    methods.
    DurationReader methods:
        get, print: get/print elapsed time. DurationReader.__call__ bound to DurationReader.get
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

    def __init__(self, default_rounding_precision=2,
                 default_comment_last_call="elapsed since last call",
                 default_comment_start="elapsed since start",
                 timer=time.perf_counter):
        self.default_rounding_precision = default_rounding_precision
        self.default_comment_start = default_comment_start
        self.default_comment_last_call = default_comment_last_call
        self._timer = timer

        self._times = {
            "init": None,
            "last": None
        }

        # declaring for autocompletion
        self.elapsed_since_start: DurationReader = None
        self.elapsed_since_last_call: DurationReader = None
        self.silent: ReadersTuple = None

    def _now(self):
        return self._timer()

    def call(self):
        self._times["last"] = self._now()

    def start(self, base_time=None):
        self._times["init"] = self._timer() if base_time is None else base_time
        self._times["last"] = self._times["init"]

        def duration_getter_no_update(begin_mark):
            def _getter():
                return self._now() - self._times[begin_mark]
            return _getter

        def duration_getter_with_update(begin_mark):
            def _getter():
                now = self._now()
                elapsed = now - self._times[begin_mark]
                self._times["last"] = now
                return elapsed
            return _getter

        def readers(reader, duration_getter):
            return ReadersTuple(
                elapsed_since_start=reader(
                    duration_getter("init"),
                    self.default_comment_start,
                    self.default_rounding_precision),
                elapsed_since_last_call=reader(
                    duration_getter("last"),
                    self.default_comment_last_call,
                    self.default_rounding_precision)
            )

        self.default = readers(DurationReader, duration_getter_with_update)
        self.silent = readers(DurationReader, duration_getter_no_update)
        
        # binding to default
        self.elapsed_since_start = self.default.elapsed_since_start
        self.elapsed_since_last_call = self.default.elapsed_since_last_call

    def restart(self, base_time=None):
        self._times["init"] = self._timer() if base_time is None else base_time
        self._times["last"] = self._times["init"]

    @classmethod
    def started(cls, *args, **kwargs):
        clock = cls(*args, **kwargs)
        clock.start()
        return clock


class DurationReader:
    def __init__(self, get, default_comment, default_rounding_precision):
        self.get = get
        self.default_comment = default_comment
        self.default_rounding_precision = default_rounding_precision

    def print(self, comment=None, rounding_precision=None):
        elapsed = self.get()
        print_comment(elapsed,
                      self.default_comment if comment is None else comment,
                      self.default_rounding_precision if rounding_precision is None else rounding_precision)
        return elapsed

    def __call__(self):
        return self.get()


def format_time(t: float, rounding_precision) -> str:
    return f"{t:.{rounding_precision}f}s"


def print_comment(elapsed, comment, rounding_precision):
    print(f"{comment}:", format_time(elapsed, rounding_precision))
