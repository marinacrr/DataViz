'''
Waffle chart
'''

import matplotlib.pyplot as plt
import pandas as pd
from pyodide.http import open_url
import requests
from pywaffle import Waffle
import numpy as np

# dataset 1
url = "https://raw.githubusercontent.com/JosephBARBIERDARNAL/data-matplotlib-journey/refs/heads/main/storms/storms.csv"
df_storms = pd.read_csv(open_url(url))

colors = {
    "hurricane": "#fcbf49",
    "tropical depression": "#f77f00",
    "tropical storm": "#d62828",
    "tropical wave": "#003049"
}

storms = list(colors.keys())

# List of years
years = np.sort(df_storms["year"].unique())

# Create grid of subplots
n_years = len(years)
cols = 4
rows = int(np.ceil(n_years / cols))

fig, axes = plt.subplots(rows, cols, figsize=(12, 10))
axes = axes.flatten()

for i, year in enumerate(years):
    ax = axes[i]

    # Count storm type for this year
    counts = {
        storm: df_storms[(df_storms["year"] == year) &
                         (df_storms["status"] == storm)]["n"].sum()
        for storm in storms
    }

    # Create waffle chart for this year
    Waffle.make_waffle(
        rows=10,
        columns=20,
        values=counts,
        colors=[colors[s] for s in storms],
        ax=ax
    )

    leg = ax.get_legend()
    if leg is not None:
        leg.remove()

    ax.set_title(str(year))

# Hide any empty axes (if grid > number of years)
for j in range(i+1, len(axes)):
    axes[j].axis("off")

fig.legend(
    handles=[plt.Rectangle((0,0),1,1, color=colors[s]) for s in storms],
    labels=storms,
    loc="center",
    bbox_to_anchor=(0.76, 0.10),
    ncol=1,
    fontsize=16
)

fig.suptitle("Distribution of Storms per Year", fontsize=26)
plt.tight_layout()
plt.show()
