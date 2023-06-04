from equation import Equation

equations = [
    Equation(lambda x, y: y + (1 + x) * y**2, 'y + (1 + x)y^2')
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


if __name__ == '__main__':
    run()