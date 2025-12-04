from faker import Faker

fake = Faker("pt_BR")

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "salesdb"
COLLECTION_NAME = "orders"

PAYMENT_METHODS = ["CREDIT_CARD", "PIX", "BOLETO"]
PAYMENT_STATUS = ["APPROVED", "PENDING", "REJECTED"]

CITIES = [
    ("Belo Horizonte", "MG"),
    ("São Paulo", "SP"),
    ("Rio de Janeiro", "RJ"),
    ("Curitiba", "PR"),
    ("Salvador", "BA")
]

PRODUCTS = [
    {"product_id": "PROD-001", "product_name": "Notebook Gamer",
        "category": "Eletrônicos", "unit_price": 4500.00},
    {"product_id": "PROD-002", "product_name": "Mouse Gamer",
        "category": "Acessórios", "unit_price": 150.00},
    {"product_id": "PROD-003", "product_name": "Teclado Mecânico",
        "category": "Acessórios", "unit_price": 350.00},
    {"product_id": "PROD-004", "product_name": "Monitor 27''",
        "category": "Eletrônicos", "unit_price": 1800.00}
]
