import time
import logging

logger = logging.getLogger("SimpleClock")


class TimeStamp:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


def ts():
    return TimeStamp(time.perf_counter())


class Reader:
    def __init__(self, duration: float, rounding_precision: int, logger=logger):
        self.duration = duration
        self.rounding_precision = rounding_precision
        self.logger = logger

    def print(self, text: str = "") -> TimeStamp:
        if text:
            print(f"{text}: {self.duration:.2f}s")
        print(f"{self.duration:.2f}s")
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
    def __init__(self, rounding_precision=2):
        self.rounding_precision = rounding_precision

    def __call__(self, ts: TimeStamp) -> Reader:
        return Reader(
            time.perf_counter() - ts.value,
            self.rounding_precision
        )
