import sys

from numpy.linalg import LinAlgError

from equation import Equation, IntervaledEquation, EquationSystem
from math import *
from Newton import newton
from solvers import chord_method, secants_method, iterations_method

single_equations = [
    Equation(lambda x: 2*x**3 + 3.41*x**2 - 23.74*x + 2.95, lambda x: 6*x**2 + 6.82*x - 23.74, lambda x: 12*x + 6.82, ''),
    Equation(lambda x: x**3 - x + 4, lambda x: 3*x**2 - 1, lambda x: 6*x, 'x^3 - x + 4 = 0'),
    Equation(lambda x: x**3 + 2.28*x**2 - 1.934*x - 3.907, lambda x: 3*x**2 + 4.56*x - 1.934, lambda x: 6*x + 4.56, 'x^3 + 2.28*x^2 - 1.934*x - 3.907 = 0'),
    Equation(lambda x: log10(x**2 + 4) - 1 - cos(x), lambda x: 2*x/(x**2 + 4)/log(10) + sin(x), lambda x: (-2*x**2 + (4 + x**2)**2 * log(10) * cos(x) + 8)/((4 + x**2)**2 * log(10)), 'lg(x^2 + 4) - 1 - cos(x) = 0')
]

equation_systems = [
    EquationSystem(lambda x, y: x**2 + y**2 - 4, lambda x, y: -3*x**2 + y,
                   lambda x, y: 2*x, lambda x, y: 2*y,
                   lambda x, y: -6*x, lambda x, y: 1,
                   'x^2 + y^2 -4 = 0', '-3*x^2 + y = 0',
                   'x**2 + y**2 - 4', '-3*x**2 + y'),
    EquationSystem(lambda x, y: x**2 + y**2 - 13, lambda x, y: x*y - 6,
                   lambda x, y: 2*x, lambda x, y: 2*y,
                   lambda x, y: y, lambda x, y: x,
                   'x^2 + y^2 - 13 = 0', 'x*y - 6 = 0',
                   'x**2 + y**2 - 13', 'x*y - 6'),
    EquationSystem(lambda x, y: 2*x**2 + 3*y**2 - 10, lambda x, y: cos(x) - 0.5*y,
                   lambda x, y: 4*x, lambda x, y: 6*y,
                   lambda x, y: -sin(x), lambda x, y: -0.5,
                   '2*x^2 + 3*y^2 = 10', 'cos(x) = 0.5y',
                   '2*x**2 + 3*y**2 - 10', 'sympy.cos(x) - 0.5*y')
]


def read_int():
    a = input().strip()

    try:
        res = int(a)
        return res
    except ValueError:
        if sys.stdin == sys.__stdin__:
            print('Пожалуйста, введите целое число')
            return read_int()
        else:
            print('На вход было подано не целое число')
    except EOFError:
        print('Конец ввода')


def read_float():
    a = input().strip()

    try:
        res = float(a)
        return res
    except ValueError:
        if sys.stdin == sys.__stdin__:
            print('Пожалуйста, введите целое число')
            return read_float()
        else:
            print('На вход было подано не целое число')
    except EOFError:
        print('Конец ввода')


def read_approx():
    print('Введите начальное приближение (x0 и y0 через пробел)')
    try:
        x, y = [float(i) for i in input().strip().split()]
        return x, y
    except:
        print('Введите 2 числа через пробел')
        return read_approx()


def read_starters():
    sys.stdin = sys.__stdin__
    filename = input('Введите имя файла, с которого считать границы интервала и погрешность или нажмите Enter: ')

    if filename.strip() != '':
        try:
            sys.stdin = open(filename, 'r')
        except:
            sys.stdin = sys.__stdin__
            print('Файл не найден либо недостаточно прав доступа')
            return read_starters()

    try:
        print('Введите три числа (левая граница, правая граница, погрешность) одной строкой через пробел')
        a, b, eps = [float(i) for i in input().strip('\n').strip().split()]
        sys.stdin = sys.__stdin__
        return a, b, eps
    except:
        print('Некорректный ввод. Введите три числа одной строкой через пробел')
        return read_starters()


def choose_method():
    print('Выберите метод решения уравнения: ')
    print('1) Метод хорд')
    print('2) Метод секущих')
    print('3) Метод простой итерации')

    try:
        n = int(input())
        if n == 1:
            return chord_method
        elif n == 2:
            return secants_method
        elif n == 3:
            return iterations_method
        else:
            return choose_method()
    except:
        return choose_method()


def set_printer():
    filename = input('Введите имя файла, в который вывести результаты или нажмите Enter, чтобы вывести в консоль: ')
    if filename.strip() != '':
        try:
            sys.stdout = open(filename, 'w')
        except:
            print('Файл не найден либо недостаточно прав доступа')
            return set_printer()


def single():
    for i in range(len(single_equations)):
        print(f'{i + 1}) {single_equations[i]}')
    try:
        print('Введите номер уравнения, которое хотите решить: ')
        n = read_int()
        eq = single_equations[n - 1]
        eq.graph()
        a, b, eps = read_starters()
        while eps <= 0:
            print('Точность должна быть больше 0')
            a, b, eps = read_starters()

        try:
            intervaled_eq = IntervaledEquation(eq, a, b)
        except ValueError:
            print('Длина интервала изоляции должна быть больше 0')
            single()
            return

        if intervaled_eq.valid is False:
            if not intervaled_eq.necessary_cond:
                print('Не выполнено необходимое условие наличия корня.')
            else:
                print('Не выполнено достаточное условие единственности корня на отрезке.')

            if len(intervaled_eq.intervals) > 0:
                print('Обратите внимание на интервалы:')
                for i in intervaled_eq.intervals:
                    print(round(i[0], 6), round(i[1], 6))
            single()
            return

        intervaled_eq.graph()
        method = choose_method()

        try:
            ans, it = method(intervaled_eq, eps)

            set_printer()


            print('Найденный корень уравнения: ', ans)
            print('Значение функции в корне: ', eq.f(ans))
            print('Число итераций: ', it)
        except ValueError as err:
            print(str(err))
        except ZeroDivisionError:
            print('Ошибка: Был введен интервал, на котором производная не сохраняет свой знак')
    except IndexError:
        single()


def system():
    for i in range(len(equation_systems)):
        print(f'{i + 1}) {equation_systems[i]}')
        print('--------------------------------')
    try:
        print('Введите номер уравнения, которое хотите решить: ')
        n = read_int()
        eq = equation_systems[n - 1]
        eq.graph()

        x, y = read_approx()

        print('Введите точность вычисления: ')
        eps = read_float()
        while eps <= 0:
            print('Точность должна быть больше 0')
            eps = read_float()

        try:
            x, y, dx, dy, it = newton(eq, x, y, eps)
        except LinAlgError:
            print('Ошибка: введите начальное приближение, которое не равноудалено от решений системы')
            system()
            return

        print('Вектор неизвестных: ', x, y)
        print('Кол-во итераций для поиска решения: ', it)
        print('Вектор погрешностей: ', abs(dx), abs(dy))
        print('Вектор значений функций с найденными корнями: ', eq.first(x, y), eq.second(x, y))
        if round(eq.first(x, y)) == 0 and round(eq.second(x, y)) == 0:
            print('Вывод: система решена верно')
        else:
            print('Вывод: система не решена')
    except IndexError:
        system()


if __name__ == '__main__':
    var = int(input('Вы хотите решить нелинейное уравнение(1) или систему(2): '))
    if var == 1:
        single()
    elif var == 2:
        system()
