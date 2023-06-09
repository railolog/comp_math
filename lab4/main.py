import sys
from functions import *
import matplotlib.pyplot as plt


def inputStream():
    print('Выберите способ ввода исходных данных')
    print('Нажмиет Enter, если хотите осуществить ввод из консоли, иначе введите имя файла: ', end='')

    name = input().strip()

    if name == '':
        return sys.__stdin__
    else:
        try:
            return open(name)
        except:
            print('Невозможно открыть файл')
            exit(1)


def ifPrint(mes, end='\n'):
    if sys.stdin == sys.__stdin__:
        print(mes, end=end)


def readInt():
    try:
        n = int(input().strip())
        return n
    except:
        if sys.stdin == sys.__stdin__:
            print('Пожалуйста, введите целое число')
            return readInt()
        print('Введено не целое число')
        exit(1)


def readAmount():
    ifPrint('Введите число пар (x, y) в таблице: ', end='')
    n = readInt()
    while n > 12 or n < 4:
        print('Число пар должно быть от 8 до 12 включительно')
        if sys.stdin != sys.__stdin__:
            exit(1)
        n = readInt()

    return n


def readPair():
    try:
        x, y = [float(i) for i in input().strip().split()]
        return x, y
    except:
        if sys.stdin == sys.__stdin__:
            print('Введите пару вещественных чисел через пробел')
            return readPair()
        exit(1)


def readPairs(n):
    x, y = [], []
    ifPrint('Введите пары x, y через пробел, по одной на строчку')
    for i in range(n):
        xi, yi = readPair()
        x.append(xi)
        y.append(yi)

    return x, y


def readTable():
    n = readAmount()
    return readPairs(n)


def draw(table, arr):
    plt.plot(table[0], table[1], 'ko')
    legend = ['Y']

    for f in arr:
        f.addPlot(plt)
        legend.append(str(f))

    plt.legend(legend)
    plt.show()


def run(stream):
    sys.stdin = stream
    table = readTable()

    xY = dict()
    for x, y in zip(table[0], table[1]):
        if x not in xY.keys():
            xY[x] = y
        elif xY[x] != y:
            print('Введена не функция')
            exit(2)

    approxArr = [
        Linear(*table),
        Quadratic(*table),
        ThreeBased(*table)
    ]

    x0 = any(x <= 0 for x in table[0])
    y0 = any(y <= 0 for y in table[1])

    if (x0 or y0) is False:
        approxArr.extend((Power(*table), Exp(*table), Log(*table)))
    elif x0 is False:
        approxArr.append(Log(*table))
    elif y0 is False:
        approxArr.append(Exp(*table))

    # print(power.eval(table[0][0]))
    if sys.stdin != sys.__stdin__:
        print('Результаты записаны в файл output.txt')
        sys.stdout = open('output.txt', 'w')

    for approx in approxArr:
        approx.showInfo()
        print()

    best = min(approxArr, key=lambda x: x.delta())

    print(f'Наименьшее среднеквадратичное отклонение {best.delta()} у функции {best}')

    draw(table, approxArr)


if __name__ == '__main__':
    run(inputStream())
