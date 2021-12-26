from src.database import cria_entrada
from src.grafico import cria_grafico_mes_corrente, cria_grafico_ultimos_tres_meses


def menu_grafico():
    print('''
    1.Mostrar o gráfico da luz.
    2.Mostrar o gráfico da água.
    3.Voltar ao menu principal.
    ''')
    escolha = input("Digite uma opção: ")
    match escolha:
        case "1":
            cria_grafico_mes_corrente("Luz")
            cria_grafico_ultimos_tres_meses("Luz")
        case "2":
            cria_grafico_mes_corrente("Agua")
            cria_grafico_ultimos_tres_meses("Agua")
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
            cria_entrada("Luz")
        case "2":
            cria_entrada("Agua")
        case "3":
            menu_grafico()
        case "4":
            quit()
        case _:
            print("******************")
            print("Opção inválida!")
            print("******************")
            menu()
