import numpy
from numpy import arange
from numpy import exp
from numpy.random import randint

def exp_array(s, n):
    return arange(s, n, 0.01), exp(arange(s, n, 0.01))

def test_array():
    x = arange(0, 5, 0.01)
    y = x* (x - 1) * (x - 2) * (x - 4) * (x - 5)

    return x, y


def add_noise(ary):
    length = len(ary)
    noise = randint(-100, 100, length)/10000

    return ary + noise
