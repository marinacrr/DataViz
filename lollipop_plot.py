'''
Lollipop plot
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from io import StringIO

# Load dataset
url = "https://raw.githubusercontent.com/JosephBARBIERDARNAL/data-matplotlib-journey/refs/heads/main/storms/storms.csv"
csv_text = requests.get(url).text
df_storms = pd.read_csv(StringIO(csv_text))

colors = {
    "hurricane": "#fcbf49",
    "tropical depression": "#f77f00",
    "tropical storm": "#d62828",
    "tropical wave": "#003049"
}

# Unique years and types
years = np.sort(df_storms["year"].unique())
years = np.array(years)
order = ["tropical wave", "tropical depression", "tropical storm", "hurricane"]
types = [t for t in order if t in df_storms["status"].unique()]


shift = 0
fig, ax = plt.subplots(figsize=(12, 4))
for s in types:
    counts = [df_storms[(df_storms["year"]==y) & (df_storms["status"]==s)]["n"].sum() for y in years]
    ax.scatter(years + shift, counts, s=counts, color=colors.get(s), label=s)
    ax.vlines(years + shift, ymin=0, ymax=counts, linestyle='--', linewidth=2, color=colors.get(s))
    shift += 0.2

ax.set_yticks(range(0, 601, 200))
ax.set_title("How many Storms per Year?")
ax.legend(loc='upper left', bbox_to_anchor=(0, 1))
plt.show()
