'''
Create a multiple axis figure to showcase MaX codes citation trend over time.
For each code, citations have been renormalized to the max value.
'''

import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO
from pypalettes import load_cmap

# Extremes for annotation
extremes = {
    "QE": (342, 3400),
    "SIESTA": (591, 858),
    "YAMBO": (28, 141),
    "BigDFT": (12, 34),
    "FLEUR": (2, 22)
}

path = "/home/jeanne/Desktop/Dataviz/images"
colors = load_cmap("Antique").colors
style_other = dict(color="grey", alpha=0.4, linewidth=0.5)
style_code = dict(ha="center", va="center", fontsize=8, weight="bold")
style_grid = dict(color="gray", lw=0.2, linestyle="dashed")
style_extremes = dict(ha="center", va="center", fontsize=6, weight="bold")

# Load data from Google Sheet
sheet_id = "1hB-FFTGNUH8kjeS0Vxs0wse4X-qcsVJPBgkVliMOVZ0"
gid = "2069501151"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
csv = requests.get(url).text
data = pd.read_csv(StringIO(csv))

years = data["Year"]
max_codes = data.columns.drop("Year")

fig, axs = plt.subplots(ncols=2, nrows=3, layout="tight")

for color, code, ax in zip(colors, max_codes, axs.flat):

    # plot all codes on background
    other_codes = max_codes.drop(code)
    ax.plot(years, data[other_codes], **style_other)

    # highlight current code
    ax.plot(years, data[code], color=color, linewidth=2)
    ax.text(0.94, 0.1, code, transform=ax.transAxes, color=color, **style_code)

    # Annotate extremes
    series = data[code]
    first_idx = series.first_valid_index()
    last_idx  = series.last_valid_index()

    if last_idx is not None:
        ax.text(
            data.loc[last_idx, "Year"]-0.3,
            series.loc[last_idx]+0.1,
            str(extremes[code][0]),
            color=color,
            **style_extremes
        )

    if first_idx is not None:
        ax.text(
            data.loc[first_idx, "Year"]+0.5,
            series.loc[first_idx]-0.1,
            str(extremes[code][1]),
            color=color,
            **style_extremes
        )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("black")
    ax.spines["bottom"].set_linewidth(0.5)

    ax.grid(axis="both", **style_grid)

    ax.set_yticks([])
    ax.set_ylabel("")
    ax.set_xlim(2009, 2026)
    ax.set_ylim(-0.1, 1.1)
    ax.tick_params(axis="x", labelsize=6)

# Remove unused subplot
for ax in axs.flat[len(max_codes):]:
    ax.remove()

plt.savefig("%s/max_cits_multiple_axis.png" %path, bbox_inches='tight', dpi=150)
