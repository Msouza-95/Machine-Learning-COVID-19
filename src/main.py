from ast import parse
from statistics import mode
from turtle import title
import pandas as pd
import plotly.express as px
from datetime import datetime
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


graphic.plot(dataFrameCountry, "observationdate",
             'confirmed', 'Casos confirmados')


# novos casos por dias (progamação funcional)
dataFrameCountry['newcases'] = list(map(
    lambda x: 0 if(
        x == 0) else dataFrameCountry['confirmed'].iloc[x] - dataFrameCountry['confirmed'].iloc[x-1],
    np.arange(dataFrameCountry.shape[0])
))

graphic.plot(dataFrameCountry, "observationdate",
             'newcases', 'Novos casos por dia no {}'.format(country))

print(dataFrameCountry)

# Mortes

fig = pgo.Figure()

fig.add_trace(
    pgo.Scatter(x=dataFrameCountry.observationdate, y=dataFrameCountry.deaths, name="mortes",
                mode='lines+markers', line={'color': 'red'})
)

fig.update_layout(title='Mortes por  COVID-19 no {}'.format(country))

fig.show()


# taxa de crescimento médio  no pais em todo o periodo.
print(rates.growthRate(dataFrameCountry, 'confirmed'))


# taxa de cresicmento diarios
def dailyGrowthRate(data, variable, date_init=None):
    if date_init == None:
        date_init = data.observationdate.loc[data[variable] > 0].min()
    else:
        date_init = pd.to_datetime(date_init)

    date_end = data.observationdate.max()

    n = (date_end - date_init).days

    # taxa calculada de um dia para o outro
    rate = list(map(
        lambda x: (data[variable].iloc[x] -
                   data[variable].iloc[x-1]) / data[variable].iloc[x-1],
        range(1, n+1)
    ))

    return np.array(rate) * 100


rate_days = dailyGrowthRate(dataFrameCountry, 'confirmed')

print(rate_days)

firstDay = dataFrameCountry.observationdate.loc[dataFrameCountry.confirmed > 0].min(
)

# inserir o plot do grafico.))

#px.line(x =pd.date_range(firstDay, dataFrameCountry.observationdate.max())[1:], y = rate_days, title = 'Taxa de crescimento de casos confirmados no Brasil')


fig2 = pgo.Figure()

fig2.add_trace(
    pgo.Scatter(x=pd.date_range(firstDay, dataFrameCountry.observationdate.max())[1:], y=rate_days, name="taxa",
                mode='lines', line={'color': 'blue'})
)

fig2.update_layout(title='Taxa de crescimento de casos confirmados no {}'.format(country))

fig2.show()


# Predições

confirmed = dataFrameCountry.confirmed
confirmed.index = dataFrameCountry.observationdate

res = seasonal_decompose(confirmed)

figure, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 8))

ax1.plot(res.observed)
ax2.plot(res.trend)
ax3.plot(res.seasonal)
ax4.plot(confirmed.index, res.resid)
ax4.axhline(0, linestyle='dashed', c='black')
plt.savefig('Seasonal.png', format='png')
plt.show()


# analise de series temporais  Arima, essse metódo tenta modela o futuro com predições do passado

model = auto_arima(confirmed)

fig3 = pgo.Figure(pgo.Scatter(
    x=confirmed.index, y=confirmed, name='Observados'
))

fig3.add_trace(pgo.Scatter(
    x=confirmed.index, y=model.predict_in_sample(), name='Preditos'
))

fig3.add_trace(pgo.Scatter(
    x=pd.date_range('2020-05-20', '2020-06-20'), y=model.predict(28), name='Forecast'
))


fig3.update_layout(
    title=' Privisão de casos confirmados no {} na faixa de 30 dias' .format(country))
fig3.show()



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



fig4 = pgo.Figure()

fig4.add_trace(pgo.Scatter(x=forecast.ds, y= forecast.yhat, name = 'Predição'))
fig4.add_trace(pgo.Scatter(x=train.ds, y= train.y, name = 'Observados - Treino'))
fig4.update_layout(title = 'Predições de casos confirmados no {}'.format(country))
fig4.show()

print('finalizou')