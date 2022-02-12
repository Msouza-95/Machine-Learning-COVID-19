from ast import parse
import numpy as np


import plotly.graph_objects as pgo

from Utils import CSV, format, graphic


dataFrame = CSV.readCsv('Data\covid_19_data.csv')

dataFrame.columns = [format.fixColums(col) for col in dataFrame.columns]

#Informe o país que deseja filtar
dataFrameCountry = format.filterByCountry( dataFrame, 'Brazil') 


graphic.confirmedCase(dataFrameCountry)


