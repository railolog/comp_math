from prettytable import PrettyTable
import numpy as np
import math


def r(num, digits=3):
    if num == 0:
        return 0

    try:
        scale = int(-math.floor(math.log10(abs(num - int(num))))) + digits - 1
    except ValueError:
        scale = digits

    if scale < digits:
        scale = digits

    if abs(num) >= 1:
        scale = digits

    return round(num, scale)


class Base:
    def __init__(self, X, Y):
        self.table = None
        self.X = X
        self.Y = Y
        self.n = len(X)

    def empirical(self):
        Y = []
        for x in self.X:
            Y.append(self.eval(x))

        return Y

    def eval(self, x):
        return x

    def eps(self):
        epsArr = []

        for x, y in zip(self.X, self.Y):
            epsArr.append(self.eval(x) - y)

        return epsArr

    def S(self):
        return sum([e ** 2 for e in self.eps()])

    def delta(self):
        return (self.S() / self.n) ** 0.5

    def prepareTable(self):
        table = PrettyTable()

        table.add_column('№', range(1, self.n + 1))
        table.add_column('X', self.X)
        table.add_column('Y', self.Y)
        table.add_column(self.__str__(), list(map(r, self.empirical())))
        table.add_column('eps', list(map(r, self.eps())))

        self.table = table

    def showInfo(self):
        self.prepareTable()
        res = str(self.table) + '\n' + f'S = {self.S()}' + '\n' + f'delta = {self.delta()}'
        print(res)


class Linear(Base):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.a, self.b = self.solve()

    def solve(self):
        SX = sum(self.X)
        SXX = sum([x ** 2 for x in self.X])
        SY = sum(self.Y)
        SXY = sum([x * y for x, y in zip(self.X, self.Y)])

        d = SXX * self.n - SX ** 2
        d1 = SXY * self.n - SX * SY
        d2 = SXX * SY - SX * SXY

        return d1 / d, d2 / d  # TODO

    def eval(self, x):
        return self.a * x + self.b

    def addPlot(self, plt):
        x = np.linspace(min(self.X), max(self.X), 100)
        y = self.a * x + self.b

        plt.plot(x, y, 'b')

    def corr(self):
        xm = sum(self.X) / self.n
        ym = sum(self.Y) / self.n

        a = sum([(x - xm) * (y - ym) for x, y in zip(self.X, self.Y)])
        b = sum([(x - xm) ** 2 for x in self.X]) * sum([(y - ym) ** 2 for y in self.Y])

        try:
            return a / math.sqrt(b)
        except ZeroDivisionError:
            return 0

    def __str__(self):
        return f'{r(self.a)}*x + {r(self.b)}'

    def showInfo(self):
        self.prepareTable()
        res = str(self.table) + '\n' + f'S = {self.S()}' + '\n' + f'delta = {self.delta()}'
        res += '\n' + f'Коэффициент корелляции Пирсона = {self.corr()}'
        print(res)


class Quadratic(Base):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.a0, self.a1, self.a2 = self.solve()

    def solve(self) -> [float, float, float]:
        SX = sum(self.X)
        SX2 = sum([x ** 2 for x in self.X])
        SX3 = sum([x ** 3 for x in self.X])
        SX4 = sum([x ** 4 for x in self.X])
        SXY = sum([x * y for x, y in zip(self.X, self.Y)])
        SX2Y = sum([x * x * y for x, y in zip(self.X, self.Y)])
        SY = sum(self.Y)

        b = np.array([SY, SXY, SX2Y])
        a = np.array([[self.n, SX, SX2],
                      [SX, SX2, SX3],
                      [SX2, SX3, SX4]])

        return np.linalg.solve(a, b)

    def eval(self, x):
        return self.a0 + self.a1 * x + self.a2 * x ** 2

    def addPlot(self, plt):
        x = np.linspace(min(self.X), max(self.X), 100)
        y = self.a0 + self.a1 * x + self.a2 * x ** 2

        plt.plot(x, y, 'g')

    def __str__(self):
        return f'{r(self.a2)}*x^2 + {r(self.a1)}*x + {r(self.a0)}'


class ThreeBased(Base):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.a0, self.a1, self.a2, self.a3 = self.solve()

    def solve(self) -> [float, float, float]:
        SX = sum(self.X)
        SX2 = sum([x ** 2 for x in self.X])
        SX3 = sum([x ** 3 for x in self.X])
        SX4 = sum([x ** 4 for x in self.X])
        SX5 = sum([x ** 5 for x in self.X])
        SX6 = sum([x ** 6 for x in self.X])

        SY = sum(self.Y)
        SXY = sum([x * y for x, y in zip(self.X, self.Y)])
        SX2Y = sum([x * x * y for x, y in zip(self.X, self.Y)])
        SX3Y = sum([x * x * x * y for x, y in zip(self.X, self.Y)])

        b = np.array([SY, SXY, SX2Y, SX3Y])
        a = np.array([[self.n, SX, SX2, SX3],
                      [SX, SX2, SX3, SX4],
                      [SX2, SX3, SX4, SX5],
                      [SX3, SX4, SX5, SX6]])

        return np.linalg.solve(a, b)

    def eval(self, x):
        return self.a0 + self.a1 * x + self.a2 * x ** 2 + self.a3 * x ** 3

    def addPlot(self, plt):
        x = np.linspace(min(self.X), max(self.X), 100)
        y = self.a0 + self.a1 * x + self.a2 * x ** 2 + self.a3 * x ** 3

        plt.plot(x, y, 'y')

    def __str__(self):
        return f'{r(self.a3)}*x^3 + {r(self.a2)}*x^2 + {r(self.a1)}*x + {r(self.a0)}'


class Power(Base):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.a, self.b = self.solve()

    def solve(self):
        Y = [math.log(y) for y in self.Y]
        X = [math.log(x) for x in self.X]
        proxy = Linear(X, Y)

        return math.exp(proxy.b), proxy.a

    def eval(self, x):
        res = self.a * x ** self.b
        return res

    def addPlot(self, plt):
        x = np.linspace(min(self.X), max(self.X), 100)
        y = self.a * x ** self.b

        plt.plot(x, y, 'r')

    def __str__(self):
        return f'{r(self.a)}*x^{r(self.b)}'


class Exp(Base):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.a, self.b = self.solve()

    def solve(self):
        Y = [math.log(y) for y in self.Y]
        X = self.X
        proxy = Linear(X, Y)

        return math.exp(proxy.b), proxy.a

    def eval(self, x):
        return self.a * math.exp(self.b * x)

    def addPlot(self, plt):
        x = np.linspace(min(self.X), max(self.X), 100)
        y = self.a * np.exp(self.b * x)

        plt.plot(x, y, 'c')

    def __str__(self):
        return f'{r(self.a)}*e^({r(self.b)}*x)'


class Log(Base):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.a, self.b = self.solve()

    def solve(self):
        Y = self.Y
        X = [math.log(x) for x in self.X]
        proxy = Linear(X, Y)

        return proxy.a, proxy.b

    def eval(self, x):
        return self.a * math.log(x) + self.b

    def addPlot(self, plt):
        x = np.linspace(min(self.X), max(self.X), 100)
        y = self.a * np.log(x) + self.b

        plt.plot(x, y, 'm')

    def __str__(self):
        return f'{r(self.a)}*ln(x) + {r(self.b)}'
