import pandas as pd


def readCsv(file):
    # o parse_dates garante que import os campos definidos como data
    return pd.read_csv(file, parse_dates=['ObservationDate', 'Last Update'])


if(__name__ == "__main__"):
    print(readCsv('Data\covid_19_data.csv'))
