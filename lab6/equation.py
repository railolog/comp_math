import math

from prettytable import PrettyTable


class Equation:
    def __init__(self, f, I, C, view):
        self.f = f
        self.I = I
        self.view = view
        self.C = C

    def __str__(self):
        return self.view


class ConcreteEquation:
    def __init__(self, eq: Equation, y0, x0, xn, h, eps):
        self.f = eq.f
        self.view = eq.view
        self.I = eq.I
        self.C = eq.C(x0, y0)
        self.y0 = y0
        self.x0 = x0
        self.xn = xn
        self.h = h
        self.eps = eps

        self.eulerY = []
        self.rungeY = []

        # print(self.C)

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
            euler.append(self.eulerIter2(x, euler[-1], self.h))
            runge.append(self.rungeIter(x, runge[-1], self.h))
            x += self.h

        X.append(x)

        return X, euler, runge

    def eulerIter2(self, x0, x1, y, h):
        n = (x1 - x0) / h
        yi = y

        xi = x0
        for i in range(int(n)):
            yi = yi + h * self.f(xi, yi)
            xi += h

        return yi

    def rungeRuledEuler(self):
        h = self.h
        hi = h
        Y = [self.y0]

        n = (self.xn - self.x0) / h
        xi = self.x0

        for i in range(int(n)):
            y1 = self.eulerIter2(xi, xi + h, Y[-1], hi)
            y2 = self.eulerIter2(xi, xi + h, Y[-1], hi/2)

            R = abs(y1 - y2)
            while R > self.eps:
                y1 = y2
                hi /= 2
                y2 = self.eulerIter2(xi, xi + h, Y[-1], hi/2)

                R = abs(y1 - y2)

                if int(h / (hi / 2)) > 200000:
                    # print(int(h / (hi / 2)))
                    hi *= 2
                    break

            xi += h
            Y.append(y2)

        self.eulerY = Y
        return Y

    def rungeIter2(self, x0, x1, y, h):
        f = self.f

        n = (x1 - x0) / h
        yi = y

        xi = x0
        for i in range(int(n)):
            k1 = f(xi, yi)
            k2 = f(xi + h / 2, yi + h * k1 / 2)
            k3 = f(xi + h / 2, yi + h * k2 / 2)
            k4 = f(xi + h, yi + h * k3)

            yi = yi + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
            xi += h

        return yi

    def rungeRuledRunge(self):
        h = self.h
        hi = h
        Y = [self.y0]

        n = (self.xn - self.x0) / h
        xi = self.x0

        for i in range(int(n)):
            y1 = self.rungeIter2(xi, xi + h, Y[-1], hi)
            y2 = self.rungeIter2(xi, xi + h, Y[-1], hi / 2)

            R = abs(y1 - y2)
            if hi > 1:
                hi = 1
            while R > self.eps:
                y1 = y2
                hi /= 2
                y2 = self.rungeIter2(xi, xi + h, Y[-1], hi / 2)

                R = abs(y1 - y2)

                if int(h / (hi / 2)) > 50000:
                    # print(int(h / (hi / 2)))
                    hi *= 2
                    break

            xi += h
            Y.append(y2)

        self.rungeY = Y
        return Y

    def miln(self):
        f = self.f
        h = self.h
        n = int((self.xn - self.x0) / h)

        if n < 4:
            return self.rungeY

        x0 = self.x0
        Y = self.rungeY[:4]
        X = [x0, x0 + h, x0 + 2*h, x0 + 3*h]
        xi = self.x0 + 3*h
        stop = False
        for i in range(3, n):
            yi = Y[-4] + (2 * f(X[-3], Y[-3]) - f(X[-2], Y[-2]) + 2 * f(X[-1], Y[-1])) * 4*h / 3
            yic = yi

            X.append(X[-1] + h)
            if stop:
                continue

            exact = self.I(X[-1], self.C)
            while abs(yic - exact) > self.eps:
                # print(X[-1], yic)
                fi = f(X[-1], yic)
                yi = Y[-2] + (f(X[-3], Y[-2]) + 4 * f(X[-2], Y[-1]) + fi) * h / 3

                if abs(yi - yic) > 1000:
                    print('Выбраны неподходящие шаг и/или интервал. Метод Милна расходится')
                    stop = True
                    break

                if abs(yi - yic) <= self.eps:
                    yic = yi
                    break

                yic = yi

            Y.append(yic)

        while len(Y) < len(X):
            Y.append('NaN')
        # print(len(self.eulerY), len(self.rungeY), len(X), len(Y))
        l = min([len(self.eulerY), len(self.rungeY), len(X), len(Y)])

        table = PrettyTable()
        table.add_column('xi', [round(i, 3) for i in X][:l])
        table.add_column('Эйлера', self.eulerY[:l])
        table.add_column('Рунге', self.rungeY[:l])
        table.add_column('Милн', Y[:l])
        table.add_column('Точное решение', [self.I(i, self.C) for i in X][:l])

        return table, X, self.eulerY, self.rungeY, Y
