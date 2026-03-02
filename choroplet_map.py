''' 
Choroplet map for the Matplotlib Journey course. 
Dataset: CO2 emissions per capita for each country in the world as of 2021.
'''

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib as mpl

path = "/home/jeanne/Desktop/Dataviz/images"
style = dict(fontsize=18, fontweight="bold")

world = gpd.read_file("https://raw.githubusercontent.com/JosephBARBIERDARNAL/data-matplotlib-journey/refs/heads/main/world/world.geojson")
df = pd.read_csv("https://raw.githubusercontent.com/JosephBARBIERDARNAL/data-matplotlib-journey/refs/heads/main/CO2/CO2.csv")

world = world.merge(df, left_on="code_adm", right_on="ISO")

eu_codes = [
    "AUT","BEL","BGR","HRV","CYP","CZE","DNK","EST","FIN","FRA",
    "DEU","GRC","HUN","IRL","ITA","LVA","LTU","LUX","MLT",
    "NLD","POL","PRT","ROU","SVK","SVN","ESP","SWE"
]
europe = world[world["ISO"].isin(eu_codes)]

# Top 5 emitters within EU
top5 = europe.nlargest(5, "Total")

# colormap
cmap = plt.cm.viridis
vmin = europe["Total"].min()
vmax = europe["Total"].max()
norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)

projection = ccrs.PlateCarree()
fig = plt.figure(figsize=(12, 10))
ax = plt.axes(projection=projection)

# Europe extent
ax.set_extent([-25, 45, 34, 72], crs=ccrs.PlateCarree())

# Ocean color
ax.set_facecolor("#dbe9f6")

# Choropleth
europe.plot(
    column="Total",
    ax=ax,
    transform=ccrs.PlateCarree(),
    cmap="viridis",
    linewidth=0.5,
    edgecolor="white",
    legend=True,
    legend_kwds={
        "label": "CO₂ emissions per capita (tons)",
        "orientation": "horizontal",
        "shrink": 0.35,
        "pad": 0.02
    }
)

# Highlight top 5
top5.plot(
    ax=ax,
    transform=ccrs.PlateCarree(),
    facecolor="none",
    edgecolor="yellow",
    linewidth=2
)

# Add rank numbers instead of ISO
for i, (_, row) in enumerate(top5.iterrows(), 1):
    centroid = row.geometry.centroid
    ax.text(
        centroid.x,
        centroid.y,
        str(i),
        transform=ccrs.PlateCarree(),
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
        color="yellow"
    )

ax.set_axis_off()
ax.text(x=-23, y=70,
        s="Highest CO₂ emitters in EU",
        **style)

plt.savefig("%s/choroplet.png" %path, bbox_inches='tight', dpi=150)
