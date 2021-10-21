# simple_calculator.py
class SimpleCalculator:
    """
    This class creates a simple calculator that is able to add and subtract 2 numbers.
    This class has an attribute of Euler's number: e.
    """
    def __init__(self):
        self.e = 2.71828182846
    def __repr__(self):
        return "A Simple Calculator Class."
    def add(self, x, y):
        return x + y
    def subtract(self, x, y):
        return x - y
    def exp(self, n):
        return self.e**n