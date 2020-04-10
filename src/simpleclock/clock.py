import time


class Clock:
    """
    Simple class for monitoring simple execution time. Relies by default on
    python standard library `time` (using `perf_counter`). Hence works with
    time references (refs) which have no absolute meaning: only diffs matter.
    Keeps a start ref, set with `[re]start[ed]` methods, and to which methods
    `*since_start` refer.

    Clock:
    | get() -> ref
    | get_since(ref) -> delta
    | get_since_start(ref) -> delta
    | print_since(ref, [str], [fmt]) -> delta
    | print_since_start(ref, [str], [fmt]) -> delta

    Example:
    clock = Clock.started()
    ref0 = clock.get()
    # some code 1
    delta_s = clock.get_since_start()  # = <duration1>
    delta_0 = clock.get_since(ref0)    # delta_0 ~ delta_s
    ref = clock.get()
    # some code 2
    clock.print_since(ref, "this first step took")  # "this first step took:
                                                    #  <duration2>s"
    clock.print_since_start()  # "elapsed since start: <~duration1+2>s"
    """

    def __init__(self, default_time_fmt=".2f",
                 default_comment="elapsed",
                 default_comment_start="elapsed since start",
                 timer=time.perf_counter):

        self.default_time_fmt = default_time_fmt
        self.default_comment_start = default_comment_start
        self.default_comment = default_comment
        self._timer = timer

        self._ref_start = None
        self._refs = {
        }

    def start(self, base_time=None):
        self._ref_start = self._timer() if base_time is None else base_time
        return self._ref_start

    def restart(self, base_time=None):
        self._refs = {}
        return self.start(base_time)

    @classmethod
    def started(cls, *args, **kwargs):
        clock = cls(*args, **kwargs)
        clock.start()
        return clock

    def get(self):
        """ return time ref for now"""
        return self._timer()

    def get_since(self, ref):
        return self._timer() - ref

    def get_since_start(self):
        return self.get_since(self._ref_start)

    def print_since(self, ref, comment=None, time_fmt=None):
        if comment is None:
            comment = self.default_comment
        if time_fmt is None:
            time_fmt = self.default_time_fmt
        elapsed = self.get_since(ref)
        print(f"{comment}:", format_time(elapsed, time_fmt))
        return elapsed

    def print_since_start(self, comment=None, time_fmt=None):
        if comment is None:
            comment = self.default_comment_start
        return self.print_since(self._ref_start, comment, time_fmt)


def format_time(t: float, time_fmt) -> str:
    return f"{t:{time_fmt}}s"
