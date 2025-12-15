def detectar_categoria(nome_produto: str) -> str:
    nome = nome_produto.lower()

    # --- Regras de exceção ---
    if any(p in nome for p in ["cães", "ração", "dog chow", "friskies", "kitekat", "purina", "whiskas"]):
        return "outros"
    if any(p in nome for p in ["escova dental", "absorvente", "condicionador", "shampoo", "creme dental", "desodorante"]):
        return "outros"
    if any(p in nome for p in ["calda", "creme", "manteiga", "iogurte", "achocolatado", "wafer", "chocolate", "cappuccino", "lasanha", "caldo", "pizza", "papel alumínio", "copo", "esponja", "guardanapo", "talher", "prato descartável", "papel higiênico", "fralda", "lenço", "toalha", "higiene"]):
        return "outros"

    # --- Açougue ---
    if any(p in nome for p in ["carne", "frango", "bovino", "suíno", "peixe", "atum", "salmão", "cordeiro", "linguiça", "presunto", "hamburguer"]):
        return "açougue"

    # --- Limpeza ---
    if any(p in nome for p in ["detergente", "sabão", "desinfetante", "inseticida", "limpador", "amaciante", "alvejante", "lysoform", "omo", "vanish", "veja", "pinho sol", "raid", "girando sol"]):
        return "limpeza"

    # --- Mercearia ---
    if any(p in nome for p in ["salgadinho", "sardinha", "extrato", "canjiquinha", "pringles", "chips", "gelatina", "farofa", "doce", "leite condensado", "chocolate ao leite", "rosquinha", "atum", "arroz", "feijão", "macarrão", "massa", "farinha", "biscoito", "torrada", "pão", "chocolate", "nutella", "azeitona", "maionese", "cereal", "panettone", "margarina", "queijo", "bolacha", "mistura", "aveia", "café", "polenguinho", "batata palha", "molho", "condimento", "tempero", "granulado"]):
        return "mercearia"
        
    # --- Bebidas ---
    if any(p in nome for p in ["isotônico", "Refresco ", "cerveja", "vinho", "espumante", "suco", "bebida", "leite", "refrigerante", "chá", "água", "energético", "batavo", "italac", "ades"]):
        return "bebidas"

    # --- Hortifuti ---
    if any(p in nome for p in ["pessego", "abóbora", "alface", "limão", "milho", "cenoura", "laranja", "ervilha", "batata", "manga", "uva", "cereja", "banana", "maçã", "tomate", "pêssego", "pepino", "couve", "brócolis"]):
        return "hortifuti"



    return "outros"
