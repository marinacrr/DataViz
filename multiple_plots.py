''' Customized Multiple Plots '''

import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO
from pypalettes import load_cmap

path = "/home/jeanne/Desktop/Dataviz/images"

url = "https://raw.githubusercontent.com/JosephBARBIERDARNAL/data-matplotlib-journey/refs/heads/main/economic/economic.csv"
csv_text = requests.get(url).text
df = pd.read_csv(StringIO(csv_text))

colors = load_cmap("Antique").colors
background_color = "#f2f2f2"

fig, axs = plt.subplots(ncols=3, nrows=3, layout="tight")

for color, country, ax in zip(colors, df["country"].unique(), axs.flat):

    other_df = df[df["country"] != country]
    for other_country in other_df["country"].unique():
        x = other_df.loc[other_df["country"] == other_country, "date"]
        y = other_df.loc[other_df["country"] == other_country, "consumer confidence"]
        ax.plot(x, y, alpha=0.2, color="grey", linewidth=0.5)

    x = df.loc[df["country"] == country, "date"]
    y = df.loc[df["country"] == country, "consumer confidence"]
    ax.plot(x, y, color=color)
    ax.set_ylim(-60, 130)
    ax.set_xticks(
        ["2020-01-01", "2022-01-01", "2024-01-01"],
        labels=[2020, 2022, 2024]
    )

    ax.text(0.6, 0.4, country.title(),
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=8,
            color=color)

    ''' Customization '''
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_color("black")
    ax.spines["left"].set_linewidth(0.4)

    ax.grid(axis="y", color="gray", lw=0.2)
    ax.set_facecolor(background_color)

    ax.tick_params(
        axis="both",
        labelsize=6,
        labelcolor="black",
        color="black"
    )

fig.patch.set_facecolor(background_color)

plt.savefig("%s/multiple_axis.png" %path, bbox_inches='tight', dpi=150)
