import pandas as pd
from src.diversos import monta_dataframe_tres_ultimos_meses, monta_dataframe_mes_corrente


def cria_grafico_mes_corrente(fornecedor):
    df = monta_dataframe_mes_corrente(fornecedor)

    pd.options.plotting.backend = "plotly"
    figMesAtual = df.plot(x="strftime('%d/%m/%Y', date(data_medidor, 'unixepoch', 'localtime'))", y="numero_medidor", title="Mês Corrente",
                          labels={"strftime('%d/%m/%Y', date(data_medidor, 'unixepoch', 'localtime'))": "Data", "numero_medidor": "Medidor"})
    # figMesAtual.show(renderer="browser")
    return figMesAtual


def cria_grafico_ultimos_tres_meses(fornecedor):
    df = monta_dataframe_tres_ultimos_meses(fornecedor)

    pd.options.plotting.backend = "plotly"
    figUltimosTresMeses = df.plot(x="strftime('%d/%m/%Y', date(data_medidor, 'unixepoch', 'localtime'))", y="numero_medidor", title="Últimos três meses",
                                  labels={"strftime('%d/%m/%Y', date(data_medidor, 'unixepoch', 'localtime'))": "Data", "numero_medidor": "Medidor"})
    # figUltimosTresMeses.show(renderer="browser")
    return figUltimosTresMeses
