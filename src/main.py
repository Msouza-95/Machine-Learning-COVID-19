from ast import parse
from statistics import mode
from turtle import title
import pandas as pd
import plotly.express as px
from datetime import datetime
import numpy as np
import plotly.graph_objects as pgo


from Utils import CSV, format, graphic

dataFrame = CSV.readCsv('Data\covid_19_data.csv')

dataFrame.columns = [format.fixColums(col) for col in dataFrame.columns]

# Informe o país que deseja filtar
dataFrameCountry = format.filterByCountry(dataFrame, 'Brazil')



graphic.plot(dataFrameCountry,"observationdate" ,'confirmed','Casos confirmados') 


# novos casos por dias (progamação funcional)
dataFrameCountry['newcases'] = list(map(
    lambda x:0 if(x==0) else dataFrameCountry['confirmed'].iloc[x] - dataFrameCountry['confirmed'].iloc[x-1],
    np.arange(dataFrameCountry.shape[0])
))

graphic.plot(dataFrameCountry,"observationdate" ,'newcases','Novos casos por dia')

print(dataFrameCountry) 

# Mortes 

fig = pgo.Figure()

fig.add_trace(
    pgo.Scatter(x = dataFrameCountry.observationdate , y = dataFrameCountry.deaths, name="mortes",
                mode='lines+markers', line={'color':'red'})
)

fig.update_layout(title='Mortes por  COVID-19 no Brasil')

fig.show()

# taxa de crescimento = (presente/passado)^(1/n)- 1

def growthRate(data, variable , date_init = None, date_end = None):
    # se date_init = None, definir como a primeira disponivel
    
    if date_init == None:
        date_init = data.observationdate.loc[data[variable]>0].min()
    else:
        date_init = pd.to_datetime(date_init)
    
    # se date_end = None, definir como a ultima disponivel
    if date_end == None:
        date_end = data.observationdate.iloc[-1]
    else:
        date_end = pd.to.datetime(date_end)
        
    # definir os valores do presente e passado 
    
    past = data.loc[data.observationdate == date_init, variable].values[0]
    present = data.loc[data.observationdate == date_end, variable].values[0]
    
    # Definir o números de prontos no tempo que vamos definir
    n = (date_end - date_init).days
  
    rate = (present/past)**(1/n) - 1
    
    return rate*100


# taxa de crescimento médio  no pais em todo o periodo. 
print(growthRate(dataFrameCountry, 'confirmed'))


# taxa de cresicmento diarios 
def dailyGrowthRate(data, variable , date_init = None) :
    if date_init == None:
        date_init = data.observationdate.loc[data[variable]>0].min()
    else:
        date_init = pd.to_datetime(date_init)
        
    date_end = data.observationdate.max()
    
    n = (date_end - date_init).days
    
    #taxa calculada de um dia para o outro
    rate = list(map(
        lambda x : (data[variable].iloc[x] - data[variable].iloc[x-1])/ data[variable].iloc[x-1],
        range(1, n+1)
    ))
    
    return np.array(rate) * 100


rate_days = dailyGrowthRate( dataFrameCountry, 'confirmed')

print(rate_days)

firstDay = dataFrameCountry.observationdate.loc[dataFrameCountry.confirmed > 0].min()

# inserir o plot do grafico.))

#px.line(x =pd.date_range(firstDay, dataFrameCountry.observationdate.max())[1:], y = rate_days, title = 'Taxa de crescimento de casos confirmados no Brasil')


    


