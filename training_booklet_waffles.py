'''
Create waffle plots for MaX Training applicants, participants, tutors, and lecturers
'''

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import tight_layout
from pywaffle import Waffle
import requests
from io import StringIO
import sys

path = "/home/jeanne/Desktop/Dataviz/images"

# Access the Google sheet containing the data
sheet_id = "1tpn_nWh9xejlfz1blpEl3YuzYAiiFLW9N0AJotSoL_Q"
gid = "0"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
csv_text = requests.get(url).text
stats = pd.read_csv(StringIO(csv_text))


''' Plot 1 - Applicants and Participants '''
tot_appl = int(stats["applicants"].sum())
tot_part = int(stats["participants"].sum())

ca = "#4D4D4D"
cp = "#FF0000"

values1 = [tot_appl - tot_part, tot_part]
colors1 = [ca, cp]
icons1 = ['user', 'user']
i_s = 12
size = 8


''' Plot 2 - Participants: Male vs Female '''
pm = stats["pm"].sum()
pf = stats["pf"].sum()

cm = "#8DA6CE"
cf = cp

values2 = [pm, pf]
colors2 = (cm, cf)
icons2 = ['person', 'person-dress']


''' Plot 3 - Tutors: Male vs Female '''
tm = stats["tm"].sum()
tf = stats["tf"].sum()
values3 = [tm, tf]


''' Plot 4 - Lecturers: Male vs Female '''
lm = stats["lm"].sum()
lf = stats["lf"].sum()
values4 = [lm, lf]

yy = 1.05

''' FIGURE '''
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(12, 4))
[ax.set_aspect("equal") for ax in (ax1, ax2, ax3, ax4)]

''' Plot 1 - Applicants and Participants '''
Waffle.make_waffle(
    rows=20,
    columns=10,
    values=values1,
    colors=colors1,
    icons=icons1,
    icon_size=i_s-2,
    ax=ax1,
)

ax1.text(x=0, y=yy, s="Applicants\n2142", color=ca, size=size, ha="left")
ax1.text(x=0.5, y=yy, s="Participants\n1106", color=cp, size=size, ha="right")

''' Plot 2 - Participants: Male vs Female '''
Waffle.make_waffle(
  rows=20,
  columns=10,
  values=values2,
  colors=colors2,
  icons=icons2,
  icon_size=i_s,
  ax=ax2,
)

ax2.text(x=0, y=yy, s="male\n811", color=cm, size=size, ha="left")
ax2.text(x=0.5, y=yy, s="female\n295", color=cf, size=size, ha="right")
ax2.text(x=0.25, y=yy+0.1, s="participants", color=ca, size=size, ha="center")

''' Plot 3 - Tutors: Male vs Female '''
Waffle.make_waffle(
  rows=20,
  columns=2,
  values=values3,
  colors=colors2,
  icons=icons2,
  icon_size=i_s,
  ax=ax3,
)

ax3.set_anchor("C")
ax3.text(x=0.022, y=yy, s="m\n47", color=cm, size=size, ha="right")
ax3.text(x=0.05, y=yy, s="f\n17", color=cf, size=size, ha="left")
ax3.text(x=0.04, y=yy+0.1, s="tutors", color=ca, size=size, ha="center")

''' Plot 4 - Lecturers: Male vs Female '''
Waffle.make_waffle(
  rows=20,
  columns=5,
  values=values4,
  colors=colors2,
  icons=icons2,
  icon_size=i_s,
  ax=ax4,
)

ax4.text(x=0.021, y=yy, s="m\n105", color=cm, size=size, ha="center")
ax4.text(x=0.22, y=yy, s="f\n21", color=cf, size=size, ha="center")
ax4.text(x=0.12, y=yy+0.1, s="lecturers", color=ca, size=size, ha="center")

plt.savefig("%s/training_booklet_waffles.png" %path, bbox_inches='tight', dpi=150)
