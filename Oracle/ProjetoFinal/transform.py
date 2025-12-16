import re
import unicodedata
from datetime import datetime
from zoneinfo import ZoneInfo
from copy import deepcopy


def convert_utc_to_sao_paulo(date_str: str) -> str:
    dt_utc = datetime.fromisoformat(
        date_str.replace("Z", "+00:00")
    )
    return dt_utc.astimezone(
        ZoneInfo("America/Sao_Paulo")
    ).isoformat()


def normalize_string(value: str) -> str:
    if not isinstance(value, str):
        return value

    value = unicodedata.normalize("NFKD", value)
    value = "".join(
        c for c in value if not unicodedata.combining(c)
    )
    value = re.sub(r"\s+", " ", value).strip()

    return value.upper()


def calculate_item_metrics(item: dict) -> dict:
    unit_price = float(item["unit_price"])
    quantity = float(item["quantity"])
    discount = float(item["discount"])

    gross_amount = unit_price * quantity
    net_amount = gross_amount - discount

    discount_percent = (
        (discount / gross_amount) * 100
        if gross_amount > 0
        else 0
    )

    return {
        **item,
        "gross_amount": round(gross_amount, 2),
        "net_amount": round(net_amount, 2),
        "discount_percent": round(discount_percent, 2),
    }


def transform_order(order: dict) -> dict:
    source = deepcopy(order)

    # Data
    order_date = convert_utc_to_sao_paulo(
        source["order_date"]
    )

    # Cliente
    customer = {
        "customer_id": source["customer"]["customer_id"],
        "name": normalize_string(source["customer"]["name"]),
        "email": normalize_string(source["customer"]["email"]),
        "document": source["customer"]["document"],
    }

    # Itens
    items = []
    for item in source["items"]:
        normalized_item = {
            "product_id": item["product_id"],
            "product_name": normalize_string(
                item["product_name"]
            ),
            "category": normalize_string(
                item["category"]
            ),
            "unit_price": item["unit_price"],
            "quantity": item["quantity"],
            "discount": item["discount"],
        }

        items.append(
            calculate_item_metrics(normalized_item)
        )

    # Pagamento
    payment = {
        "method": normalize_string(
            source["payment"]["method"]
        ),
        "installments": source["payment"]["installments"],
        "status": normalize_string(
            source["payment"]["status"]
        ),
    }

    # Entrega
    shipping = {
        "city": normalize_string(
            source["shipping"]["city"]
        ),
        "state": normalize_string(
            source["shipping"]["state"]
        ),
        "country": normalize_string(
            source["shipping"]["country"]
        ),
        "shipping_value": source["shipping"]["shipping_value"],
    }

    # Documento final transformado
    return {
        "_id": source["_id"],
        "order_id": source["order_id"],
        "order_date": order_date,
        "customer": customer,
        "items": items,
        "payment": payment,
        "shipping": shipping,

    }
