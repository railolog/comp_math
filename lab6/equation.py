import math

from prettytable import PrettyTable


class Equation:
    def __init__(self, f, view):
        self.f = f
        self.view = view

    def __str__(self):
        return self.view


class ConcreteEquation:
    def __init__(self, eq: Equation, y0, x0, xn, h, eps):
        self.f = eq.f
        self.view = eq.view
        self.y0 = y0
        self.x0 = x0
        self.xn = xn
        self.h = h
        self.eps = eps

    def eulerIter(self, x, y, h):
        newY = y + h * self.f(x, y)
        return newY

    def rungeIter(self, x, y, h):
        f = self.f

        k1 = h * f(x, y)
        k2 = h * f(x + h/2, y + k1/2)
        k3 = h * f(x + h/2, y + k2/2)
        k4 = h * f(x + h, y + k3)

        return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6

    def simpleIntegrals(self):
        X = [self.x0]
        Y = [self.y0]
        euler = [self.y0]
        runge = [self.y0]

        x = self.x0
        while x < self.xn:
            X.append(x)
            euler.append(self.eulerIter(x, euler[-1], self.h))
            runge.append(self.rungeIter(x, runge[-1], self.h))
            x += self.h

        X.append(x)

        return X, euler, runge

    def rungeRuledIntegrals(self):
        X = [self.x0]
        Y = [self.y0]
        euler = [self.y0]
        runge = [self.y0]

        x = self.x0
        while x < self.xn:
            y1 = self.eulerIter(x, euler[-1], self.h)

