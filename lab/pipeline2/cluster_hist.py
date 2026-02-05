from sys import argv
import altair as alt
import pandas as pd


def main(file: str):
    with open(file, "r") as f:
        sizes = [int(line.strip()) for line in f.readlines()]

    alt.Chart(
        pd.DataFrame({"size": sizes}), title="Rozkład wielkości klastrów"
    ).mark_bar().encode(
        alt.X("size:Q", title="Rozmiar klastru").bin(step=20),
        alt.Y("count():Q", title="Ilość klastrów").scale(type="log"),
    ).properties(width=800, height=400).save(file.replace(".txt", ".svg"))


if __name__ == "__main__":
    main(argv[1])
