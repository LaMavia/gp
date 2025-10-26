from typing import Literal
import numpy as np
import argparse as ap
import numpy.typing as npt
import matplotlib.pyplot as plt
from tqdm import tqdm

"""
d - kwant czasu 
K - liczba kroków

rokzład stacjonarny (ACTG) = (1/4, 1/4, 1/4, 1/4)


A A A A A
|
A

p_AA(d) = 1/4 + 3/4 exp(-4d)
p_AT = 1/4 - 1/4 exp(-4d)

dla każdej sekwencji liczymy wektor częstości. Rysujemy odległość od rozkładu stacjonarnego (np. euklidesowa).

t_0 = 0
t_end = K * d

(d to interwał zliczania statystyk)

Przy zmianie K,d -> 2K, d/2 się nie zmienia rozkład. Wyjaśnić.
"""


parser = ap.ArgumentParser()
parser.add_argument("--sequence", "-S", type=str, required=True)
parser.add_argument("--interval", "-d", type=int, required=True)
parser.add_argument("--steps", "-K", type=int, required=True)
parser.add_argument("--alpha", "-a", type=float, required=True)


class JC:
    SIGMA = 4
    MAP = {"A": 0, "T": 1, "C": 2, "G": 3}
    ST_DIST = np.ones(4) * 0.25

    def __init__(self, seq: str, d: int, K: int, alpha: float) -> None:
        self.seq = np.array([JC.MAP[c] for c in seq])
        self.d = d
        self.K = K
        self.a = alpha
        self.t = 0
        self.size = len(seq)
        self.xs = []
        self.ys = []

    def p(self) -> npt.NDArray:
        weights = 0.25 + np.array([0.75, -0.25, -0.25, -0.25]) * np.exp(
            -4.0 * self.a * self.t
        )

        return np.random.choice([0, 1, 2, 3], p=weights, size=self.size)

    def step_seq(self):
        self.seq = (self.seq + self.p()) % JC.SIGMA

    def gather_data(self):
        counts = np.array(
            [np.count_nonzero(self.seq == i) for i in range(JC.SIGMA)]
        )
        counts = counts.astype(np.float64) / np.sum(counts)

        self.xs.append(self.t)
        self.ys.append(np.linalg.norm(JC.ST_DIST - counts))

    def run(self):
        for self.t in range(0, self.K * self.d, self.d):
            self.gather_data()
            self.step_seq()

    def plot(self):
        plt.plot(self.xs, self.ys, ".")
        plt.show()


def main():
    args = parser.parse_args()

    factors = [float(x) for x in range(1, 3, 1) if args.steps % x == 0]
    # ls = []

    s = ['o-']

    fig, ax1 = plt.subplots()

    for i, f in enumerate(tqdm(factors[::-1], "Factors")):
        jc = JC(
            seq=args.sequence,
            d=(d := int(args.interval * f)),
            K=(K := int(args.steps / f)),
            alpha=args.alpha,
        )
        jc.run()
        ax1.plot(jc.xs, jc.ys, s[i % len(s)], label=f"{d=}, {K=}", alpha=0.5)

    ax1.legend()
    ax1.set(
        title=f"JC69 simulation: $\\alpha$={args.alpha}, $K \\in$ {[int(args.steps / f) for f in factors[::-1]]}, $d \\in$ {[int(f * args.interval) for f in factors[::-1]]}"
    )
    ax1.set_xlabel("t")
    ax1.set_ylabel("distance to stationary distribution")

    fig.show()
    plt.show()
    fig.savefig("jc69.png")


if __name__ == "__main__":
    main()
