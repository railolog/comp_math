import math
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable


def findClosest(X, x):
    ans = 0
    for i in range(len(X)):
        if x > X[i]:
            ans = i
    return ans


class Solver:
    def __init__(self, X, Y, x):
        self.X = X
        self.Y = Y
        self.x = x
        self.dy = self.getDiff()
        self.closest = findClosest(X, x)
        self.newtonF = self.newton()

    def getDiff(self):
        n = len(self.Y)
        dy = [[self.Y[i]] for i in range(n)]

        for i in range(1, n):
            for j in range(n - i):
                dy[j].append(dy[j + 1][i - 1] - dy[j][i - 1])

        return dy

    def diffTable(self):
        table = PrettyTable()

        fields = ['x_i', 'y_i', '∆y_i']
        for i in range(2, len(self.X)):
            fields.append(f'∆^{i}y_i')

        table.field_names = fields

        dy = [[round(k, 4) for k in i] + [' ' for j in range(len(self.dy) - len(i))] for i in self.dy]

        for i in range(len(self.X)):
            dy[i].insert(0, round(self.X[i], 4))

        table.add_rows(dy)

        return table

    def lagrange(self):
        X = self.X
        x = self.x
        Y = self.Y

        def l(num):
            res = 1

            for j in range(len(X)):
                if j != num:
                    res *= x - X[j]
                    res /= X[num] - X[j]

            return res

        L = 0
        for i in range(len(X)):
            L += Y[i] * l(i)

        return L

    def newtonForward(self, x):
        def T(c):
            resT = 1
            for j in range(c):
                resT *= t - j
            resT /= math.factorial(c)
            return resT

        res = 0
        t = (x - self.X[self.closest]) / (self.X[1] - self.X[0])

        for i in range(len(self.X) - self.closest):
            res += T(i) * self.dy[self.closest][i]

        return res

    def newtonBackward(self, x):
        def T(c):
            res = 1
            for i in range(c):
                res *= t + i
            res /= math.factorial(c)
            return res

        res = 0
        t = (x - self.X[-1]) / (self.X[1] - self.X[0])

        n = len(self.X)
        for i in range(n):
            res += T(i) * self.dy[n - i - 1][i]

        return res

    def newton(self):
        x = self.x
        X = self.X

        if abs(x - X[0]) > abs(x - X[-1]):
            return self.newtonBackward
        return self.newtonForward

    def graph(self):
        X = self.X

        plt.plot(X, self.Y, 'ko')
        x = np.linspace(min(X + [self.x]), max(X + [self.x]), 100)
        plt.plot(x, np.vectorize(self.newtonF)(x))
        plt.show()
