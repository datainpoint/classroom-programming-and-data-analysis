# simple_calculator.py
class SimpleCalculator:
    """
    This class creates a simple calculator that is able to add, subtract, multiply, and divide 2 numbers.
    This class has an attribute of Euler's number: e.
    """
    def __init__(self):
        self.e = 2.71828182846
    def add(self, x, y):
        return x + y
    def subtract(self, x, y):
        return x - y
    def multiply(self, x, y):
        return x * y
    def divide(self, x, y):
        return x / y