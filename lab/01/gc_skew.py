import argparse as ap
import matplotlib.pyplot as plt
import sys
from tqdm import tqdm
from itertools import accumulate
import numpy as np

parser = ap.ArgumentParser()
parser.add_argument("--window-size", "-w", type=int, default=1)
parser.add_argument("--stride", "-s", type=int, default=1)


def gc_skew(window: str) -> float:
    g = window.count("G")
    c = window.count("C")

    return (g - c) / (g + c)


def main(args: ap.Namespace):
    EPS = 5e-4
    window_size = args.window_size
    stride = args.stride

    buffer = ""
    position = 0

    ys = []
    xs = []
    intervals = []
    interval = []
    omn, omx = 1, -1

    for i, line in tqdm(enumerate(sys.stdin.readlines())):
        if i == 0:
            continue

        buffer += line

        while len(buffer) > window_size:
            y = gc_skew(buffer[:window_size])
            ys.append(y)
            xs.append(position)

            omn = min(omn, y)
            omx = max(omx, y)

            if abs(y) < EPS:
                interval.append(position)
            elif len(interval) > 0:
                intervals.append(interval)
                interval = []

            buffer = buffer[stride:]
            position += stride

    if len(interval) > 0:
        intervals.append(interval)

    intervals = [(mn := min(i), mx := max(i), mx - mn) for i in intervals]
    print(f"mn:{omn} mx:{omx}")
    print(intervals)
    plt.plot(xs, ys, "-c", label="GC-skew")
    cgc_ys = np.array(list(accumulate(ys)))
    plt.plot(
        xs,
        cgc_ys / np.max(np.abs(cgc_ys)) * max(abs(omn), abs(omx)),
        "--c",
        label="CGC-skew, scaled to GC-skew scale",
    )
    plt.plot(xs, [0] * len(ys), "-k")
    plt.title(
        f"MIN={omn:.3f}, MAX={omx:.3f}, Terminus position≈{np.average(intervals[0][:-1]):.2e}, Origin position≈{np.average(intervals[1][:-1]):.2e}"
    )
    plt.legend()
    plt.show()


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
