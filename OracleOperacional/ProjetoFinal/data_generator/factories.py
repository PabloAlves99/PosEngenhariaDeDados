from datetime import datetime, timedelta
import random
import uuid

from .config import fake, PAYMENT_METHODS, PAYMENT_STATUS, CITIES, PRODUCTS


def random_date(start_year=2024, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))


def generate_customer():
    return {
        "customer_id": f"CUST-{fake.random_int(100, 999)}",
        "name": fake.name(),
        "email": fake.email(),
        "document": fake.cpf().replace(".", "").replace("-", "")
    }


def generate_items():
    n = random.randint(1, 4)
    items = []

    for _ in range(n):
        p = random.choice(PRODUCTS)
        items.append({
            "product_id": p["product_id"],
            "product_name": p["product_name"],
            "category": p["category"],
            "unit_price": p["unit_price"],
            "quantity": random.randint(1, 3),
            "discount": round(random.uniform(0, 250), 2)
        })

    return items


def generate_order():
    city, state = random.choice(CITIES)

    return {
        "_id": str(uuid.uuid4()),
        "order_id": f"ORD-{datetime.now().year}-{random.randint(100000, 999999)}",
        "order_date": random_date().isoformat() + "Z",
        "customer": generate_customer(),
        "items": generate_items(),
        "payment": {
            "method": random.choice(PAYMENT_METHODS),
            "installments": random.choice([1, 2, 3, 6, 10, 12]),
            "status": random.choice(PAYMENT_STATUS)
        },
        "shipping": {
            "city": city,
            "state": state,
            "country": "BR",
            "shipping_value": round(random.uniform(10, 80), 2)
        }
    }
