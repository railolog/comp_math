import math
import sys
from interpolation import *

STDIN = sys.__stdin__
FUNC = -1


functions = [
    lambda x: math.sin(x),
    lambda x: 3*x**3 - 5*x**2 + 17*x - 4,
    lambda x: 3*math.sin(x)**2 - 2*math.cos(x)**3
]

functionNames = [
    'sin(x)',
    '3x^3 - 5x^2 + 17x - 4',
    '3*sin(x)^2 - 2*cos(x)^3'
]

assert len(functionNames) == len(functions)


def printf(mes, end='\n'):
    if sys.stdin == sys.__stdin__:
        print(mes, end=end)


def readInt():
    try:
        n = int(input())
        return n
    except:
        print('Введено не целое число')

        if sys.stdin == STDIN:
            return readInt()
        exit(1)


def readFloat():
    try:
        return float(input())
    except:
        print('Введено не число')

        if sys.stdin == STDIN:
            return readFloat()
        exit(1)


def readFloatPair():
    try:
        return [float(i) for i in input().strip().split()]
    except:
        print('Некорректный ввод. Вводите пары значений (x, y) по одной на строке через пробел')

        if sys.stdin == STDIN:
            return readFloatPair()
        exit(1)


def getFileStream():
    name = input('Введите имя файла (или нажмите Enter): ')

    if name == '':
         return sys.__stdin__
    else:
        try:
            return open(name)
        except:
            print('Произошла ошибка!')
            return getFileStream()


def readTable(stream=sys.__stdin__):
    sys.stdin = stream

    printf('Введите число пар (x, y) (от 2 до 10)')
    n = readInt()

    while sys.stdin == STDIN and (n < 2 or n > 10):
        printf('Введите число пар (x, y) (от 2 до 10)')
        n = readInt()

    if sys.stdin != STDIN and (n < 2 or n > 10):
        exit(2)

    X, Y = [], []

    printf('Введите пары через пробел по одной на строке: ')
    for i in range(n):
        a, b = readFloatPair()
        X.append(a)
        Y.append(b)

    sys.stdin = sys.__stdin__

    return X, Y


def chooseFunc():
    print('Выберите функцию: ')

    for i in range(len(functionNames)):
        print(f'{i + 1}) {functionNames[i]}')

    n = readInt()
    if n < 1 or n > len(functions):
        return chooseFunc()

    global FUNC
    FUNC = n - 1
    return functions[n - 1]


def generateTable():
    func = chooseFunc()

    print('Введите левую границу интервала:')
    a = readFloat()

    print('Введите правую границу интервала:')
    b = readFloat()

    if b < a:
        a, b = b, a

    print('Введите кол-во точек на интервале (2-10):')
    n = readInt()

    n = min(n, 10)
    n = max(n, 2)

    step = (b - a) / (n - 1)
    X, Y = [], []
    x = a

    for i in range(n):
        X.append(x)
        Y.append(func(x))

        x += step

    return X, Y


def getTable():
    print('Выберите способ ввода данных:')
    print('1) В виде пар значений (х, у) через консоль')
    print('2) В виде пар значений (х, у) из файла')
    print('3) На основе функции')

    n = readInt()
    while n > 3 or n < 1:
        print('Введите число от 1 до 3')
        n = readInt()

    if n == 1:
        return readTable()
    elif n == 2:
        return readTable(getFileStream())
    elif n == 3:
        return generateTable()


def verify(arr):
    step = arr[1] - arr[0]

    if math.isclose(step, 0): return False
    if len(arr) == 2: return True

    for i in range(2, len(arr)):
        if not math.isclose(arr[i] - arr[i - 1], step):
            return False

    return True


def run():
    X, Y = getTable()

    if not verify(X):
        print(X)
        print('Введены не равноотстоящие узлы')
        exit(1)

    print('Введите значение аргумента:')
    x = readFloat()

    solver = Solver(X, Y, x)

    print(solver.diffTable())
    print('Лагранж:', solver.lagrange())
    print('Ньютон:', solver.newtonF(x))

    if FUNC >= 0:
        print(f'Реальное значение функции: {functions[FUNC](x)}')

    solver.graph()


if __name__ == '__main__':
    run()
