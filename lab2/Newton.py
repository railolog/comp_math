import numpy
from equation import EquationSystem


def solve(A, d):
    M = numpy.array(A)
    v = numpy.array(d)
    return numpy.linalg.solve(M, v)


def newton(system: EquationSystem, x0: float, y0: float, eps: float) -> [[float, float], [float, float], int]:
    delta = 2 * eps
    it, dx, dy = 0, 0, 0
    while delta > eps:
        it += 1

        A = [[system.dfdx(x0, y0), system.dfdy(x0, y0)],
             [system.dgdx(x0, y0), system.dgdy(x0, y0)]]
        d = [-system.first(x0, y0), -system.second(x0, y0)]

        dx, dy = solve(A, d)
        x0 += dx
        y0 += dy
        delta = max(abs(dx), abs(dy))

        if it > 10**4:
            # print('Превышение кол-ва итераций')
            break

    return x0, y0, dx, dy, it
