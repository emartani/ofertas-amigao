DEBUG = False  # coloque False para desativar

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from classificacao import detectar_categoria
import os

# ============================================================
# SISTEMA DE LOG
# ============================================================

debug_log = open("debug_log.txt", "w", encoding="utf-8")

def debug_print(*args):
    if DEBUG:
        texto = " ".join(str(a) for a in args)
        print(texto)
        debug_log.write(texto + "\n")

def debug_screenshot(driver, nome="debug"):
    if DEBUG:
        caminho = f"debug_{nome}.png"
        driver.save_screenshot(caminho)
        debug_print(f"[DEBUG] Screenshot salva: {caminho}")

def debug_html_bs4(element, idx):
    if DEBUG:
        html = element.prettify()
        debug_print(f"\n===== DEBUG HTML PRODUTO #{idx} =====")
        debug_log.write(html + "\n")
        debug_print("===== FIM HTML =====\n")


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def extrair_produtos():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    #options.add_argument("--headless=new")  # modo headless moderno

    driver = webdriver.Chrome(options=options)

    url = "https://www.amigao.com/s/?clubProducts"
    debug_print("[DEBUG] Acessando URL:", url)
    driver.get(url)
    time.sleep(50)

    debug_screenshot(driver, "pagina_inicial")

    # Fechar pop-up de cookies se aparecer
    try:
        botao_consentimento = driver.find_element(By.CSS_SELECTOR, "button.modal-cookies-agree")
        botao_consentimento.click()
        time.sleep(2)
        debug_print("[DEBUG] Pop-up de cookies fechado")
    except:
        debug_print("[DEBUG] Nenhum pop-up de cookies encontrado")

    # Clicar em "Mostrar Mais" até não existir mais
    from selenium.common.exceptions import TimeoutException

    produtos_anteriores = 0
    while True:
        try:
            botao = driver.find_element(By.CSS_SELECTOR, "a[data-testid='show-more']")
            botao.click()
            time.sleep(3)

            # conta produtos atuais
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            cards = soup.select(".product-card")
            total = len(cards)

            if total == produtos_anteriores:
                debug_print("[DEBUG] Nenhum produto novo carregado, encerrando loop")
                break
            produtos_anteriores = total

        except TimeoutException:
            debug_print("[DEBUG] Timeout - não há mais botão")
            break
        except Exception:
            debug_print("[DEBUG] Não há mais 'Mostrar Mais'")
            break


    debug_screenshot(driver, "pagina_final")

    # Extrair HTML final
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    cards = soup.select(".product-card")
    debug_print(f"[DEBUG] Total de produtos encontrados: {len(cards)}")

    produtos = []

    # ============================================================
    # LOOP DOS PRODUTOS
    # ============================================================

    for idx, item in enumerate(cards, start=1):

        # HTML bruto do produto
        debug_html_bs4(item, idx)

        nome = item.select_one(".product-card-name")
        desconto = item.select_one(".product-card-discount-badge-value")
        preco_clube = item.select_one(".product-card-club-price")
        preco_antigo = item.select_one(".product-card-old-price span")
        preco_novo = item.select_one(".product-card-new-price")

        nome_texto = nome.get_text(strip=True) if nome else "Sem nome"

        # Converter desconto
        desconto_valor = 0
        if desconto:
            txt = desconto.get_text(strip=True)
            try:
                desconto_valor = int(txt.replace("%", "").strip()) if "%" in txt else 0
            except:
                desconto_valor = 0

        # Debug dos valores capturados
        debug_print(f"\n===== PRODUTO #{idx} =====")
        debug_print("Nome:", nome_texto)
        debug_print("Desconto:", desconto.get_text(strip=True) if desconto else "")
        debug_print("Preço Clube:", preco_clube.get_text(strip=True) if preco_clube else "")
        debug_print("Preço Antigo:", preco_antigo.get_text(strip=True) if preco_antigo else "")
        debug_print("Preço Novo:", preco_novo.get_text(strip=True) if preco_novo else "")
        debug_print("==============================")

        categoria = detectar_categoria(nome_texto)

        produtos.append({
            "nome": nome_texto,
            "desconto": desconto.get_text(strip=True) if desconto else "",
            "desconto_valor": desconto_valor,
            "preco_clube": preco_clube.get_text(strip=True).replace(" no + Amigo", "") if preco_clube else "",
            "preco_antigo": preco_antigo.get_text(strip=True) if preco_antigo else "",
            "preco_novo": preco_novo.get_text(strip=True) if preco_novo else "Sem preço",
            "categoria": categoria
        })

    if DEBUG:
        debug_log.close()

    return produtos


# ============================================================
# TESTE DIRETO
# ============================================================

if __name__ == "__main__":
    lista = extrair_produtos()
    print("\n===== PRIMEIROS 10 PRODUTOS =====")
    for p in lista[:10]:
        print(p["nome"], "=>", p["categoria"])