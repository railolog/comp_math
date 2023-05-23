from typing import Tuple

from equation import IntervaledEquation

ITERATIONS = 10**4


def chord_method(eq: IntervaledEquation, eps: float) -> Tuple[float, int]:
    x = 0
    f = eq.eq.f
    a = eq.a
    b = eq.b

    it = 0
    delta = 2 * eps
    while delta > eps:
        it += 1
        delta = x
        x = a - f(a) * (b - a) / (f(b) - f(a))
        delta = abs(delta - x)

        if f(x) * f(a) < 0:
            b = x
        else:
            a = x

    return x, it


def secants_method(eq: IntervaledEquation, eps: float) -> Tuple[float, int]:
    f = eq.eq.f
    d2f = eq.eq.d2f
    a = eq.a
    b = eq.b
    x0 = a if f(a) * d2f(a) > 0 else b
    x1 = x0 + max(eps, 0.01)

    it = 0
    while abs(f(x1)) > eps:
        it += 1

        x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        x0 = x1
        x1 = x2

    if x1 < a or x1 > b:
        raise ValueError('Не выполнены достаточные условия сходимости метода Ньютона(секущих)')
    return x1, it


def max_dfi(df, h, a, b):
    d = (b - a) / ITERATIONS
    it = a
    max_df = 0

    for i in range(ITERATIONS):
        max_df = max(abs(max_df), abs(1 + h * df(it)))
        it += d

    return max_df


def iterations_method(eq: IntervaledEquation, eps: float) -> Tuple[float, int]:
    f = eq.eq.f
    df = eq.eq.df
    a = eq.a
    b = eq.b

    max_df = 0
    d = (b - a) / ITERATIONS
    it = a
    x = a
    for i in range(ITERATIONS - 2):
        if abs(df(it)) > abs(max_df):
            max_df = df(it)
        it += d

    h = -1 / max_df
    fi = lambda x: x + h * f(x)

    q = max_dfi(df, h, a, b)

    if q > 0.999:
        print('Значение q близко к единице. Сходимость может быть очень медленной')

    if 1 > q > 0.5:
        eps = (1 - q) * eps / q

    x0 = a
    delta = eps * 2
    it = 0
    while delta > eps:
        it += 1

        x1 = fi(x0)
        delta = abs(x1 - x0)

        x0 = x1

        if it > 5*10**5:
            raise ValueError('Вероятно, выбран слишком длинный интервал для метода простых итераций. Попробуйте ввести уменьшенный интервал.')

    return x0, it
