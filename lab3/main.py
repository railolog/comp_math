from function_t import Function
from integrals import *
from math import *

functions = [
    Function(lambda x: x**2, 'x^2'),
    Function(lambda x: 3*x**3 + 5*x**2 + 3*x - 6, '3x^3 + 5x^2 + 3x - 6'),
    Function(lambda x: x**3 + 2*x**2 - 3*x - 12, 'x^3, + 2x^2 - 3x - 12'),
    Function(lambda x: x**3 - 2*x**2 - 5*x + 24, 'x^3 - 2x^2 - 5x + 24'),
    Function(lambda x: (sin(x)**3 * cos(x**3)**4), 'sin^3(x) * cos^4(x^2)')
]


solvers = [left_rect, right_rect, mid_rect, [left_rect, right_rect, mid_rect], trapeze, simp, [left_rect, right_rect, mid_rect, trapeze, simp]]
solvers_names = [
    'Метод левых прямоугольников',
    'Метод правых прямоугольников',
    'Метод средних прямоугольников',
    'Метод прямоугольников(левые, правые, средние)',
    'Метод трапеций',
    'Метод Симпсона',
    'Все методы'
]
names = [
    'Метод левых прямоугольников',
    'Метод правых прямоугольников',
    'Метод средних прямоугольников',
    'Метод трапеций',
    'Метод Симпсона'
]



def print_err(msg: str):
    print(f'Ошибка: {msg}')


def read_float() -> float:
    try:
        n = float(input().strip().replace(',', '.'))
        return n
    except:
        print('Введите вещественное число')
        return read_float()


def read_int() -> int:
    try:
        n = int(input().strip())
        return n
    except:
        print('Введите целое число')
        return read_int()


def read_f():
    print('Выберите функцию:')

    for i in range(len(functions)):
        print(f'{i + 1}) y = {functions[i]}')

    n = read_int()
    if n > len(functions) or n <= 0:
        return read_f()

    return functions[n - 1].f


def read_ab() -> (float, float):
    print('Введите левый предел')
    a = read_float()
    print('Введите правый предел')
    b = read_float()

    if a == b:
        print('Введите различные числа')
        return read_ab()
    if a > b:
        return b, a
    return a, b


def read_precision() -> float:
    print('Введите точность вычисления')
    eps = read_float()

    if eps <= 0:
        print('Точность должна быть >= 0')
        return read_precision()
    return eps


def read_method() -> Callable:
    print('Выберите метод вычисления интеграла:')
    for i in range(len(solvers)):
        print(f'{i + 1}) {solvers_names[i]}')

    n = read_int()
    if n > len(solvers) or n <= 0:
        print('Введен не существующий номер метода')
        return read_method()

    return solvers[n - 1]


def main():
    f = read_f()
    a, b = read_ab()
    eps = read_precision()
    method = read_method()

    try:
        for i in range(len(method)):
            print(names[i])
            I, n = integrate(f, a, b, eps, method[i])
            print(f'Значение интеграла: {I}\nЧисло разбиения интервала: {n}')
            print('-----------------------------------------------------------')
    except TypeError:
        I, n = integrate(f, a, b, eps, method)
        print(f'Значение интеграла: {I}\nЧисло разбиения интервала: {n}')


if __name__ == '__main__':
    main()
