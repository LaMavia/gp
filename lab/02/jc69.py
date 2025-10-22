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
        if self.t % self.d == 0:
            counts = np.array(
                [np.count_nonzero(self.seq == i) for i in range(JC.SIGMA)]
            )
            counts = counts.astype(np.float64) / np.sum(counts)

            self.xs.append(self.t)
            self.ys.append(np.linalg.norm(JC.ST_DIST - counts))

    def run(self):
        for t in range(self.K * self.d):
            self.t = t
            self.gather_data()
            self.step_seq()

    def plot(self):
        plt.plot(self.xs, self.ys, ".")
        plt.show()


def main():
    args = parser.parse_args()

    factors = [1.0, 2.0, 5.0]
    ls = [1e2, 5e2, 1e3, 5e3, 1e4, 5e4, 1e5, 5e5, 1e6, 5e6]

    s = list(".1234")

    fig, (ax1, ax2) = plt.subplots(1, 2)

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

    sim_xs = []
    sim_ys = []
    sim_yerr = []
    for j, l in enumerate(tqdm(ls, "Sequence lengths")):
        common_xs = set()
        yss = []
        for i, f in enumerate(factors):
            jc = JC(
                seq="A" * int(l),
                d=(d := int(args.interval * f)),
                K=(K := int(args.steps / f)),
                alpha=args.alpha,
            )
            jc.run()
            yss.append((jc.xs, jc.ys))
            if i == 0:
                common_xs = common_xs.union(jc.xs)
            else:
                common_xs.intersection_update(jc.xs)

        yss = [
            np.array([y for x, y in zip(xs, ys) if x in common_xs]) for xs, ys in yss
        ]
        diffs = [
            np.linalg.norm(ys_a - ys_b)
            for i_a, ys_a in enumerate(yss)
            for i_b, ys_b in enumerate(yss)
            if i_a > i_b
        ]

        sim_xs.append(l)
        sim_ys.append(np.average(diffs))
        sim_yerr.append([np.min(diffs), np.max(diffs)])

    ax2.errorbar(sim_xs, sim_ys, yerr=np.array(sim_yerr).T, fmt="-c", capsize=4)
    ax2.set_yscale("log")
    ax2.set_xscale("log")
    ax2.set(title="random-run plot difference for varying sequence lengths")
    ax2.set_xlabel("sequence length")
    ax2.set_ylabel("avg. plot distance between scaling factors")

    fig.show()
    plt.show()


if __name__ == "__main__":
    main()
