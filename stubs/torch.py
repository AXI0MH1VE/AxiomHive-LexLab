"""Tiny shim of the parts of torch used in unit tests.

Implements a minimal `rand` function and a Tensor wrapper around nested lists.
"""
import random

class Tensor(list):
    def numpy(self):
        return self

def rand(*shape):
    # produce a nested list of floats matching shape (support 1D and 2D simple cases)
    if len(shape) == 2:
        return Tensor([[random.random() for _ in range(shape[1])] for _ in range(shape[0])])
    if len(shape) == 1:
        return Tensor([random.random() for _ in range(shape[0])])
    return Tensor([random.random()])

def tensor(data):
    return Tensor(data)

def manual_seed(s):
    random.seed(s)
