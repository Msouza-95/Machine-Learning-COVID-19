from numpy import tile
import plotly.express as px
from datetime import datetime


def plot(data, myX, myY, myTitle):
    return px.line(data, x = myX, y = myY, title ='{} {}'.format(myTitle,data.countryregion))
