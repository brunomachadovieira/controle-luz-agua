from src.database import cria_banco
from src.menu import menu


def main():
    cria_banco()
    print("Vai dar certo!")
    menu()


if __name__ == "__main__":
    main()
