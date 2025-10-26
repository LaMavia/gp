import numpy as np
import matplotlib.pyplot as plt
from numpy.typing import NDArray

a = 0.002
def g(t):
    return np.exp(-4 * a * t)


def main2():
    def p0(i, j):
        if i == j: return lambda t: 1/4 * (1 + 3 * g(t))
        else: return lambda t: 1/4 * (1 - g(t))

    def pik(i, k):
        f = p0(i, k)
        return lambda t: f(2 * t)

    def pijk(i, j, k):
        pij = p0(i, j)
        pjk = p0(j, k)

        return lambda t: pij(2 * t) * pjk(2 * t + 1)

    elems = list("ACTG")
    space = [(i, j, k) for i in elems for j in elems for k in elems]
    
    fs = [(pik(i, k), pijk(i, j, k)) for i, j, k in space]
    def y(t):
        return sum(ijk(t) / ik(t) for ik, ijk in fs) / len(fs)

    t = np.linspace(1, 500, 10000) 

    args = list(zip([(1, .25), (3, .75), (3, .75), (3, .75), (6, 6/4)], map(tuple, ["AAA", "AAC", "ACC", "ACA", "ACT"])))
    n = len(args)
    fig, (ax0, ax1, *axs) = plt.subplots(len(args) + 2, 1, figsize=(2 * n, 8 * n))

    augmented_args = [(np.array([]), np.array([]), *a) for a in args]

    for idx, (((m, o), (i, j, k)), ax) in enumerate(zip(args, axs)):
        ax.plot(t, ys_ik := o * pik(i, k)(t), 'k-', label="i→k")
        ax.plot(t, ys_ijk := m * pijk(i, j, k)(t), 'k--', label="i→j→k")
        eq = lambda x, y: '=' if x == y else '≠' 
        ax.set(title=f"i{eq(i, j)}j{eq(j,k)}k{eq(k, i)}i, $\\infty_{{ijk}} = {ys_ijk[-1]:.03}$")
        ax.legend()

        augmented_args[idx] = (ys_ik, ys_ijk, *augmented_args[idx][2:])

    (eq_bucket_ik, eq_bucket_ijk), (neq_bucket_ik, neq_bucket_ijk) = (np.zeros_like(t), np.zeros_like(t)), (np.zeros_like(t), np.zeros_like(t))

    for ys_ik, ys_ijk, m, (i, _, k) in augmented_args:
        if i == k:
            eq_bucket_ik += ys_ik
            eq_bucket_ijk += ys_ijk
        else:
            neq_bucket_ik += ys_ik
            neq_bucket_ijk += ys_ijk

    ax0.plot(t, eq_bucket_ijk, 'g--', label='Pr(i→j→k | i=k)')
    ax0.plot(t, neq_bucket_ijk, 'r--', label="Pr(i→j→k | i≠k)")
    ax0.plot(t, eq_bucket_ik, 'g-', label='Pr(i→k | i=k)')
    ax0.plot(t, neq_bucket_ik, 'r-', label='Pr(i→k | i≠k)')
    ax0.set(title=f"p_eq1={eq_bucket_ik[-1]:.03}, p_neq1={neq_bucket_ik[-1]:.03}\np_eq2={eq_bucket_ijk[-1]:.03}, p_neq2={neq_bucket_ijk[-1]:.03}")
    ax0.legend()

    ax1.plot(t, eq_bucket_ijk / eq_bucket_ik, 'g', label="p_eq2/p_eq1")
    ax1.plot(t, neq_bucket_ijk / neq_bucket_ik, 'r', label="p_neq2/p_neq1")
    ax1.legend()
        
    fig.savefig("nsq.svg")
    fig.savefig("nsq.png")


def main():
    def y1(t):
        return (1 + 3*g(2*t)) * (1 + 3*g(2*t+1)) - 4 - 12*g(2*t)
    def y2(t):
        return (1 + 3*g(2*t)) * (1 - g(2 * t + 1)) - 4 + 4*g(2*t)
    def y3(t):
        return (1 - g(2*t)) * (1 + 3*g(2*t + 1)) - 4 + 4*g(2*t)
    def y4(t):
        return (1 - g(2*t)) * (1 - g(2*t+1)) - 4 - 12*g(2*t)
    def y5(t):
        return (1 - g(2*t)) * (1 - g(2*t+1)) - 4 + 4 * g(2*t)

    t = np.linspace(0, 500, 10000)
    Ey = 1/16 * (y1(t) + 3 * (y2(t) + y3(t) + y4(t)) + 6*y5(t))

    plt.plot(t, Ey)
    plt.show()

if __name__ == '__main__':
    main2()

