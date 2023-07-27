"""
Generator functions return a special iterator called generator. It is special because,
it implements other useful methods such as .send, .throw and .close.
We can create generator functions by using the yield statement.
When the execution arrives at the yield statement, the function is stopped and its state is saved.
The return statement stops the iteration by raising the StopIteration exception.
"""
from typing import Generator


def generator_function() -> Generator:
    yield "first string"
    yield "second string"
    yield "third string"


for s in generator_function():
    print(s)
