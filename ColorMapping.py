'''
Color-mapping using True-False condition
'''

import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO

# Load dataset
url = "https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/refs/heads/master/static/data/iris.csv"
csv_text = requests.get(url).text
iris = pd.read_csv(StringIO(csv_text))

x = iris["sepal_length"]
y = iris["sepal_width"]

color_mapping = {
  True: "#78290f",
  False: "lightgrey"
}

colors = (iris["species"] == "virginica").map(color_mapping)

fig, ax = plt.subplots()
ax.scatter(x, y, color=colors, s=200)
plt.show()
