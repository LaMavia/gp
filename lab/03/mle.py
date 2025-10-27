from os import PathLike, path
import sys
from typing import overload
import numpy as np
from numpy.random import choice, rand, uniform
from numpy.typing import NDArray
import matplotlib.pyplot as plt
import matplotlib
from tqdm import tqdm

from Bio.SeqIO.FastaIO import SimpleFastaParser

# https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html
def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current Axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(range(data.shape[1]), labels=col_labels,
                  rotation=-30, ha="right", rotation_mode="anchor")
    ax.set_yticks(range(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar

# https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html
def annotate_heatmap(im, data: NDArray | None=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data: NDArray = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(np.max(data))/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) < threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts


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

    @overload
    def pJC(self, a: NDArray, b: NDArray, t: float) -> float: ...
    @overload
    def pJC(self, a: NDArray, b: NDArray, t: NDArray) -> NDArray: ...
    def pJC(self, a: NDArray, b: NDArray, t: float | NDArray) -> float | NDArray:
        n_matching, n_non_matching = self._decompose(a, b)

        e = np.exp(-4 * self.a * t)

        return (0.25 + 0.75 * e)**n_matching * (0.25 - 0.25 * e)**n_non_matching

    def optT(self, a: NDArray, b: NDArray):
        n, m = self._decompose(a, b)

        if 3 * n > m:
            return np.log(3 * (n + m) / (3 * n - m)) / (4 * self.a)
        else:
            sim = lambda t1, t2: abs(t1 - t2) 
            score = lambda t: self.pJC(a, b, t) / t
            rounds = 50
            bank_size = 50
            n_seed = 10
            x = uniform(0, 5, bank_size)

            bank: dict[float, float] = {(t := float(x[i])): float(score(t)) for i in range(x.size)}
            d_avg = sum(sim(t1, t2) for t1 in bank for t2 in bank) / len(bank) ** 2
            d_cut = d_avg / 2

            for r in range(rounds):
                scores = sorted(bank.items(), key=lambda p: p[1], reverse=True)
                d_cut = max(d_avg / 5, d_cut * 0.98 ** r)
                for t1, _ in scores[n_seed:]:
                    t2s = list(choice(list(bank.keys()), 5))
                    for t2 in t2s:
                        p = rand()
                        t3 = float(p * t1 + (1 - p) * t2)
                        news = [t3, t3 + 1]

                        for t3 in news: 
                            t3_score = float(score(t3))
                            worst, worst_score = scores[-1]

                            if t3_score < worst_score:
                                continue

                            closest, _ = scores[0]
                            min_dist = sim(t3, closest)

                            for t in bank:
                                d = sim(t3, t)
                                if d <= min_dist:
                                    min_dist = d
                                    closest = t

                            if min_dist < d_cut: 
                                if t3_score > bank[closest]:
                                    index_of_closest = scores.index((closest, bank[closest]))
                                    del bank[closest]
                                    bank[t3] = t3_score
                                    scores[index_of_closest] = (t3, t3_score)
                            else:
                                scores[-1] = (t3, t3_score)
                                del bank[worst] 
                                bank[t3] = t3_score

                                scores = sorted(scores, key=lambda p: p[0], reverse=True)
                        
            t = max(bank.keys(), key=lambda t: bank[t])
            return t

    def simmatrix(self, filename: PathLike | str) -> tuple[list[str], NDArray]:
        labels: list[str] = []
        sequences: list[NDArray] = []
        with open(filename) as f:
            for label, seq in SimpleFastaParser(f):
                labels.append(label)
                sequences.append(np.array(list(seq)))

        n = len(sequences)
        M = np.zeros((n, n))
        pairs = [
            ((i, seq_i), (j, seq_j)) 
            for i, seq_i in enumerate(sequences) 
            for j, seq_j in enumerate(sequences) 
            if i <= j
        ]
        for (i, seq_i), (j, seq_j) in tqdm(pairs):
            M[i, j] = M[j, i] = self.optT(seq_i, seq_j)

        return labels, M

        

if __name__ == "__main__":
    f = lambda x: np.array(list(x))
    a = f("ACCATAACGA-TGCATCGGA-GACACAAACACGGGGAAACGAGA")
    b = f("ACCAT--CGC-TCCTTAGGAG---ACAATCTCTGGGAACAGGA-")
    
    mle = MLE(1)

    labels, M = mle.simmatrix(sys.argv[1])    
    im, cbar = heatmap(M, labels, labels)
    annotate_heatmap(im, valfmt='{x:.02f}')
    plt.show()

