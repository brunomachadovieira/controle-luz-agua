import sqlite3
import datetime
from src.diversos import converte_data_para_timestamp, inserir_valor_na_tabela


# criar banco
def cria_banco():
    try:
        f = open("sqlite.db")
    except FileNotFoundError:
        con = sqlite3.connect("sqlite.db")
        cur = con.cursor()
        sqlFile = open("dados.sql")
        sqlString = sqlFile.read()
        cur.executescript(sqlString)
        sqlFile.close()
        con.commit()
        con.close()


# cria entrada no banco
def cria_entrada(fornecedor):
    data = input("Digite a data da coleta (formato:dd/mm/aaaa): ")
    valor = input("Digite o valor do medidor:")
    formato = "%d/%m/%Y"
    try:
        datetime.datetime.strptime(data, formato)
    except:
        print("Formato errado!")
        quit()
    data_timestamp = converte_data_para_timestamp(data)
    print("Data: "+data+" Medidor: "+valor)
    dados_estao_certos = input("Os dados estão certos? s/n ")
    if dados_estao_certos == "s":
        inserir_valor_na_tabela(fornecedor, data_timestamp, valor)
    else:
        print("Volte quando tiver certeza!")
        quit()
