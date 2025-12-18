from scraper_amigao import get_all_products
from paginas import gerar_tabela
import os
import webbrowser

def main():
    produtos = get_all_products()
    arquivo = gerar_tabela(produtos)

    caminho = os.path.abspath(arquivo) 
    webbrowser.open(f"file:///{caminho}")

if __name__ == "__main__":
    main()

