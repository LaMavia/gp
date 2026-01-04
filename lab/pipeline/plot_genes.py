import altair as alt
import pandas as pd

df = pd.read_csv("./out.csv", delimiter=";")

print(df)

alt.Chart(df).mark_rect().encode(x="s_start:Q", x2="s_end:Q", y="name:N").show()
