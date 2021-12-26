import sqlite3
import datetime
import plotly.express as px
import pandas as pd
import sqlite3


# criar banco
def criaBanco():
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


# criar menu
def menuGrafico():
    print('''
    1.Mostrar o gráfico da luz.
    2.Mostrar o gráfico da água.
    3.Voltar ao menu principal.
    ''')
    escolha = input("Digite uma opção: ")
    match escolha:
        case "1":
            criaGraficoMesAtual("Luz")
            criaGraficoTresMeses("Luz")
        case "2":
            criaGraficoMesAtual("Agua")
            criaGraficoTresMeses("Agua")
        case "3":
            menu()
        case _:
            print("Opção invalida!")
            quit()


def menu():
    print('''
    1.Adicionar registro da luz.
    2.Adicionar registro da água.
    3.Criar gráfico.
    4.Sair
    ''')
    escolha = input("Digite uma opção: ")
    match escolha:
        case "1":
            criaEntrada("Luz")
        case "2":
            criaEntrada("Agua")
        case "3":
            menuGrafico()
        case "4":
            quit()
        case _:
            print("******************")
            print("Opção inválida!")
            print("******************")
            menu()

# cria entrada no banco


def criaEntrada(fornecedor):
    data = input("Digite a data da coleta (formato:dd/mm/aaaa): ")
    formato = "%d/%m/%Y"
    try:
        datetime.datetime.strptime(data, formato)
    except:
        print("Formato errado!")
        quit()
    valor = input("Digite o valor do medidor:")
    dataUnixTime = int(datetime.datetime.strptime(
        data, '%d/%m/%Y').strftime("%s"))
    print('Data: ' + data + ' UnixTime: ' +
          str(dataUnixTime) + ' Medidor: ' + valor)
    dadosEstaoCertos = input("Os dados estão certos? s/n ")
    if dadosEstaoCertos == "s":
        con = sqlite3.connect("sqlite.db")
        cur = con.cursor()
        if fornecedor == "Luz":
            cur.execute("INSERT INTO tabela_Luz VALUES (" +
                        str(dataUnixTime) + ", " + str(valor) + ")")
            print("Incluido na tabela do medidor da luz com sucesso!")
        else:
            cur.execute("INSERT INTO tabela_Agua VALUES (" +
                        str(dataUnixTime) + ", " + str(valor) + ")")
            print("Incluido na tabela do medidor de água com sucesso!")
        con.commit()
        con.close()
    else:
        print("Volte quando tiver certeza!")
        quit()


# cria grafico
dataUS = datetime.date.today()
data = dataUS.strftime("%d/%m/%Y")


def dataUnixTime(data):
    dataUnixTime = int(datetime.datetime.strptime(
        data, '%d/%m/%Y').strftime("%s"))
    return dataUnixTime


def criaGraficoMesAtual(fornecedor):
    mesAnoAtual = dataUS.strftime("%m/%Y")
    primeiroDiaMes = "01/"+mesAnoAtual+""
    primeiroDiaMes = dataUnixTime(primeiroDiaMes)
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    cur.execute("CREATE VIEW Mes_Corrente_"+str(fornecedor)+" AS SELECT * FROM tabela_" +
                str(fornecedor)+" WHERE data_medidor > "+str(primeiroDiaMes)+";")
    df = pd.read_sql_query(
        "SELECT strftime('%d/%m/%Y', date(data_medidor, 'unixepoch', 'localtime')), numero_medidor from Mes_Corrente_"+str(fornecedor)+"", con)
    cur.execute("DROP VIEW Mes_Corrente_"+fornecedor+"")
    con.commit()
    con.close()
    pd.options.plotting.backend = "plotly"
    figMesAtual = df.plot(x="strftime('%d/%m/%Y', date(data_medidor, 'unixepoch', 'localtime'))", y="numero_medidor", title="Mês Corrente",
                          labels={"strftime('%d/%m/%Y', date(data_medidor, 'unixepoch', 'localtime'))": "Data", "numero_medidor": "Medidor"})
    figMesAtual.show(renderer="browser")
    # return figMesAtual


def criaGraficoTresMeses(fornecedor):
    mesAnoAtual = dataUS.strftime("%m/%Y")
    primeiroDiaMes = "01/"+mesAnoAtual+""
    primeiroDiaMes = dataUnixTime(primeiroDiaMes)
    ultimosTresMeses = primeiroDiaMes - 7776000
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    cur.execute("CREATE VIEW Mes_Tres_Ultimos_"+fornecedor+" AS SELECT * FROM tabela_" +
                fornecedor+" WHERE data_medidor > "+str(ultimosTresMeses)+";")
    df = pd.read_sql_query(
        "SELECT strftime('%d/%m/%Y', date(data_medidor, 'unixepoch', 'localtime')), numero_medidor from Mes_Tres_Ultimos_"+fornecedor+"", con)
    cur.execute("DROP VIEW Mes_Tres_Ultimos_"+fornecedor+"")
    con.commit()
    con.close()
    pd.options.plotting.backend = "plotly"
    figUltimosTresMeses = df.plot(x="strftime('%d/%m/%Y', date(data_medidor, 'unixepoch', 'localtime'))", y="numero_medidor", title="Últimos três meses",
                                  labels={"strftime('%d/%m/%Y', date(data_medidor, 'unixepoch', 'localtime'))": "Data", "numero_medidor": "Medidor"})
    figUltimosTresMeses.show(renderer="browser")
    # return figUltimosTresMeses

# cria dash


def main():
    criaBanco()
    print("Vai dar certo!")
    menu()


if __name__ == "__main__":
    main()
