"""
Context managers allow you to easily establish setup and teardown stages.
A context manager implements two methods: __enter__ and __exit__.
We can define context managers using functions as well.
"""
import logging
from contextlib import contextmanager
logging.basicConfig(level=logging.INFO)


class CustomContextManager():
    def __enter__(self):
        logging.info("setup")
        return "context"

    def __exit__(self, exc_type, exc_value, traceback):
        logging.info("teardown")


@contextmanager
def func_context_manager():
    logging.info("setup")
    yield "context"
    logging.info("teardown")


with CustomContextManager() as context:
    logging.info(context)

with func_context_manager() as context:
    logging.info(context)
