import datetime
import sqlite3
import pandas as pd


def converte_data_para_timestamp(data):
    data_timestamp = int(datetime.datetime.strptime(data, '%d/%m/%Y')
                         .strftime("%s"))
    return data_timestamp


def inserir_valor_na_tabela(fornecedor, data_timestamp, valor):
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    cur.execute("INSERT INTO tabela_Luz VALUES ("+str(data_timestamp) +
                ", "+str(valor)+")")
    print("Incluido na tabela do medidor da "+fornecedor+" com sucesso!")
    con.commit()
    con.close()


def primeiro_dia_do_mes_corrente():
    hoje_padrao_americano = datetime.date.today()
    primeiro_dia_mes = "01"+hoje_padrao_americano.strftime("/%m/%Y")
    primeiro_dia_mes = converte_data_para_timestamp(primeiro_dia_mes)
    return primeiro_dia_mes


def monta_dataframe_mes_corrente(fornecedor):
    primeiro_dia_mes = str(primeiro_dia_do_mes_corrente())
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    cur.execute(
        "CREATE VIEW Mes_Corrente_"+fornecedor+" AS SELECT * FROM tabela_" + fornecedor+" WHERE data_medidor > "+primeiro_dia_mes+";")
    df = pd.read_sql_query(
        "SELECT strftime('%d/%m/%Y', date(data_medidor, 'unixepoch', 'localtime')), numero_medidor from Mes_Corrente_"+fornecedor+"", con)
    cur.execute("DROP VIEW Mes_Corrente_"+fornecedor+"")
    con.commit()
    con.close()
    return df


def monta_dataframe_tres_ultimos_meses(fornecedor):
    ultimos_tres_meses = int(primeiro_dia_do_mes_corrente()) - 7776000
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    cur.execute(
        "CREATE VIEW Mes_Tres_Ultimos_"+fornecedor+" AS SELECT * FROM tabela_" + fornecedor+" WHERE data_medidor > "+str(ultimos_tres_meses)+";")
    df = pd.read_sql_query(
        "SELECT strftime('%d/%m/%Y', date(data_medidor, 'unixepoch', 'localtime')), numero_medidor from Mes_Tres_Ultimos_"+fornecedor+"", con)
    cur.execute("DROP VIEW Mes_Tres_Ultimos_"+fornecedor+"")
    con.commit()
    con.close()
    return df
