import pandas as pd


# taxa de crescimento = (presente/passado)^(1/n)- 1
def growthRate(data, variable, date_init=None, date_end=None):
    # se date_init = None, definir como a primeira disponivel

    if date_init == None:
        date_init = data.observationdate.loc[data[variable] > 0].min()
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
