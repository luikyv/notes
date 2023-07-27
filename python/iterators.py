"""
Iterable objects implement the __iter__ method which is reponsible for returning an iterator.
An iterator in turn is an object that holds the information on how to perform iterations.
An iterator implements two methods: __iter__ and __next__ where __iter__ usually returns the iterator itself.
Behind the scenes, for loops use __iter__ to get the iterator and __next__ to perform the iterations
"""
from typing import Iterator


class FibonacciSequence():
    """Fibonacci sequence iterator"""

    def __init__(self, stop: int) -> None:
        self._stop = stop
        self._index = 0
        self._current = 0
        self._next = 1

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> int:

        if self._index >= self._stop:
            raise StopIteration

        self._index += 1
        fib_number = self._current
        self._current, self._next = (
            self._next,
            self._current + self._next,
        )
        return fib_number


fib_seq = FibonacciSequence(stop=10)
for fib_number in fib_seq:
    print(fib_number)
