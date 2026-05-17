import oracledb
from pymongo import MongoClient
from datetime import datetime, timezone
from data_generator.config import MONGO_URI, DB_NAME, COLLECTION_NAME
from transform import transform_order


# =========================
# CONFIG ORACLE
# =========================
ORACLE_CONFIG = {
    "user": "sys",
    "password": "oracle",
    "dsn": "localhost:1521/freepdb1",
    "mode": oracledb.SYSDBA
}


# =========================
# UTIL
# =========================
def get_next_sk(cursor, table, column):
    cursor.execute(f"SELECT NVL(MAX({column}), 0) + 1 FROM {table}")
    return cursor.fetchone()[0]


def parse_iso_datetime(value):
    """
    Converte string ISO (Mongo) para datetime Python.
    Aceita Z ou offset.
    """
    if isinstance(value, datetime):
        return value

    value = value.replace("Z", "+00:00")
    return datetime.fromisoformat(value).astimezone(timezone.utc).replace(tzinfo=None)


# =========================
# EXTRACT
# =========================
def extract_orders():
    client = MongoClient(MONGO_URI)
    collection = client[DB_NAME][COLLECTION_NAME]

    for doc in collection.find():
        yield transform_order(doc)


# =========================
# LOAD STAGING
# =========================
def load_staging(cursor, orders):
    batch_id = int(datetime.now().timestamp())

    for order in orders:
        order_date = parse_iso_datetime(order["order_date"])

        for item in order["items"]:
            cursor.execute("""
                INSERT INTO STAGING.STG_SALES (
                    batch_id,
                    id_mongo,
                    order_id,
                    order_date_utc,
                    customer_id,
                    customer_name,
                    customer_email,
                    customer_document,
                    product_id,
                    product_name,
                    product_category,
                    quantity,
                    unit_price,
                    discount_value,
                    payment_method,
                    payment_status,
                    installments,
                    shipping_city,
                    shipping_state,
                    shipping_country,
                    shipping_value,
                    source_system
                ) VALUES (
                    :1,:2,:3,:4,:5,:6,:7,:8,:9,:10,
                    :11,:12,:13,:14,:15,:16,:17,:18,
                    :19,:20,:21,:22
                )
            """, (
                batch_id,
                order["_id"],
                order["order_id"],
                order_date,  # datetime Python
                order["customer"]["customer_id"],
                order["customer"]["name"],
                order["customer"]["email"],
                order["customer"]["document"],
                item["product_id"],
                item["product_name"],
                item["category"],
                item["quantity"],
                item["unit_price"],
                item["discount"],
                order["payment"]["method"],
                order["payment"]["status"],
                order["payment"]["installments"],
                order["shipping"]["city"],
                order["shipping"]["state"],
                order["shipping"]["country"],
                order["shipping"]["shipping_value"],
                "MONGODB"
            ))

    return batch_id


# =========================
# DIM CUSTOMER (SCD 2)
# =========================
def load_dim_customer(cursor):
    cursor.execute("""
        SELECT DISTINCT
            customer_id,
            customer_name,
            customer_email,
            customer_document
        FROM STAGING.STG_SALES
    """)

    for cust_id, name, email, doc in cursor.fetchall():

        cursor.execute("""
            SELECT sk_customer, name, email
            FROM DW.DIM_CUSTOMER
            WHERE bk_customer_id = :1
              AND fl_ativo = 'S'
        """, (cust_id,))

        row = cursor.fetchone()

        if row:
            sk, old_name, old_email = row
            if old_name != name or old_email != email:
                cursor.execute("""
                    UPDATE DW.DIM_CUSTOMER
                    SET dt_final = SYSDATE,
                        fl_ativo = 'N'
                    WHERE sk_customer = :1
                """, (sk,))
            else:
                continue

        sk_new = get_next_sk(cursor, "DW.DIM_CUSTOMER", "sk_customer")

        cursor.execute("""
            INSERT INTO DW.DIM_CUSTOMER (
                sk_customer,
                bk_customer_id,
                name,
                email,
                document,
                dt_inicial,
                dt_final,
                fl_ativo
            ) VALUES (
                :1,:2,:3,:4,:5,SYSDATE,NULL,'S'
            )
        """, (sk_new, cust_id, name, email, doc))


# =========================
# DIM PRODUCT (SCD 2)
# =========================
def load_dim_product(cursor):
    cursor.execute("""
        SELECT DISTINCT
            product_id,
            product_name,
            product_category
        FROM STAGING.STG_SALES
    """)

    for prod_id, name, cat in cursor.fetchall():

        cursor.execute("""
            SELECT sk_product, name, category
            FROM DW.DIM_PRODUCT
            WHERE bk_product_id = :1
              AND fl_ativo = 'S'
        """, (prod_id,))

        row = cursor.fetchone()

        if row:
            sk, old_name, old_cat = row
            if old_name != name or old_cat != cat:
                cursor.execute("""
                    UPDATE DW.DIM_PRODUCT
                    SET dt_final = SYSDATE,
                        fl_ativo = 'N'
                    WHERE sk_product = :1
                """, (sk,))
            else:
                continue

        sk_new = get_next_sk(cursor, "DW.DIM_PRODUCT", "sk_product")

        cursor.execute("""
            INSERT INTO DW.DIM_PRODUCT (
                sk_product,
                bk_product_id,
                name,
                category,
                dt_inicial,
                dt_final,
                fl_ativo
            ) VALUES (
                :1,:2,:3,:4,SYSDATE,NULL,'S'
            )
        """, (sk_new, prod_id, name, cat))


# =========================
# DIM DATE
# =========================
def load_dim_date(cursor):
    cursor.execute("""
        SELECT DISTINCT TRUNC(order_date_utc)
        FROM STAGING.STG_SALES
    """)

    for (dt,) in cursor.fetchall():

        cursor.execute("""
            SELECT 1
            FROM DW.DIM_DATE
            WHERE date_value = :1
        """, (dt,))

        if cursor.fetchone():
            continue

        sk = get_next_sk(cursor, "DW.DIM_DATE", "sk_date")

        cursor.execute("""
            INSERT INTO DW.DIM_DATE (
                sk_date,
                date_value,
                year,
                month,
                day
            ) VALUES (
                :1, :2, :3, :4, :5
            )
        """, (
            sk,
            dt,
            dt.year,
            dt.month,
            dt.day
        ))


# =========================
# FACT SALES
# =========================
def load_fact_sales(cursor):
    cursor.execute("""
        SELECT
            s.order_id,
            s.quantity,
            s.unit_price,
            s.discount_value,
            s.shipping_value,
            s.payment_method,
            s.payment_status,
            c.sk_customer,
            p.sk_product,
            d.sk_date
        FROM STAGING.STG_SALES s
        JOIN DW.DIM_CUSTOMER c
          ON c.bk_customer_id = s.customer_id
         AND c.fl_ativo = 'S'
        JOIN DW.DIM_PRODUCT p
          ON p.bk_product_id = s.product_id
         AND p.fl_ativo = 'S'
        JOIN DW.DIM_DATE d
          ON d.date_value = TRUNC(s.order_date_utc)
    """)

    for (
        order_id,
        quantity,
        unit_price,
        discount_value,
        shipping_value,
        payment_method,
        payment_status,
        sk_customer,
        sk_product,
        sk_date
    ) in cursor.fetchall():

        sk_sale = get_next_sk(cursor, "DW.FCT_SALES", "sk_sale")

        gross_amount = quantity * unit_price
        net_amount = gross_amount - discount_value

        cursor.execute("""
            INSERT INTO DW.FCT_SALES (
                sk_sale,
                sk_customer,
                sk_product,
                sk_order_date,
                order_id,
                quantity,
                unit_price,
                discount_value,
                shipping_value,
                gross_amount,
                net_amount,
                payment_method,
                payment_status
            ) VALUES (
                :1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13
            )
        """, (
            sk_sale,
            sk_customer,
            sk_product,
            sk_date,
            order_id,
            quantity,
            unit_price,
            discount_value,
            shipping_value,
            gross_amount,
            net_amount,
            payment_method,
            payment_status
        ))

# =========================
# MAIN
# =========================


def main():
    conn = oracledb.connect(**ORACLE_CONFIG)
    cursor = conn.cursor()

    orders = list(extract_orders())

    load_staging(cursor, orders)
    load_dim_customer(cursor)
    load_dim_product(cursor)
    load_dim_date(cursor)
    load_fact_sales(cursor)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
