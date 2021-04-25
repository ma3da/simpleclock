import time


class TimeStamp:
    def __init__(self, value, name):
        self.value = value
        self.name = name

    def __repr__(self):
        return f"<TimeStamp: {self.name}>"


def ts(name="Unnamed"):
    return TimeStamp(time.perf_counter(), name)


class Reader:
    def __init__(self, duration: float, ts_name: str, precision: int, logger=None):
        self.duration = duration
        self.ts_name = ts_name
        self.text_default = ts_name
        self.logger = logger
        self.rnd_fmt = f".{precision}f"

    def format(self, text: str = "") -> str:
        if text:
            return f"{text}: {self.duration:{self.rnd_fmt}}s"
        else:
            return f"{self.text_default}: {self.duration:{self.rnd_fmt}}s"

    def print(self, text: str = "") -> TimeStamp:
        print(self.format(text))
        return ts()

    def debug(self, text: str = "") -> TimeStamp:
        self.logger.debug(self.format(text))
        return ts()

    def info(self, text: str = "") -> TimeStamp:
        self.logger.info(self.format(text))
        return ts()

    def warning(self, text: str = "") -> TimeStamp:
        self.logger.warning(self.format(text))
        return ts()

    def error(self, text: str = "") -> TimeStamp:
        self.logger.error(self.format(text))
        return ts()


class Since:
    def __init__(self, precision: int = 2, logger=None):
        try:
            self.precision = int(precision)
        except ValueError:
            raise ValueError(f"precision expects an int, unlike: {precision}")
        self.logger = logger

    def __call__(self, ts: TimeStamp) -> Reader:
        return Reader(
            time.perf_counter() - ts.value,
            ts.name,
            self.precision,
            self.logger
        )
