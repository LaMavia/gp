import altair as alt
import numpy as np
import pandas as pd

# Compute x^2 + y^2 across a 2D grid
x, y = np.meshgrid(range(-5, 5), range(-5, 5))
z = x**2 + y**2

oc = "Orth. Con."
ofc = "Orth. Filtered Con."
os = "Orth. Super"

tt = "Time Tree"
ncbi = "NCBI"
pub = "Publication"

df = pd.read_csv("./scores.csv", delimiter=";")


# Convert this grid to columnar pandasta expected by Altair
source = pd.DataFrame(
    {
        "method": [{"oc": oc, "foc": ofc, "os": os}[m] for m in df["method"]],
        "reference": [{"tt": tt, "ncbi": ncbi, "pub": pub}[m] for m in df["reference"]],
        "nRF": list(df["nRF"]),
        "nJRF": list(df["nJRF"]),
    }
)

print(source.sort_values("method").to_string(index=False))


def f(k: str):
    base = alt.Chart(source, title=k).properties(width=300, height=300)

    heatmap = base.mark_rect().encode(x="reference:O", y="method:O", color=f"{k}:Q")

    color = alt.value("black")
    text = base.mark_text(baseline="middle").encode(
        alt.Text(f"{k}:Q", format=".0f"), color=color
    )

    return heatmap


(f("nRF") | f("nJRF")).save("scores.svg")
