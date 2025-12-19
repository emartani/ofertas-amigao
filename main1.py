from scraper1 import extrair_produtos_api
from paginas1 import gerar_tabela_api

def main():
    produtos = extrair_produtos_api()
    arquivo = gerar_tabela_api(produtos)
    print("[DEBUG] HTML gerado:", arquivo)

if __name__ == "__main__":
    main()
