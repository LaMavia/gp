import altair as alt
import pandas as pd
import sys


def main(models_file: str):
    with open(models_file, "r") as f:
        models = [line.strip() for line in f.readlines() if len(line) > 1]

    print(models)

    df = pd.DataFrame({"model": models})

    alt.Chart(df).mark_bar().encode(alt.X("model:N"), alt.Y("count():Q")).save(
        "models.svg"
    )


if __name__ == "__main__":
    main(models_file=sys.argv[1])
