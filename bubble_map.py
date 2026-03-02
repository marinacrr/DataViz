'''
Create a bubble map for the Matplotlib Journey course.
Dataset: CO2 emissions per capita in 2021.
'''

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from pyodide.http import open_url


url = "https://raw.githubusercontent.com/JosephBARBIERDARNAL/data-matplotlib-journey/refs/heads/main/world/world.geojson"
world = gpd.read_file(open_url(url))
world = world[world["name"] != "Antarctica"]
world["continent"] = world["continent"].replace("North America", "America")
world["continent"] = world["continent"].replace("South America", "America")

url = "https://raw.githubusercontent.com/JosephBARBIERDARNAL/data-matplotlib-journey/refs/heads/main/CO2/CO2.csv"
df = pd.read_csv(open_url(url))

world = world.merge(
  df,
  left_on="code_adm",
  right_on="ISO",
)
world["centroid"] = world["geometry"].centroid
x = world["centroid"].x
y = world["centroid"].y
s = world["Total"]

color = "#aa8737"

fig, ax = plt.subplots(layout="tight")

world.plot(ax=ax,
           color="lightgrey",
           edgecolor="white",
          linewidth=0.2
          )

ax.scatter(
    x,
    y,
    s=s*10,
    c=color,
    alpha=0.6,
    edgecolor="black",
    linewidth=0.3
)

ax.set_axis_off()

ax.text(x=10, y=92,
        s="Who's leading in per-capita carbon emissions?",
        fontsize=10,
        fontweight="bold",
        ha="center"
        )

ax.text(x=114, y=84,
        s="Data: 2021",
        fontstyle="italic",
        fontsize=6,
        ha="center"
        )


plt.show()
