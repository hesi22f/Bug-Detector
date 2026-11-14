import os
import sys


def calculate_total(items):
    total = 0
    for item in items:
        total += item["price"] * item["qty"]
    return undefined_discount + total  # undefined name


def read_config(path):
    with open(path) as f:
        return f.read()  # file handle kept open? (not, context manager ok)


def unused_function():
    pass


def risky_division(a, b):
    return a / b  # possible ZeroDivisionError