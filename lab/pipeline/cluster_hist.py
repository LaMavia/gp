from sys import argv
import altair as alt
import pandas as pd


def main(file: str):
    with open(file, "r") as f:
        sizes = [int(l.strip()) for l in f.readlines()]

    alt.Chart(
        pd.DataFrame({"size": sizes}), title="Rozkład wielkości klastrów"
    ).mark_bar().encode(
        alt.X("size:Q", bin=True, title="Rozmiar klastru"),
        alt.Y("count()", title="Ilość klastrów"),
    ).save("cluster_sizes.svg")


if __name__ == "__main__":
    main(argv[1])
