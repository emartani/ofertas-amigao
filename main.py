from scraper import extrair_produtos
from paginas import gerar_tabela

def main():
    produtos = extrair_produtos()
    print(f"Total de produtos carregados: {len(produtos)}")
    print("Exemplos:", [p["nome"] for p in produtos[:5]])

    gerar_tabela(produtos)

if __name__ == "__main__":
    main()

