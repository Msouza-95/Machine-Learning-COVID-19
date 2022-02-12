import plotly.express as px
from datetime import datetime

def confirmedCase(data):
    return px.line(data, 'observationdate', 'confirmed',
                   title='Casos confimados {}'.format(data.countryregion))
