import webbrowser
from datetime import datetime

def gerar_tabela(produtos, arquivo="index.html"):
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Ordenação inicial: maior desconto
    produtos_ordenados = sorted(produtos, key=lambda x: -x["desconto_valor"])

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

    <style>
        :root {{
            --bg-page: #fff7eb;
            --bg-header: #ffebc2;
            --accent: #e53935;  /* vermelho ofertas */
            --accent-dark: #b71c1c;
            --accent-secondary: #ff9800; /* laranja destaque */
            --text-main: #333;
            --text-muted: #666;
            --table-header-bg: #e53935;
            --table-header-text: #fff;
            --card-shadow: 0 3px 8px rgba(0,0,0,0.18);
            --border-radius: 10px;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            background-color: var(--bg-page);
            margin: 0;
            padding: 16px;
            color: var(--text-main);
        }}

        header {{
            max-width: 1100px;
            margin: 0 auto 16px auto;
            background: linear-gradient(135deg, #ffe0b2, #fff3e0);
            border-radius: var(--border-radius);
            padding: 16px 16px 12px 16px;
            box-shadow: var(--card-shadow);
        }}

        header h1 {{
            margin: 0;
            text-align: center;
            color: var(--accent-dark);
            font-size: 1.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        header p {{
            margin: 8px 0 0 0;
            text-align: center;
            font-size: 0.9rem;
            color: var(--text-muted);
        }}

        main {{
            max-width: 1100px;
            margin: 0 auto;
        }}

        .top-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }}

        .botoes {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        button {{
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
        }}

        button:hover {{
            background: var(--accent-dark);
            transform: translateY(-1px);
        }}

        button span.icon {{
            font-size: 1rem;
        }}

        #busca {{
            flex: 1;
            min-width: 180px;
            padding: 10px 12px;
            font-size: 0.95rem;
            border: 1px solid #d0b090;
            border-radius: 999px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            outline: none;
        }}

        #busca:focus {{
            border-color: var(--accent-secondary);
            box-shadow: 0 0 0 2px rgba(255,152,0,0.18);
        }}

        .table-container {{
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            background: #fff;
            border-radius: var(--border-radius);
            box-shadow: var(--card-shadow);
            padding: 0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            min-width: 720px;
        }}

        thead th {{
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
        }}

        tbody td {{
            padding: 9px 10px;
            border-bottom: 1px solid #f0e0d0;
            font-size: 0.93rem;
        }}

        tbody tr:nth-child(even) {{
            background-color: #fffaf4;
        }}

        tbody tr:hover {{
            background-color: #ffe8d2;
        }}

        .col-nome {{
            font-weight: 600;
        }}

        .desconto {{
            font-weight: 700;
            color: var(--accent);
        }}

        .preco-usado {{
            font-style: italic;
            color: var(--text-muted);
        }}

        .tag-desconto-alto {{
            display: inline-block;
            margin-left: 6px;
            padding: 2px 6px;
            font-size: 0.7rem;
            background: var(--accent-secondary);
            color: #fff;
            border-radius: 999px;
            text-transform: uppercase;
        }}

        .badge-ordem {{
            display: inline-block;
            margin-left: 6px;
            padding: 2px 8px;
            font-size: 0.7rem;
            border-radius: 999px;
            border: 1px solid rgba(0,0,0,0.15);
            background: #fff;
            color: #555;
        }}

        .info-bar {{
            margin-bottom: 6px;
            font-size: 0.82rem;
            color: var(--text-muted);
        }}

        @media (max-width: 600px) {{
            body {{
                padding: 10px;
            }}

            header {{
                padding: 12px 10px 8px 10px;
            }}

            header h1 {{
                font-size: 1.3rem;
            }}

            header p {{
                font-size: 0.8rem;
            }}

            .top-bar {{
                flex-direction: column;
                align-items: stretch;
            }}

            #busca {{
                width: 100%;
            }}

            .botoes {{
                width: 100%;
                flex-direction: column;
            }}

            button {{
                width: 100%;
                justify-content: center;
            }}

            table {{
                min-width: 600px;
            }}
        }}
    </style>
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

    for p in produtos_ordenados:
        html += f"""
                    <tr>
                        <td class="col-nome">{p['nome']}</td>
                        <td>{p['preco_clube']}</td>
                        <td>{p['preco_antigo']}</td>
                        <td>{p['preco_novo']}</td>
                        <td class="desconto">{p['desconto']}</td>
                        <td class="preco-usado">-</td>
                    </tr>
"""

    html += """
                </tbody>
            </table>
        </div>
    </main>

    <script>
    function normalizeText(s) {
        return s.toLowerCase()
                .normalize('NFD')
                .replace(/[\\u0300-\\u036f]/g, '')
                .trim();
    }

    function extrairPreco(tr) {
        let precoClube = tr.cells[1].textContent.replace("R$", "").replace(",", ".").split(" ")[0];
        let precoNovo = tr.cells[3].textContent.replace("R$", "").replace(",", ".").split(" ")[0];

        let pc = parseFloat(precoClube);
        let pn = parseFloat(precoNovo);

        if (!isNaN(pc) && pc > 0) return { valor: pc, tipo: "Clube + Amigo" };
        if (!isNaN(pn) && pn > 0) return { valor: pn, tipo: "Novo" };
        return { valor: Infinity, tipo: "-" };
    }

    function preencherMenorValor() {
        const linhas = document.querySelectorAll('#tabela tbody tr');
        linhas.forEach(function(tr) {
            const celulas = tr.querySelectorAll('td');
            if (!celulas.length) return;
            let info = extrairPreco(tr);
            if (info.valor === Infinity) {
                celulas[5].textContent = "-";
            } else {
                celulas[5].textContent = info.tipo + " (" + info.valor.toFixed(2) + ")";
            }
        });
    }

    function ordenarTabela(colIndex, desc) {
        const tabela = document.getElementById("tabela");
        let linhas = Array.from(tabela.tBodies[0].rows);

        linhas.sort((a, b) => {
            let va = parseInt(a.cells[colIndex].textContent.replace('%','')) || 0;
            let vb = parseInt(b.cells[colIndex].textContent.replace('%','')) || 0;
            return desc ? vb - va : va - vb;
        });

        linhas.forEach(l => tabela.tBodies[0].appendChild(l));
    }

    function ordenarTabelaPreco() {
        const tabela = document.getElementById("tabela");
        let linhas = Array.from(tabela.tBodies[0].rows);

        linhas.sort((a, b) => {
            let va = extrairPreco(a);
            let vb = extrairPreco(b);
            return va.valor - vb.valor;
        });

        linhas.forEach(l => tabela.tBodies[0].appendChild(l));
        preencherMenorValor();
    }

    function ordenarDesconto() {
        ordenarTabela(4, true);
        document.getElementById("info-ordem").innerHTML = 'Listando por: <strong>Maior desconto</strong>';
        preencherMenorValor();
    }

    function ordenarPreco() {
        ordenarTabelaPreco();
        document.getElementById("info-ordem").innerHTML = 'Listando por: <strong>Menor valor</strong>';
    }

    document.addEventListener('DOMContentLoaded', function() {
        const input = document.getElementById('busca');
        const linhas = document.querySelectorAll('#tabela tbody tr');

        input.value = '';
        linhas.forEach(tr => tr.style.display = '');

        input.addEventListener('input', function() {
            const filtro = normalizeText(input.value);
            linhas.forEach(function(tr) {
                const celulas = tr.querySelectorAll('td');
                if (!celulas.length) return;
                const nome = normalizeText(celulas[0].textContent);
                tr.style.display = (filtro === '' || nome.includes(filtro)) ? '' : 'none';
            });
        });

        // Ao carregar a página, já preencher "Menor valor"
        preencherMenorValor();
    });
    </script>
</body>
</html>
"""

    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(html)

    webbrowser.open(arquivo)
