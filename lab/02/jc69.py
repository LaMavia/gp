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

    def gather_data(self, t:int):
        counts = np.array(
            [np.count_nonzero(self.seq == i) for i in range(JC.SIGMA)]
        )
        counts = counts.astype(np.float64) / np.sum(counts)

        self.xs.append(t)
        self.ys.append(np.linalg.norm(JC.ST_DIST - counts))

    def run(self):
        print(f"============ {self.K=}, {self.d=}")
        for self.t in range(0, self.K):
            self.gather_data(self.t * self.d)
            for _ in range(self.d):
                print(f"{self.t=}")
                self.step_seq()
        # for self.t in range(0, self.K * self.d, self.d):
        #     self.gather_data()
        #     self.step_seq()
        print("============")

    def plot(self):
        plt.plot(self.xs, self.ys, ".")
        plt.show()


def main():
    args = parser.parse_args()

    # factors = [float(x) for x in range(1, 3, 1) if args.steps % x == 0]
    # # ls = []
    #
    s = ['o-']
    #
    fig, ax1 = plt.subplots()
    jc0 = JC(
        seq=f"{args.sequence}",
        d=args.interval,
        K=args.steps,
        alpha=args.alpha
    )
    jc1 = JC(
        seq=f"{args.sequence}",
        d=args.interval//2,
        K=args.steps * 2,
        alpha=args.alpha
    )

    for t in range(args.interval * args.steps):
        jc0.t = t
        jc1.t = t//2
        jc0.gather_data(t)
        jc1.gather_data(t)

        jc0.step_seq()
        jc1.step_seq()
        jc1.step_seq()

    ax1.plot(jc0.xs, jc0.ys, s[0], label="normal")
    ax1.plot(jc1.xs, jc1.ys, s[0], label="d/2, K*2")

    #
    # for i, f in enumerate(tqdm(factors[::-1], "Factors")):
    #     jc = JC(
    #         seq=args.sequence,
    #         d=(d := int(args.interval * f)),
    #         K=(K := int(args.steps / f)),
    #         alpha=args.alpha,
    #     )
    #     jc.run()
    #     ax1.plot(jc.xs, jc.ys, s[i % len(s)], label=f"{d=}, {K=}", alpha=0.5)

    ax1.legend()
    ax1.set(
        title=f"JC69 simulation"
    )
    ax1.set_xlabel("t")
    ax1.set_ylabel("distance to stationary distribution")

    fig.show()
    plt.show()
    fig.savefig("jc69.png")


if __name__ == "__main__":
    main()
