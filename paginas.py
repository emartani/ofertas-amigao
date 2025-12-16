import webbrowser
from datetime import datetime

def gerar_tabela(produtos, arquivo="index.html"):
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Ordenação inicial: maior desconto
    produtos_ordenados = sorted(produtos, key=lambda x: -x["desconto_valor"])

    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
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
            body {{
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 20px;
                color: #333;
            }}

            h1 {{
                text-align: center;
                color: #006400;
                margin-bottom: 10px;
            }}

            #atualizacao {{
                text-align: center;
                font-size: 14px;
                color: #555;
                margin-bottom: 20px;
            }}

            #busca {{
                display: block;
                margin: 20px auto;
                padding: 12px;
                width: 60%;
                font-size: 16px;
                border: 1px solid #bbb;
                border-radius: 6px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}

            .botoes {{
                text-align: center;
                margin: 20px;
            }}

            button {{
                padding: 10px 20px;
                margin: 5px;
                font-size: 15px;
                cursor: pointer;
                border: none;
                border-radius: 6px;
                background: #007b3a;
                color: #fff;
                transition: 0.2s;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }}

            button:hover {{
                background: #005f2c;
                transform: scale(1.03);
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                background: white;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 6px rgba(0,0,0,0.15);
            }}

            th {{
                background-color: #006400;
                color: #fff;
                padding: 12px;
                text-align: left;
                position: sticky;
                top: 0;
                z-index: 1;
            }}

            td {{
                padding: 10px 12px;
                border-bottom: 1px solid #eee;
            }}

            tr:hover {{
                background-color: #f1f1f1;
            }}

            .desconto {{
                font-weight: bold;
                color: #d32f2f;
            }}

            .preco-usado {{
                font-style: italic;
                color: #555;
            }}
        </style>
    </head>

    <body>
        <h1 id="titulo">Ofertas Amigão Lins - Ordenados por Maior Desconto</h1>
        <p id="atualizacao">Atualizado em: {data_atual}</p>

        <div class="botoes">
            <button onclick="ordenarDesconto()">Ordenados por Maior Desconto</button>
            <button onclick="ordenarPreco()">Ordenados por Menor Valor</button>
        </div>

        <input type="text" id="busca" placeholder="Buscar produto...">

        <table id="tabela">
            <tr>
                <th>Nome</th>
                <th>Preço Clube + Amigo</th>
                <th>Preço Antigo</th>
                <th>Preço Novo</th>
                <th>Desconto</th>
                <th>Menor Valor</th>
            </tr>
    """

    # Preenche tabela inicial (ordenada por desconto)
    for p in produtos_ordenados:
        html += f"""
            <tr>
                <td>{p['nome']}</td>
                <td>{p['preco_clube']}</td>
                <td>{p['preco_antigo']}</td>
                <td>{p['preco_novo']}</td>
                <td class="desconto">{p['desconto']}</td>
                <td class="preco-usado">-</td>
            </tr>
        """

    html += """
        </table>

        <script>
        function normalizeText(s) {
            return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim();
        }

        document.addEventListener('DOMContentLoaded', function() {
            const input = document.getElementById('busca');
            input.value = '';
            const linhas = document.querySelectorAll('#tabela tr');
            linhas.forEach(tr => tr.style.display = '');
            input.addEventListener('input', function() {
                const filtro = normalizeText(input.value);
                linhas.forEach(function(tr) {
                    if (!tr.querySelector('td')) return;
                    const nome = normalizeText(tr.cells[0].textContent);
                    tr.style.display = (filtro === '' || nome.includes(filtro)) ? '' : 'none';
                });
            });
        });

        function ordenarDesconto() {
            ordenarTabela(4, true);
            document.getElementById("titulo").textContent = "Ofertas Amigão Lins - Ordenados por Maior Desconto";
            atualizarPrecoUsado("-");
        }

        function ordenarPreco() {
            ordenarTabelaPreco();
            document.getElementById("titulo").textContent = "Ofertas Amigão Lins - Ordenados por Menor Valor";
        }

        function ordenarTabela(colIndex, desc) {
            const tabela = document.getElementById("tabela");
            let linhas = Array.from(tabela.rows).slice(1);
            linhas.sort((a, b) => {
                let va = parseInt(a.cells[colIndex].textContent.replace('%','')) || 0;
                let vb = parseInt(b.cells[colIndex].textContent.replace('%','')) || 0;
                return desc ? vb - va : va - vb;
            });
            linhas.forEach(l => tabela.appendChild(l));
        }

        function ordenarTabelaPreco() {
            const tabela = document.getElementById("tabela");
            let linhas = Array.from(tabela.rows).slice(1);
            linhas.sort((a, b) => {
                let va = extrairPreco(a);
                let vb = extrairPreco(b);
                return va.valor - vb.valor;
            });
            linhas.forEach(l => tabela.appendChild(l));
            linhas.forEach(l => {
                let info = extrairPreco(l);
                l.cells[5].textContent = info.tipo + " (" + info.valor.toFixed(2) + ")";
            });
        }

        function extrairPreco(tr) {
            let precoClube = tr.cells[1].textContent.replace("R$", "").replace(",", ".").split(" ")[0];
            let precoNovo = tr.cells[3].textContent.replace("R$", "").replace(",", ".").split(" ")[0];
            let pc = parseFloat(precoClube);
            let pn = parseFloat(precoNovo);
            if (!isNaN(pc) && pc > 0) return {valor: pc, tipo: "Clube + Amigo"};
            if (!isNaN(pn) && pn > 0) return {valor: pn, tipo: "Novo"};
            return {valor: Infinity, tipo: "-"};
        }

        function atualizarPrecoUsado(valor) {
            const linhas = document.querySelectorAll('#tabela tr');
            linhas.forEach(function(tr) {
                if (!tr.querySelector('td')) return;
                tr.cells[5].textContent = valor;
            });
        }
        </script>
    </body>
    </html>
    """

    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(html)

    webbrowser.open(arquivo)
