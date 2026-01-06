'''
Create Lollipop plot for MaX Training Booklet
'''

import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO
import sys
import numpy as np

path = "/home/jeanne/Desktop/Dataviz/images"

# Access Google sheet
sheet_id = "1tpn_nWh9xejlfz1blpEl3YuzYAiiFLW9N0AJotSoL_Q"
gid = "0"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
csv_text = requests.get(url).text
stats = pd.read_csv(StringIO(csv_text))

schools = stats["schools"]
n_schools = np.arange(len(stats))
y = np.ones(len(stats))

part = stats["participants"]
dates = stats["date"]
types = stats["type"]
codes = stats["code"]
venue = ["online" if v == "online" else "onsite" for v in stats["venue"]]


''' colors '''
c_online = "#4D4D4D"
c_onsite = "#FF0000"
c_hack = "#0D48F2"

color_mapping = {
  True: c_online,
  False: c_onsite
}
colors = (stats["venue"] == "online").map(color_mapping)


''' custom '''
ymin = 0.9
ymax = 1.22
yy = 1.15
l = 1
a = 1.6
size = 14
x0 = len(stats)/2 - 1.5
style = dict(size=size, ha="center", fontweight="bold")

''' FIGURE '''
fig, ax  = plt.subplots(figsize=(14, 3))

ax.vlines(
    x=n_schools,
    ymin=ymin,
    ymax=y,
    color=colors,
    linestyles="dashed",
    linewidth=l
)

ax.scatter(
    n_schools,
    y,
    color=colors,
    s=part ** a,
    zorder=3,
    alpha=0.8
)

''' highlight hackathons'''
for n, t in enumerate(types):
    if t == "H":
        ax.scatter(
            n,
            1,
            s=(part[n] + 20) ** a,
            facecolors='none',
            edgecolors=c_hack,
            linewidths=2,
            zorder=3,
        )

''' Legend '''
ax.text(x=x0, y=yy, s="on-site", color=c_onsite, **style)
ax.text(x=x0 + 2, y=yy, s="online", color=c_online, **style)

ax.scatter(x=x0 + 3.6, y=yy+0.005, facecolor='none', edgecolor=c_hack, s=100, linewidth=2)
ax.text(x=x0 + 5, y=yy, s="hackathon", color=c_hack, **style)

ax.scatter(x=x0 -0.5 + 8, y=yy+0.005, facecolor='none', edgecolor=c_online, s=50**a, linewidth=1)
ax.scatter(x=x0 -0.5 + 8.18, y=yy+0.005, facecolor='none', edgecolor=c_online, s=100**a, linewidth=1)
ax.scatter(x=x0 -0.5 + 8.34, y=yy+0.005, facecolor='none', edgecolor=c_online, s=150**a, linewidth=1)
ax.text(x=x0 + 9.6, y=yy, s="attendees", color=c_online, **style)

ax.set_ylim(ymin, ymax)
ax.set_yticks([])

ax.set_xticks(n_schools)
ax.set_xticklabels(dates, rotation=45, ha="right")
for tick_label, c in zip(ax.get_xticklabels(), colors):
    tick_label.set_color(c)

ax.spines[["top", "right", "bottom", "left"]].set_visible(False)

plt.savefig("%s/training_booklet_lollipops.png" %path, bbox_inches='tight', dpi=150)
