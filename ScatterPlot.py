import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


path = '/home/jeanne/Desktop/Dataviz'

''' Customize '''
background_color = "#252647"
white = "#f1f1f1"
light_grey = "#bab9b9"
dark_grey = '#242421'

lbs = 12 #labelsize
tks = 14 #ticksize


''' Read the CSV file in Dataframe '''
data = '%s/datasets/capita.csv' %path
footprint = pd.read_csv(data)
first_row = footprint.iloc[0]

x = footprint["gdpCapita"]
y = footprint["footprint"]
s = footprint["populationMillions"]
r = footprint["region"]

# Create a DataFrame for sorting
plot_data = pd.DataFrame({
    "x": x,
    "y": y,
    "s": s,
    "r": r
})

# Sort by size (s) in descending order so that larger bubbles go behind
plot_data = plot_data.sort_values("s", ascending=False)

# Plot sorted data
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(
    plot_data["x"],
    plot_data["y"],
    s=plot_data["s"] * 4,
    alpha=0.4,
    c="#477eed",
    edgecolor="#477eed"
)

subset = footprint[s > 100]
for i, row in subset.iterrows():
    country = row["country"]
    x_value = row["gdpCapita"]
    y_value = row["footprint"]

# Offsets to move the text a bit
    offset_x = 0
    offset_y = 0.5

    ax.text(
        x=x_value + offset_x, y=y_value + offset_y, s=country,
        ha="center", va="center",
        color=dark_grey, size=lbs,
        fontweight="bold"
    )

''' X label '''
ax.text(x=82000, y=0.5,
        s="GDP\nper Capita",
        color=dark_grey, size=lbs
        )

''' Y label '''
ax.text(x=0, y=12.5,
        s="Global hectares\nper person",
        color=dark_grey, size=lbs
        )

''' X-axis tick labels'''
location = [20_000, 40_000, 60_000, 80_000, 100_000]
labels = ["$20k", "$40k", "$60k", "$80k", "$100k"]
ax.set_xticks(location, labels=labels)

''' Y-axis tick labels'''
location = [0, 4, 8, 12]
ax.set_yticks(location, labels=location)

ax.tick_params(length=0)
ax.tick_params(axis="both", labelsize=tks, labelcolor=dark_grey)

ax.set_ylim(0, 14)
ax.set_xlim(-2000, 86_000)

ax.grid(True, c=light_grey, ls='--', alpha=0.6)
ax.spines[["top", "right"]].set_visible(False)
ax.spines[["left", "bottom"]].set_color(dark_grey)


''' Legend '''
legend_sizes = [50, 150, 300]
legend_bubbles = [size * 4 for size in legend_sizes]

legend_elements = [
    Line2D(
        [0], [0],
        marker='o',
        color='w',
        label=f"{size}M",
        markerfacecolor="#477eed",
        markeredgecolor="#477eed",
        alpha=0.4,
        markersize=(bubble_size ** 0.5),
        markeredgewidth=1
    )
    for size, bubble_size in zip(legend_sizes, legend_bubbles)
]

ax.legend(
    handles=legend_elements,
    title="Population (Millions)",
    loc="upper right",
    ncol=len(legend_elements),  # one row
    handletextpad=1.,
    columnspacing=2.,
    frameon=True,
    borderaxespad=-0.5,
    labelspacing=2.0,
    handlelength=2.5
)

fig.suptitle("More capita, more footprint",
             fontsize=2*lbs, color=dark_grey
             )
#plt.show()
plt.savefig('%s/images/FinalBoss.png' %path, dpi=300)
