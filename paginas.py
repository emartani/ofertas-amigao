import webbrowser
from datetime import datetime
import textwrap

def gerar_tabela(produtos, arquivo="index.html"):
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Ordenação inicial: maior desconto
    # produtos_ordenados = sorted(produtos, key=lambda x: -x["desconto_valor"])
    produtos_ordenados = produtos # mantém a ordem original da API
    
    # ============================
    # CSS (agora sem f-string!)
    # ============================
    css = textwrap.dedent("""
    <style>

        /* ======== Variáveis ======== */
        :root {
            --bg-page: #fff7eb;
            --bg-header: #ffebc2;
            --accent: #e53935;
            --accent-dark: #b71c1c;
            --accent-secondary: #ff9800;
            --text-main: #333;
            --text-muted: #666;
            --table-header-bg: #e53935;
            --table-header-text: #fff;
            --card-shadow: 0 3px 8px rgba(0,0,0,0.18);
            --border-radius: 10px;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            background-color: var(--bg-page);
            margin: 0;
            padding: 16px;
            color: var(--text-main);
        }

        header {
            max-width: 1100px;
            margin: 0 auto 16px auto;
            background: linear-gradient(135deg, #ffe0b2, #fff3e0);
            border-radius: var(--border-radius);
            padding: 16px 16px 12px 16px;
            box-shadow: var(--card-shadow);
        }

        header h1 {
            margin: 0;
            text-align: center;
            color: var(--accent-dark);
            font-size: 1.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        header p {
            margin: 8px 0 0 0;
            text-align: center;
            font-size: 0.9rem;
            color: var(--text-muted);
        }

        main {
            max-width: 1100px;
            margin: 0 auto;
        }

        .top-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }

        .botoes {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        button {
            padding: 10px 16px;
            font-size: 0.95rem;
            cursor: pointer;
            border: none;
            border-radius: 999px;
            background: var(--accent);
            color: #fff;
            transition: 0.2s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            display: inline-flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
        }

        button:hover {
            background: var(--accent-dark);
            transform: translateY(-1px);
        }

        #busca {
            flex: 1;
            min-width: 180px;
            padding: 10px 12px;
            font-size: 0.95rem;
            border: 1px solid #d0b090;
            border-radius: 999px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            outline: none;
        }

        .table-container {
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            background: #fff;
            border-radius: var(--border-radius);
            box-shadow: var(--card-shadow);
            padding: 0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            min-width: 720px;
        }

        thead th {
            background: var(--table-header-bg);
            color: var(--table-header-text);
            padding: 10px 10px;
            text-align: left;
            position: sticky;
            top: 0;
            z-index: 1;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        tbody td {
            padding: 9px 10px;
            border-bottom: 1px solid #f0e0d0;
            font-size: 0.93rem;
        }

        tbody tr:nth-child(even) {
            background-color: #fffaf4;
        }

        tbody tr:hover {
            background-color: #ffe8d2;
        }

        .col-nome {
            font-weight: 600;
        }

        .desconto {
            font-weight: 700;
            color: var(--accent);
        }

        .preco-usado {
            font-style: italic;
            color: var(--text-muted);
        }

        /* ======== MOBILE ======== */
        @media (max-width: 600px) {
            body { padding: 10px; }
            header { padding: 12px 10px 8px 10px; }
            header h1 { font-size: 1.3rem; }
            header p { font-size: 0.8rem; }
            .top-bar { flex-direction: column; align-items: stretch; }
            #busca { width: 100%; }
            .botoes { width: 100%; flex-direction: column; }
            button { width: 100%; justify-content: center; }
            table { min-width: 600px; }
        }

        /* ======== PAISAGEM (LANDSCAPE) ======== */
        @media (orientation: landscape) {

            html, body {
                max-width: 100%;
                overflow-x: hidden;
            }

            * {
                max-width: 100%;
            }

            .table-container {
                overflow-x: hidden;
            }

            table {
                width: 100%;
                min-width: unset;
                table-layout: fixed;
            }

            th, td {
                white-space: normal;
                word-wrap: break-word;
                font-size: 0.85rem;
            }

            .col-nome {
                max-width: 200px;
            }
        }

    </style>
    """)

    # ============================
    # HTML PRINCIPAL
    # ============================
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ofertas Amigão Lins</title>

    <!-- Plausible Analytics -->
    <script defer data-domain="emartani.github.io" src="https://plausible.io/js/script.js"></script>

    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-0X4P4ZM0RC"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{ dataLayer.push(arguments); }}
        gtag('js', new Date());
        gtag('config', 'G-0X4P4ZM0RC');
    </script>

    {css}
</head>

<body>
    <header>
        <h1>Ofertas Amigão Lins</h1>
        <p>Atualizado em: {data_atual}</p>
    </header>

    <main>
        <div class="top-bar">
            <div class="botoes">
                <button onclick="ordenarDesconto()">
                    <span class="icon">🔥</span>
                    <span>Maior desconto</span>
                </button>
                <button onclick="ordenarPreco()">
                    <span class="icon">💰</span>
                    <span>Menor valor</span>
                </button>
            </div>
            <input type="text" id="busca" placeholder="Buscar produto...">
        </div>

        <div class="info-bar" id="info-ordem">
            Listando por: <strong>Maior desconto</strong>
        </div>

        <div class="table-container">
            <table id="tabela">
                <thead>
                    <tr>
                        <th>Produto</th>
                        <th>Preço Clube + Amigo</th>
                        <th>Preço antigo</th>
                        <th>Preço novo</th>
                        <th>Desconto</th>
                        <th>Menor valor</th>
                    </tr>
                </thead>
                <tbody>
"""

    # ============================
    # LINHAS DA TABELA
    # ============================
        # ============================
    # LINHAS DA TABELA
    # ============================
    for p in produtos_ordenados:
        # escolher o menor valor entre as 3 colunas de preço (texto)
        valores = [
            p["preco_clube"],
            p["preco_antigo"],
            p["preco_novo"],
        ]

        # filtrar valores vazios 
        valores_validos = [v for v in valores if v.strip() != ""]

# se todos estiverem vazios, coloca "-" 
        if not valores_validos: 
            p["menor_valor"] = "-" 
        else:

        # converte só para comparar, mantendo o texto original
            def para_float(v):
                try:
                    return float(
                        v.replace("R$", "")
                        .replace(".", "")
                        .replace(",", ".")
                        .strip()
                    )
                except:
                    return float('inf')  # para valores inválidos   
            
            p["menor_valor"] = min(valores, key=para_float)

        html += f"""
                    <tr>
                        <td class="col-nome">{p['nome']}</td>
                        <td>{p['preco_clube']}</td>
                        <td>{p['preco_antigo']}</td>
                        <td>{p['preco_novo']}</td>
                        <td class="desconto">{p['desconto']}</td>
                        <td class="preco-usado">{p['menor_valor']}</td>
                    </tr>
"""


    # ============================
    # FECHAMENTO DO HTML
    # ============================
    html += """
                </tbody>
            </table>
        </div>
    </main>

    <script>
    function obterValorNumerico(texto) {
        if (!texto) return 0;
        return parseFloat(
            texto.replace("R$", "")
                 .replace(/\./g, "")
                 .replace(",", ".")
                 .trim()
        ) || 0;
    }

    function ordenarTabela(comparador) {
        const tabela = document.getElementById("tabela");
        const tbody = tabela.querySelector("tbody");
        const linhas = Array.from(tbody.querySelectorAll("tr"));

        linhas.sort(comparador);

        linhas.forEach(linha => tbody.appendChild(linha));
    }

    function ordenarDesconto() {
        const info = document.getElementById("info-ordem");
        ordenarTabela((a, b) => {
            const ta = a.querySelector(".desconto")?.textContent || "0";
            const tb = b.querySelector(".desconto")?.textContent || "0";

            const va = parseFloat(ta.replace("%", "").trim()) || 0;
            const vb = parseFloat(tb.replace("%", "").trim()) || 0;

            // maior desconto primeiro
            return vb - va;
        });
        if (info) {
            info.innerHTML = 'Listando por: <strong>Maior desconto</strong>';
        }
    }

    function ordenarPreco() {
        const info = document.getElementById("info-ordem");
        ordenarTabela((a, b) => {
            // aqui você escolhe QUAL coluna usar:
            // 1) preço novo (quarta coluna)
            const ta = a.children[3].textContent;
            const tb = b.children[3].textContent;

            // se quiser usar "Menor valor", troque 3 por 5:
            // const ta = a.children[5].textContent;
            // const tb = b.children[5].textContent;

            const va = obterValorNumerico(ta);
            const vb = obterValorNumerico(tb);

            // menor valor primeiro
            return va - vb;
        });
        if (info) {
            info.innerHTML = 'Listando por: <strong>Menor valor</strong>';
        }
    }

    // DESATIVADO DURANTE TESTES opcional: ordenar por maior desconto ao carregar
    // document.addEventListener("DOMContentLoaded", ordenarDesconto);
    </script>

    <script> 
        // FILTRAR TABELA ENQUANTO DIGITA 
        document.getElementById("busca").addEventListener("input", function () { 
            const termo = this.value.toLowerCase(); 
            const linhas = document.querySelectorAll("#tabela tbody tr"); 
            
            linhas.forEach(linha => { 
                const textoLinha = linha.textContent.toLowerCase(); 
                linha.style.display = textoLinha.includes(termo) ? "" : "none"; 
            }); 
        }); 
    </script>
    
</body>
</html>
"""

    # Salvar arquivo
    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(html)

    return arquivo