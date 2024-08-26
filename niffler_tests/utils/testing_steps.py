import logging
from contextlib import ContextDecorator

import allure


class Step(ContextDecorator):
    def __init__(self, title):
        self.title = title
        self.allure_step = allure.step(title)

    def __enter__(self):
        self.allure_step.__enter__()
        logging.info(f"Step: {self.title}")

    def __exit__(self, type, value, traceback):
        self.allure_step.__exit__(type, value, traceback)
