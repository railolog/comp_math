from typing import Callable, List, Tuple, Union, Any
import numpy as np
import sympy
from math import *
import matplotlib.pyplot as plt

ITERATIONS = 10 ** 5
PRECISE = 10**(-3)


class Equation:
    def __init__(self, f: Callable[[float], float], df: Callable[[float], float], d2f: Callable[[float], float], view: str):
        self.f = f
        self.df = df
        self.d2f = d2f
        self.view = view

    def __str__(self):
        return self.view

    def graph(self):
        x = np.arange(-10, 10, 0.01)
        plt.plot(x, np.vectorize(self.f)(x))
        plt.grid(True)
        plt.ylim(-10, 10)
        plt.show(block=False)


class EquationSystem:
    def __init__(self,
                 f: Callable[[float, float], float],
                 g: Callable[[float, float], float],
                 dfdx: Callable[[float, float], float],
                 dfdy: Callable[[float, float], float],
                 dgdx: Callable[[float, float], float],
                 dgdy: Callable[[float, float], float],
                 f_view: str,
                 g_view: str,
                 symf: str,
                 symg: str):
        self.first = f
        self.second = g
        self.dfdx = dfdx
        self.dfdy = dfdy
        self.dgdx = dgdx
        self.dgdy = dgdy
        self.view = f_view + '\n' + g_view
        self.symf = symf
        self.symg = symg

    def __str__(self):
        return self.view

    def graph(self):
        sympy.var('x y')
        p1 = sympy.plot_implicit(sympy.Eq(eval(self.symf), 0), show=False, block=False)
        p2 = sympy.plot_implicit(sympy.Eq(eval(self.symg), 0), show=False)
        p1.append(p2[0])
        p1.show()


class IntervaledEquation:
    def __init__(self, equation: Equation, a: float, b: float):
        if a == b:
            raise ValueError('Длина интервала изоляции должна быть больше 0')

        self.eq = equation
        self.a = min(a, b)
        self.b = max(a, b)
        self.necessary_cond = False
        self.intervals = self.find_intervals()
        self.valid = self.validate()

    def find_intervals(self) -> List[Tuple[float, Union[float, Any]]]:
        res = []

        eps = (self.b - self.a) / ITERATIONS
        eps = max(eps, PRECISE)
        f = self.eq.f
        xi = self.a
        for i in range(round((self.b - self.a) / eps)):
            if f(xi) * f(xi + eps) < 0:
                res.append((xi, xi + eps))
            xi += eps

        return res

    def keeps_sign_derivative(self) -> bool:
        def sign(a):
            if a > 0:
                return 1
            elif a < 0:
                return -1
            else:
                return 0

        df = self.eq.df
        first = sign(df(self.a))

        eps = (self.b - self.a) / ITERATIONS
        xi = self.a
        for i in range(ITERATIONS):
            if sign(df(xi)) != first:
                return False
            xi += eps

        return True

    def validate(self) -> bool:
        f = self.eq.f
        if f(self.a) * f(self.b) < 0:
            self.necessary_cond = True
        return self.necessary_cond and len(self.intervals) == 1

    def graph(self):
        x = np.arange(self.a, self.b, (self.b - self.a) / 1000)
        plt.plot(x, np.vectorize(self.eq.f)(x))
        plt.grid(True)
        plt.ylim(-10, 10)
        plt.show(block=False)
