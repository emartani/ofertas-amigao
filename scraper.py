from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from classificacao import detectar_categoria  # função inteligente

def extrair_produtos():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless=new")  # modo headless moderno

    driver = webdriver.Chrome(options=options)  # Selenium Manager resolve tudo

    url = "https://www.amigao.com/s/?clubProducts"
    driver.get(url)
    time.sleep(3)

    # Fechar pop-up de cookies se aparecer
    try:
        botao_consentimento = driver.find_element(By.CSS_SELECTOR, "button.modal-cookies-agree")
        botao_consentimento.click()
        time.sleep(2)
    except:
        pass

    # Clicar em "Mostrar Mais" até não existir mais
    while True:
        try:
            botao = driver.find_element(By.CSS_SELECTOR, "a[data-testid='show-more']")
            botao.click()
            time.sleep(3)
        except:
            break

    # Extrair HTML final
    html = driver.page_source
    driver.quit()

    # Usar BeautifulSoup para pegar informações dos produtos
    soup = BeautifulSoup(html, "html.parser")

    produtos = []
    for item in soup.select(".product-card"):
        nome = item.select_one(".product-card-name")
        desconto = item.select_one(".product-card-discount-badge-value")
        preco_clube = item.select_one(".product-card-club-price")
        preco_antigo = item.select_one(".product-card-old-price span")
        preco_novo = item.select_one(".product-card-new-price")

        # Converter desconto para número (ex: "34%" -> 34)
        desconto_valor = 0
        if desconto:
            txt = desconto.get_text(strip=True)
            try:
                desconto_valor = int(txt.replace("%", "").strip()) if "%" in txt else 0
            except:
                desconto_valor = 0

        nome_texto = nome.get_text(strip=True) if nome else "Sem nome"
        categoria = detectar_categoria(nome_texto)  # <<< classificação automática

        produtos.append({
            "nome": nome_texto,
            "desconto": desconto.get_text(strip=True) if desconto else "",
            "desconto_valor": desconto_valor,
            "preco_clube": preco_clube.get_text(strip=True).replace(" no + Amigo", "") if preco_clube else "",
            "preco_antigo": preco_antigo.get_text(strip=True) if preco_antigo else "",
            "preco_novo": preco_novo.get_text(strip=True) if preco_novo else "Sem preço",
            "categoria": categoria
        })

    return produtos

if __name__ == "__main__":
    lista = extrair_produtos()
    for p in lista[:20]:
        print(p["nome"], "=>", p["categoria"])
