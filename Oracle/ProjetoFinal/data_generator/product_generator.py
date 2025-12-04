import random

CATEGORIES = {
    "Eletrônicos": (300, 6000),
    "Acessórios": (30, 600),
    "Casa e Escritório": (40, 2000),
    "Informática": (40, 1200),
    "Esportes": (40, 1200),
    "Games": (80, 1500),
}

ADJECTIVES = [
    "Pro", "Plus", "Max", "Ultra", "Prime", "X", "S", "Advance", "Elite", "Turbo"
]

NOUNS = [
    "Notebook", "Smartphone", "Monitor", "Headset", "Mouse", "Teclado",
    "SSD", "HD", "Webcam", "Roteador", "Caixa de Som", "Smartwatch",
    "Volante", "Controle", "Câmera", "Hub USB", "Fone", "Cadeira",
    "Luminária", "Organizador", "Balança", "Óculos", "Cooler", "Placa Wi-Fi"
]


def generate_product_name():
    """
    Combina nome + adjetivo de forma variada.
    """
    base = random.choice(NOUNS)
    adj = random.choice(ADJECTIVES)
    return f"{base} {adj}"


def generate_price(category):
    """
    Gera valores coerentes dentro das faixas por categoria.
    """
    low, high = CATEGORIES[category]
    return round(random.uniform(low, high), 2)


def generate_products(n=1):
    """
    Gera n produtos completos no formato exigido pelo seu Mongo.
    """
    products = []

    for i in range(1, n+1):
        category = random.choice(list(CATEGORIES.keys()))
        product_name = generate_product_name()
        product_id = f"PROD-{i:03d}"

        products.append({
            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "unit_price": generate_price(category)
        })

    return products
