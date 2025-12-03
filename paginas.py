import webbrowser

def gerar_tabela(produtos, arquivo="produtos_amigao_tabela.html"):
    # Ordenação inicial: maior desconto
    produtos_ordenados = sorted(produtos, key=lambda x: -x["desconto_valor"])

    html = """
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Produtos Extraídos</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #fafafa; margin: 20px; color: #333; }
            h1 { text-align: center; color: #006400; }
            #busca { display:block; margin:20px auto; padding:10px; width:50%; font-size:16px; border:1px solid #ccc; border-radius:4px; }
            .botoes { text-align:center; margin:20px; }
            button { padding:10px 20px; margin:5px; font-size:14px; cursor:pointer; border:none; border-radius:4px; background:#006400; color:#fff; }
            button:hover { background:#004d00; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }
            th { background-color: #006400; color: #fff; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            .desconto { font-weight: bold; color: #d32f2f; }
            .preco-usado { font-style: italic; color: #555; }
        </style>
    </head>
    <body>
    <h1 id="titulo">Produtos Extraídos - Ordenados por Maior Desconto</h1>
    <div class="botoes">
        <button onclick="ordenarDesconto()">Ordenados por Maior Desconto</button>
        <button onclick="ordenarPreco()">Ordenados por Menor Valor</button>
    </div>
    <input type="text" id="busca" placeholder="Buscar produto...">
    <table id="tabela">
        <tr>
            <th>Nome</th>
            <th>Peso</th>
            <th>Preço Clube + Amigo</th>
            <th>Preço Antigo</th>
            <th>Preço Novo</th>
            <th>Desconto</th>
            <th>Preço usado</th>
        </tr>
    """

    # Preenche tabela inicial (ordenada por desconto)
    for p in produtos_ordenados:
        html += f"""
        <tr>
            <td>{p['nome']}</td>
            <td>{p['peso']}</td>
            <td>{p['preco_clube'].replace(" no + Amigo", "")}</td>
            <td>{p['preco_antigo']}</td>
            <td>{p['preco_novo']}</td>
            <td class="desconto">{p['desconto']}</td>
            <td class="preco-usado">-</td>
        </tr>
        """

    html += """
    </table>
    <script>
    // Normaliza texto para busca
    function normalizeText(s) {
        return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim();
    }

    // Campo de busca
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

    // Ordenação por desconto
    function ordenarDesconto() {
        ordenarTabela(5, true);
        document.getElementById("titulo").textContent = "Produtos Extraídos - Ordenados por Maior Desconto";
        atualizarPrecoUsado("-");
    }

    // Ordenação por menor valor (clube ou novo)
    function ordenarPreco() {
        ordenarTabelaPreco();
        document.getElementById("titulo").textContent = "Produtos Extraídos - Ordenados por Menor Valor";
    }

    // Ordenar por coluna numérica (desconto)
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

    // Ordenar por menor preço (clube ou novo)
    function ordenarTabelaPreco() {
        const tabela = document.getElementById("tabela");
        let linhas = Array.from(tabela.rows).slice(1);
        linhas.sort((a, b) => {
            let va = extrairPreco(a);
            let vb = extrairPreco(b);
            return va.valor - vb.valor;
        });
        linhas.forEach(l => tabela.appendChild(l));
        // Atualiza coluna "Preço usado"
        linhas.forEach(l => {
            let info = extrairPreco(l);
            l.cells[6].textContent = info.tipo + " (" + info.valor.toFixed(2) + ")";
        });
    }

    function extrairPreco(tr) {
        let precoClube = tr.cells[2].textContent.replace("R$", "").replace(",", ".").split(" ")[0];
        let precoNovo = tr.cells[4].textContent.replace("R$", "").replace(",", ".").split(" ")[0];
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
            tr.cells[6].textContent = valor;
        });
    }
    </script>
    </body>
    </html>
    """

    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(html)

    webbrowser.open(arquivo)
