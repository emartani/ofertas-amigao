def gerar_tabela_api(produtos):
    html = """
    <html>
    <head>
        <meta charset="utf-8">
        <title>Produtos API</title>
        <style>
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Produtos extraídos via API GraphQL</h1>
        <table>
            <tr>
                <th>Nome</th>
                <th>Preço Clube</th>
                <th>Preço Antigo</th>
                <th>Preço Novo</th>
                <th>Desconto</th>
            </tr>
    """

    for p in produtos:
        html += f"""
            <tr>
                <td>{p['nome']}</td>
                <td>{p['preco_clube']}</td>
                <td>{p['preco_antigo']}</td>
                <td>{p['preco_novo']}</td>
                <td>{p['desconto']}</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    with open("produtos_api.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("[DEBUG] Arquivo 'produtos_api.html' gerado com", len(produtos), "produtos")
    return "produtos_api.html"
