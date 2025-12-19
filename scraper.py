from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from classificacao import detectar_categoria
import os

from dotenv import load_dotenv 
load_dotenv()
# ============================================================
# DEBUG
# ============================================================

DEBUG = False
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

load_dotenv()

# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import os

def extrair_produtos():
    # Inicializa o driver
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        # Abre página de login
        driver.get("https://secure.amigao.com/login")
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".vtex-login-2-x-inputContainerEmail input"))
        )

        # Campo de e-mail
        campo_email = driver.find_element(By.CSS_SELECTOR, ".vtex-login-2-x-inputContainerEmail input")
        campo_email.clear()
        campo_email.send_keys(os.environ.get("AMIGAO_EMAIL"))

        # Campo de senha
        campo_senha = driver.find_element(By.CSS_SELECTOR, ".vtex-login-2-x-inputContainerPassword input")
        campo_senha.clear()
        campo_senha.send_keys(os.environ.get("AMIGAO_SENHA"))

        # Botão Entrar
        botao_entrar = driver.find_element(By.XPATH, "//button[.//span[text()='Entrar']]")
        botao_entrar.click()

        time.sleep(5)  # espera login

        # ============================================================
        # ACESSAR PÁGINA DE PRODUTOS
        # ============================================================

        url = "https://www.amigao.com/s/?clubProducts"   # ou outra URL de categoria/busca
        debug_print("[DEBUG] Acessando URL:", url)
        driver.get(url)
        time.sleep(2)

        debug_screenshot(driver, "pagina_inicial")

        # Fechar pop-up de cookies se aparecer
        try:
            botao_consentimento = driver.find_element(By.CSS_SELECTOR, "button.modal-cookies-agree")
            botao_consentimento.click()
            time.sleep(1)
            debug_print("[DEBUG] Pop-up de cookies fechado")
        except:
            debug_print("[DEBUG] Nenhum pop-up de cookies encontrado")

        time.sleep(10)

        # Lista de seletores possíveis para botões de pop-up
        seletores_popups = [
            "button.modal-cookies-agree",          # cookies
            "button.bonus-popup-close",            # exemplo: fechar bônus
            "button[data-testid='close-promo']",   # exemplo: fechar promoções
        ]

        for seletor in seletores_popups:
            try:
                botao = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, seletor))
                )
                botao.click()
                debug_print(f"[DEBUG] Pop-up fechado: {seletor}")
                time.sleep(1)
            except:
                debug_print(f"[DEBUG] Nenhum pop-up encontrado para seletor: {seletor}")

        # ✅ Clicar em "Mostrar Mais" até acabar
        while True:
            try:
                botao = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-testid='show-more']"))
                )
                botao.click()
                debug_print("[DEBUG] Clique em 'Mostrar Mais'")
                time.sleep(2)  # dá tempo para carregar os novos produtos
            except:
                debug_print("[DEBUG] Não há mais 'Mostrar Mais'")
                break

        debug_screenshot(driver, "pagina_final")

        with open("produtos.txt", "w", encoding="utf-8") as f:
            for p in produtos:
                linha = f"{p['nome']} | Clube: {p['preco_clube']} | Antigo: {p['preco_antigo']} | Novo: {p['preco_novo']} | Desconto: {p['desconto']} | Categoria: {p['categoria']}\n"
                f.write(linha)

        print("[DEBUG] Arquivo 'produtos.txt' gerado com", len(produtos), "produtos")


        # Extrair HTML final (agora com todos os produtos carregados)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")


        # Extrai produtos
        cards = soup.select(".product-card")
        print(f"[DEBUG] Total de produtos encontrados: {len(cards)}")

        produtos = []
        for card in cards:
            nome = card.select_one(".product-card-name")
            preco_clube = card.select_one(".product-card-club-price")
            preco_antigo = card.select_one(".product-card-old-price span")
            preco_novo = card.select_one(".product-card-new-price")
            desconto = card.select_one(".product-card-discount-badge-value")

            # Se não tiver nome, pula
            if not nome:
                continue

            produtos.append({
                "nome": nome.get_text(strip=True),
                "preco_clube": preco_clube.get_text(strip=True) if preco_clube else "",
                "preco_antigo": preco_antigo.get_text(strip=True) if preco_antigo else "",
                "preco_novo": preco_novo.get_text(strip=True) if preco_novo else "",
                "desconto": desconto.get_text(strip=True) if desconto else "",
                "promocao": "Mais Amigo" if card.select_one(".product-club-badge") else ""
            })



        return produtos

    finally:
        driver.quit()
