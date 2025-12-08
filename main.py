from scraper import extrair_produtos
from paginas import gerar_tabela

def main():
    produtos = extrair_produtos()
    gerar_tabela(produtos)

if __name__ == "__main__":
    main()

