from ast import parse
from statistics import mode
from turtle import title
import pandas as pd
import numpy as np
import plotly.graph_objects as pgo
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
from Utils import CSV, format, graphic, rates
from fbprophet import Prophet


from pmdarima.arima import auto_arima

dataFrame = CSV.readCsv('Data\covid_19_data.csv')

dataFrame.columns = [format.fixColums(col) for col in dataFrame.columns]

# Informe o país que deseja filtar
country = 'Brazil'
dataFrameCountry = format.filterByCountry(dataFrame, country)


graphic.plot(dataFrameCountry.observationdate,
             dataFrameCountry.confirmed, 'Casos confirmados')


# novos casos por dias (progamação funcional)
dataFrameCountry['newcases'] = list(map(
    lambda x: 0 if(
        x == 0) else dataFrameCountry['confirmed'].iloc[x] - dataFrameCountry['confirmed'].iloc[x-1],
    np.arange(dataFrameCountry.shape[0])
))

graphic.plot( dataFrameCountry.observationdate,
             dataFrameCountry.newcases, 'Novos casos por dia no {}'.format(country))

#print(dataFrameCountry)

# gerar grafico de Mortes

graphic.plotDeathByday(dataFrameCountry, country)

# taxa de crescimento médio  no pais em todo o periodo.
print(rates.growthRate(dataFrameCountry, 'confirmed'))

# taxa de cresicmento diarios

rate_days = rates.dailyGrowthRate(dataFrameCountry, 'confirmed')


firstDay = dataFrameCountry.observationdate.loc[dataFrameCountry.confirmed > 0].min(
)

# grafico de Taxa de crescimento de casos confirmado

graphic.plotGrowthRate(firstDay, dataFrameCountry, rate_days, country)


# Predições

confirmed = dataFrameCountry.confirmed
confirmed.index = dataFrameCountry.observationdate

res = seasonal_decompose(confirmed)

# graficos de Prediction 
graphic.plotPrediction(confirmed, res)


# analise de series temporais  Arima, essse metódo tenta modela o futuro com predições do passado

model = auto_arima(confirmed)

# grafico de Privisão de casos confirmados

graphic.plotForecastOfCases(confirmed,model,country)


train = confirmed.reset_index()[:-5]
test = confirmed.reset_index()[-5:]

# Renomear as colunas

train.rename(columns={'observationdate': 'ds', 'confirmed': 'y'}, inplace=True)
test.rename(columns={'observationdate': 'ds', 'confirmed': 'y'}, inplace=True)

prophet = Prophet(growth='logistic', changepoints=[
                  '2020-03-21', '2020-03-30', '2020-04-25', '2020-04-25', '2020-05-03', '2020-05-10'])


pop = 211463256
train['cap']= pop 

#treinar o modelo 

prophet.fit(train)

future_dates = prophet.make_future_dataframe(periods=200)
future_dates['cap'] = pop
forecast = prophet.predict(future_dates)


 # grafico Predições de casos confirmados
#graphic.plotPredictForecastOfCases(confirmed,train,country)

fig = pgo.Figure()

fig.add_trace(pgo.Scatter(x=forecast.ds, y=forecast.yhat, name='Predição'))
fig.add_trace(pgo.Scatter(x=train.ds, y=train.y,
                name='Observados - Treino'))
fig.update_layout(
    title='Predições de casos confirmados no {}'.format(country))
fig.show()

print('finalizou')