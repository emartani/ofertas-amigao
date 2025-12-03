def classificar_categoria(nome):
    nome = nome.lower()
    if any(p in nome for p in ["carne", "frango", "peixe", "bife", "linguiça", "costela", "porco", "hamburguer"]):
        return "Açougue"
    elif any(p in nome for p in ["detergente", "sabão", "desinfetante", "limpeza", "amaciante", "candida", "multiuso"]):
        return "Limpeza"
    elif any(p in nome for p in ["arroz", "feijão", "macarrão", "açúcar", "café", "óleo", "farinha", "molho", "sal"]):
        return "Mercearia"
    elif any(p in nome for p in ["banana", "maçã", "limão", "laranja", "uva", "batata", "tomate", "cenoura", "alface"]):
        return "Hortifruti"
    elif any(p in nome for p in ["cerveja", "vinho", "refrigerante", "suco", "água", "whisky", "vodka"]):
        return "Bebidas"
    elif any(p in nome for p in ["pão", "bolo", "biscoito", "croissant", "torta"]):
        return "Padaria"
    elif any(p in nome for p in ["leite", "queijo", "manteiga", "iogurte", "requeijão", "creme de leite"]):
        return "Laticínios"
    elif any(p in nome for p in ["pizza", "lasanha", "sorvete", "nuggets", "hamburguer congelado"]):
        return "Congelados"
    elif any(p in nome for p in ["shampoo", "condicionador", "sabonete", "creme dental", "desodorante", "higiene"]):
        return "Higiene Pessoal"
    else:
        return "Outros"
