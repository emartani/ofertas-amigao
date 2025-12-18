from scraper import extrair_produtos
from paginas import gerar_tabela
import os
import webbrowser

def main():
    produtos = extrair_produtos()
    arquivo = gerar_tabela(produtos)

    caminho = os.path.abspath(arquivo) 
    webbrowser.open(f"file:///{caminho}")

if __name__ == "__main__":
    main()

