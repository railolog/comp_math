from decimal import Decimal
import math

from equation import *

equations = [
    Equation(
        lambda x, y: x + y,
        lambda x, c: c * math.exp(x) - x - 1,
        lambda x, y: (y + x + 1) / math.exp(x),
        'y + x'
    ),
    Equation(
        lambda x, y: x**3,
        lambda x, c: c + x**4 / 4,
        lambda x, y: y - x**4 / 4,
        'x^3'
    ),
    Equation(
        lambda x, y: math.sin(x) - y,
        lambda x, c: c * math.exp(-x) + math.sin(x)/2 - math.cos(x)/2,
        lambda x, y: (y - math.sin(x)/2 + math.cos(x)/2)/math.exp(-x),
        'sin(x) - y'
    )
]


def readInt():
    try:
        return int(input())
    except:
        print('Введите целое число')
        return readInt()


def readFloat():
    try:
        return float(input())
    except:
        print('Введите число')
        return readFloat()


def chooseEquation():
    print('Выберите уравнение:')

    for i in range(len(equations)):
        print(f'{i + 1}) {equations[i]}')

    n = readInt()
    while n < 1 or n > len(equations):
        n = readInt()

    return equations[n - 1]


def readStarters():
    print('y_0 = y(x_0) = ', end='')
    y0 = readFloat()

    print('Введите левую границу:')
    x0 = readFloat()

    print('Введите правую границу:')
    xn = readFloat()

    print('Введите шаг h:')
    h = readFloat()

    print('Введите точность:')
    eps = readFloat()

    while eps <= 0:
        print('Точность должна быть > 0')
        eps = readFloat()

    return y0, x0, xn, h, eps


def run():
    equation = chooseEquation()
    y0, x0, xn, h, eps = readStarters()

    if h > xn - x0:
        exit(10)

    concreteEquation = ConcreteEquation(equation, y0, x0, xn, h, eps)

    concreteEquation.rungeRuledEuler()
    concreteEquation.rungeRuledRunge()
    print(concreteEquation.miln())


if __name__ == '__main__':
    run()
