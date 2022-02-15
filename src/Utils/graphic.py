from numpy import tile
import plotly.express as px
import plotly.graph_objects as pgo
import pandas as pd
import matplotlib.pyplot as plt


def plot(data, myX, myY, myTitle):
    px.line(data, x=myX, y=myY, title='{} {}'.format(
        myTitle, data.countryregion))

    return


def plotDeathByday(data, country):
    fig = pgo.Figure()

    fig.add_trace(
        pgo.Scatter(x=data.observationdate, y=data.deaths, name="mortes",
                    mode='lines+markers', line={'color': 'red'})
    )

    fig.update_layout(title='Mortes por  COVID-19 no {}'.format(country))

    fig.show()

    return


def plotGrowthRate(firstDay, dataFrameCountry, rate_days, country):

    fig = pgo.Figure()

    fig.add_trace(
        pgo.Scatter(x=pd.date_range(firstDay, dataFrameCountry.observationdate.max())[1:], y=rate_days, name="taxa",
                    mode='lines', line={'color': 'blue'})
    )

    fig.update_layout(
        title='Taxa de crescimento de casos confirmados no {}'.format(country))

    fig.show()


def plotPrediction(confirmed, res):

    figure, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 8))
    
    ax1.plot(res.observed)
    ax2.plot(res.trend)
    ax3.plot(res.seasonal)
    ax4.plot(confirmed.index, res.resid)
    ax4.axhline(0, linestyle='dashed', c='black')
    plt.savefig('Seasonal.png', format='png')
    plt.show()
    return
