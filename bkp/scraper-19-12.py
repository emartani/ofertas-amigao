from dotenv import load_dotenv
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

def extrair_produtos():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    # options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)

    # ============================================================
    # LOGIN
    # ============================================================

    debug_print("[DEBUG] Abrindo página inicial para login...")
    driver.get("https://www.amigao.com/")
    time.sleep(2)

    debug_screenshot(driver, "login_inicio")

    #with open("pagina_login.html", "w", encoding="utf-8") as f:
    #    f.write(driver.page_source)
    #debug_print("[DEBUG] HTML da página de login salvo em pagina_login.html")

    # Fechar pop-up de cookies se aparecer
    try:
        botao_consentimento = driver.find_element(By.CSS_SELECTOR, "button.modal-cookies-agree")
        botao_consentimento.click()
        time.sleep(1)
        debug_print("[DEBUG] Pop-up de cookies fechado")
    except:
        debug_print("[DEBUG] Nenhum pop-up de cookies encontrado")
    
    print(driver.page_source)

    time.sleep(10)
  
 

    
# ============================================================
# LOGIN
# ============================================================

    debug_print("[DEBUG] Abrindo página de login...")
    driver.get("https://secure.amigao.com/login")
    time.sleep(2)

    debug_screenshot(driver, "pagina_login")
    #time.sleep(10)
    # ✅ Campo de e-mail (loop até aparecer)
    campo_email = None
    for _ in range(30):  # tenta por até ~30 segundos
        try:
            campo_email = driver.find_element(By.CSS_SELECTOR, ".vtex-login-2-x-inputContainerEmail input")
            if campo_email.is_displayed():
                break
        except:
            pass
        time.sleep(1)

    if not campo_email:
        debug_print("[ERRO] Campo de email não encontrado após 30s")
        driver.quit()
        return []

    campo_email.clear()
    campo_email.send_keys(os.environ.get("AMIGAO_EMAIL"))
    debug_print("[DEBUG] Email digitado")

    # ✅ Campo de senha (loop até aparecer)
    campo_senha = None
    for _ in range(30):
        try:
            campo_senha = driver.find_element(By.CSS_SELECTOR, ".vtex-login-2-x-inputContainerPassword input")
            if campo_senha.is_displayed():
                break
        except:
            pass
        time.sleep(1)

    if not campo_senha:
        debug_print("[ERRO] Campo de senha não encontrado após 30s")
        driver.quit()
        return []

    campo_senha.clear()
    campo_senha.send_keys(os.environ.get("AMIGAO_SENHA"))
    debug_print("[DEBUG] Senha digitada")

    # ✅ Botão Entrar
    try:
        botao_entrar = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Entrar']]"))
        )
        botao_entrar.click()
        debug_print("[DEBUG] Clique no botão Entrar")
        time.sleep(3)
    except Exception as e:
        debug_print("[ERRO] Botão Entrar não encontrado:", e)
        driver.quit()
        return []

    # Esperar redirecionamento
    time.sleep(3)

    # ============================================================
    # ACESSAR PÁGINA DE PRODUTOS
    # ============================================================

    url = "https://www.amigao.com/s/?clubProducts"
    debug_print("[DEBUG] Acessando URL:", url)
    driver.get(url)
    time.sleep(3)

    debug_screenshot(driver, "pagina_inicial")

    # ✅ Clicar em "Mostrar Mais" até acabar
    while True:
        try:
            botao = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-testid='show-more']"))
            )
            botao.click()
            debug_print("[DEBUG] Clique em 'Mostrar Mais'")
            time.sleep(2)
        except:
            debug_print("[DEBUG] Não há mais 'Mostrar Mais'")
            break


    # Fechar pop-up de cookies se aparecer novamente
    try:
        botao_consentimento = driver.find_element(By.CSS_SELECTOR, "button.modal-cookies-agree")
        botao_consentimento.click()
        time.sleep(2)
        debug_print("[DEBUG] Pop-up de cookies fechado")
    except:
        pass

    debug_screenshot(driver, "pagina_final")

    # Extrair HTML final
    html = driver.page_source
    driver.quit()

    # ============================================================
    # EXTRAÇÃO DOS PRODUTOS
    # ============================================================

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select(".product-card")
    debug_print(f"[DEBUG] Total de produtos encontrados: {len(cards)}")

    produtos = []

    for idx, card in enumerate(cards):
        debug_html_bs4(card, idx)

        nome = card.select_one(".product-name")
        preco = card.select_one(".best-price")

        if not nome or not preco:
            continue

        nome = nome.get_text(strip=True)
        preco = preco.get_text(strip=True)

        categoria = detectar_categoria(nome)

        produtos.append({
            "nome": nome,
            "preco": preco,
            "categoria": categoria
        })

    return produtos
