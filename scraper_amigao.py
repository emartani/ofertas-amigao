import os
import json
import requests
from typing import List, Dict, Any

AMIGAO_URL = "https://www.amigao.com/api/graphql"

def build_headers() -> Dict[str, str]:
    """
    Headers para chamar a API do Amigão.
    O cookie vem de uma variável de ambiente (GitHub Secret).
    """
    cookie = os.environ.get("COOKIE_AMIGAO")
    if not cookie:
        raise RuntimeError("Variável de ambiente COOKIE_AMIGAO não definida.")

    return {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) PythonScraper/1.0",
        "Accept": "application/json, text/plain, */*",
        "Cookie": cookie,
        "Referer": "https://www.amigao.com/s/?clubProducts",
    }


def build_variables(first: int, after: str | None) -> Dict[str, Any]:
    """
    Monta o objeto 'variables' da query GraphQL.
    Ajuste 'regionId' se trocar de região.
    """
    selected_facets = [
        {"key": "preco2", "value": "true"},
        {
            "key": "channel",
            "value": json.dumps({
                "salesChannel": "2",
                "regionId": "v2.4EEA2E146173A58695898C94FB44150A",
            }),
        },
        {"key": "locale", "value": "pt-br"},
    ]

    variables: Dict[str, Any] = {
        "first": first,
        "sort": "score_desc",
        "term": "",
        "selectedFacets": selected_facets,
    }

    if after is not None:
        variables["after"] = after

    return variables


def fetch_page(first: int, after: str | None) -> Dict[str, Any]:
    """
    Faz uma chamada para uma página de produtos.
    """
    headers = build_headers()
    variables = build_variables(first, after)

    params = {
        "operationName": "ProductsQuery",
        "variables": json.dumps(variables, separators=(",", ":")),
    }

    resp = requests.get(AMIGAO_URL, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def parse_products(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extrai os dados relevantes de cada produto do JSON.
    """
    products_data = data["data"]["search"]["products"]
    edges = products_data["edges"]

    produtos: List[Dict[str, Any]] = []

    for edge in edges:
        node = edge["node"]

        name = node.get("name")
        sku = node.get("sku")
        slug = node.get("slug")
        brand = (node.get("brand") or {}).get("name")
        gtin = node.get("gtin")

        price_without_promotions = node.get("priceWithoutPromotions")
        has_club_price = node.get("hasClubPrice")

        custom_offers = node.get("customOffers") or {}
        list_price_custom = custom_offers.get("listPriceCustom")
        spot_price_custom = custom_offers.get("spotPriceCustom")
        has_discount = custom_offers.get("hasDiscount")

        offers_block = node.get("offers") or {}
        low_price = offers_block.get("lowPrice")

        image_url = None
        if node.get("image"):
            image_url = node["image"][0].get("url")

        category_tree = node.get("categoryTree") or []

        produtos.append({
            "name": name,
            "sku": sku,
            "slug": slug,
            "brand": brand,
            "gtin": gtin,
            "price_without_promotions": price_without_promotions,
            "has_club_price": has_club_price,
            "list_price_custom": list_price_custom,
            "spot_price_custom": spot_price_custom,
            "has_discount": has_discount,
            "low_price": low_price,
            "image_url": image_url,
            "category_tree": category_tree,
        })

    return produtos


def get_all_products(page_size: int = 50) -> List[Dict[str, Any]]:
    """
    Pagina sobre todos os produtos com preco2=true.
    """
    all_products: List[Dict[str, Any]] = []
    after: str | None = None

    while True:
        data = fetch_page(first=page_size, after=after)

        products_data = data["data"]["search"]["products"]
        page_info = products_data["pageInfo"]
        edges = products_data["edges"]

        if not edges:
            break

        produtos = parse_products(data)
        all_products.extend(produtos)

        # A API que você mandou tem pageInfo.totalCount,
        # mas não vimos ainda cursor real.
        # Muitas implementações usam 'page' como string do offset,
        # aqui estamos usando 'after' como "próximo offset".
        # Você pode adaptar se tiver um cursor explícito.
        total_count = page_info.get("totalCount")
        print(f"Coletados {len(all_products)} / {total_count} produtos (até agora)")

        # Estratégia simples: se o número coletado >= totalCount, para.
        if total_count and len(all_products) >= total_count:
            break

        # Próxima página:
        # se a API tiver cursor real, use pageInfo["endCursor"] / "hasNextPage".
        # Como não vimos no JSON, vamos simular por offset:
        after = str(len(all_products))

    return all_products

if __name__ == "__main__":
    produtos = get_all_products(page_size=50)
    print(f"\nTotal final de produtos: {len(produtos)}\n")

    # Exemplo: mostrar os 10 primeiros
    for p in produtos[:10]:
        print(
            p["name"],
            "| Clube:", p["spot_price_custom"],
            "| Lista:", p["list_price_custom"],
            "| Baixo:", p["low_price"],
        )
