from typing import Callable

MAX_IT = 10**6


def left_rect(f: Callable, a: float, b: float, n: int) -> float:
    I = 0
    h = (b - a) / n
    x = a
    for i in range(n):
        I += f(x)
        x += h

    return I * h


def right_rect(f: Callable, a: float, b: float, n: int) -> float:
    I = 0
    h = (b - a) / n
    x = a
    for i in range(n):
        x += h
        I += f(x)

    return I * h


def mid_rect(f: Callable, a: float, b: float, n: int) -> float:
    I = 0
    h = (b - a) / n
    x = a
    for i in range(n):
        x += h/2
        I += f(x)
        x += h/2

    return I * h


def trapeze(f: Callable, a: float, b: float, n: int) -> float:
    I = 0
    h = (b - a) / n
    x = a
    for i in range(n - 1):
        x += h
        I += f(x)

    return h * ((f(a) + f(b)) / 2 + I)


def simp(f: Callable, a: float, b: float, n: int) -> float:
    I = 0
    h = (b - a) / n
    x = a
    for i in range(n + 1):
        if i == 0 or i == n:
            I += f(x)
        elif i % 2 == 0:
            I += 2 * f(x)
        else:
            I += 4 * f(x)

        x += h

    return I * h / 3


def integrate(f: Callable, a: float, b: float, eps: float, I: Callable) -> (float, int):
    n = 4

    I0 = I(f, a, b, n)
    n *= 2
    I1 = I(f, a, b, n)
    # print(f'I0: {I0}, I1: {I1}')
    while abs(I1 - I0)/15 > eps and n < MAX_IT:
        I0 = I1
        n *= 2
        I1 = I(f, a, b, n)
        # print(f'I0: {I0}, I1: {I1}')

    if n >= MAX_IT:
        print('Превышено максимальное значние n, окончательный ответ не получен')

    return I1, n
