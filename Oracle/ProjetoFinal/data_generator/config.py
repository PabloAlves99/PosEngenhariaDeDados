from faker import Faker
from .product_generator import generate_products

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

PRODUCTS = generate_products(50)
