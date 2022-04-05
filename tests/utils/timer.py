import sys
import time
import logging


# =========== configs for logs ===========

# This is intended for the testing environment.

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    " [%(asctime)s:%(name)s:%(levelname)s] %(message)s"
)

handler.setFormatter(formatter)
logger.addHandler(handler)

# ========================================


class Timer:

    from colorama import Fore, init

    init(autoreset=True)

    r = Fore.RED
    g = Fore.GREEN
    w = Fore.RESET
    y = Fore.YELLOW

    def __init__(self, msg=""):
        self.msg = msg
        self.start = 0
        self.total = 0


    def __enter__(self):
        self.start = time.perf_counter()

        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.total = time.perf_counter() - self.start

        if self.total >= 3:
            self.level = self.r
        elif self.total >= 1:
            self.level = self.y
        else:
            self.level = self.g

        logger.info(self)


    def __str__(self):
        test_info_log = f"[{self.level}{self.msg}{self.w}]"
        test_time_spent = f"Time spent - {round(self.total, 5)} s"

        return f"{test_info_log} {test_time_spent}"
