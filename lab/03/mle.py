import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt


class MLE:
    def __init__(self, a: float) -> None:
        self.a = a

    def _decompose(self, a: NDArray, b: NDArray):
        assert a.size == b.size

        I = np.minimum(a != '-', b != '-')
        a = a[I]
        b = b[I]

        matches = a == b
        n_matching = np.count_nonzero(matches)
        n_non_matching = a.size - n_matching

        return n_matching, n_non_matching

    def pJC(self, a: NDArray, b: NDArray, t: float | NDArray):
        n_matching, n_non_matching = self._decompose(a, b)

        e = np.exp(-4 * self.a * t)

        return (0.25 + 0.75 * e)**n_matching * (0.25 - 0.25 * e)**n_non_matching

    def optT(self, a: NDArray, b: NDArray):
        n, m = self._decompose(a, b)

        if m == 0:
            return 0
        if n == 0:
            return -1

        if 3 * n > m:
            return np.log(3 * (n + m) / (3 * n - m)) / (4 * self.a)
        else:
            ...

        

if __name__ == "__main__":
    f = lambda x: np.array(list(x))
    a = f("ACCATAACGA-TGCATCGGA-GACACAAACACGGGGAAACGAGA")
    b = f("ACCAT--CGC-TCCTTAGGAG---ACAATCTCTGGGAACAGGA-")
    
    mle = MLE(1)
    # plt.plot(ts := np.arange(0, 1, 0.01), mle.pJC(a, b, ts))
    # plt.show()

    mle.optT(a, b)

