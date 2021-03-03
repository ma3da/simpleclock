import time


class TimeStamp:
    def __init__(self, value, name):
        self.value = value
        self.name = name

    def __repr__(self):
        return str(self.value)


def ts(name="Unnamed"):
    return TimeStamp(time.perf_counter(), name)


class Reader:
    def __init__(self, duration: float, ts_name: str, rounding_precision: int, logger=None):
        self.duration = duration
        self.ts_name = ts_name
        self.text_default = ts_name
        self.rounding_precision = rounding_precision
        self.logger = logger

    def print(self, text: str = "") -> TimeStamp:
        if text:
            print(f"{text}: {self.duration:.2f}s")
        else:
            print(f"{self.text_default}: {self.duration:.2f}s")
        return ts()

    def debug(self) -> TimeStamp:
        self.logger.debug(f"{self.duration:.2f}s")
        return ts()

    def info(self) -> TimeStamp:
        self.logger.info(f"{self.duration:.2f}s")
        return ts()

    def warning(self) -> TimeStamp:
        self.logger.warning(f"{self.duration:.2f}s")
        return ts()

    def error(self) -> TimeStamp:
        self.logger.error(f"{self.duration:.2f}s")
        return ts()


class Since:
    def __init__(self, rounding_precision=2, logger=None):
        self.rounding_precision = rounding_precision
        self.logger = logger

    def __call__(self, ts: TimeStamp) -> Reader:
        return Reader(
            time.perf_counter() - ts.value,
            ts.name,
            self.rounding_precision,
            self.logger
        )
