import re

# Transforma o nome das colunas em Minúsculo e remove caracteres especiais


def fixColums(col):
    return re.sub(r"[/| ]", "", col).lower()


def filterByCountry(dataFrame, country):

    return dataFrame.loc[
        (dataFrame.countryregion == country) &
        (dataFrame.confirmed > 0)
    ]


if __name__ == '__main__':

    print(fixColums('AAA/xds '))
