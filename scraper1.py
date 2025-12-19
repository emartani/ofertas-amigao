import requests

def extrair_produtos_api():
    url = "https://www.amigao.com/api/graphql"
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36"
    }


    query = """
    query ProductsQuery($first: Int, $after: String, $sort: String, $term: String, $selectedFacets: [SelectedFacetInput]) {
      products(first: $first, after: $after, sort: $sort, term: $term, selectedFacets: $selectedFacets) {
        totalCount
        edges {
          node {
            productName
            productId
            items {
              sellers {
                commertialOffer {
                  Price
                  ListPrice
                }
              }
            }
          }
        }
      }
    }
    """

    variables = {
        "first": 10,
        "after": "0",
        "sort": "score_desc",
        "term": "",
        "selectedFacets": [
            {"key": "channel", "value": "{\"salesChannel\":\"2\",\"regionId\":\"v2.4EEA2E146173A58695898C94FB44150A\"}"},
            {"key": "locale", "value": "pt-br"}
        ]
    }

    produtos = []
    cursor = 0

    while True:
        variables["after"] = str(cursor)
        resp = requests.post(url, headers=headers, json={"query": query, "variables": variables})
        print("[DEBUG] Status:", resp.status_code)
        print("[DEBUG] Conteúdo:", resp.text[:500])  # mostra os primeiros 500 caracteres
        data = resp.json()

        edges = data["data"]["products"]["edges"]
        if not edges:
            break

        for edge in edges:
            node = edge["node"]
            offer = node["items"][0]["sellers"][0]["commertialOffer"]
            produtos.append({
                "nome": node["productName"],
                "preco_antigo": offer["ListPrice"],
                "preco_novo": offer["Price"],
                "preco_clube": "",  # se não vier separado
                "desconto": "",     # pode calcular depois
            })

        cursor += variables["first"]

    return produtos
