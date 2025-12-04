import os
from classe_mongo import BDMongo
from dotenv import load_dotenv

load_dotenv()


def test_insert(db: BDMongo, collection: str):
    print("\n🚀 Iniciando testes de inserção...\n")
    db.get_collection(collection)

    documentos = [
        {"Criador": "Pablo Alves", "Data": "2025-05-19", "Descrição": "Doc 1"},
        {"Criador": "Maria Silva", "Data": "2025-05-18", "Descrição": "Doc 2"},
        {"Criador": "João Souza", "Data": "2025-05-17", "Descrição": "Doc 3"},
        {"Criador": "Pablo Alves", "Data": "2025-05-16", "Descrição": "Doc 4"},
    ]

    for doc in documentos:
        result = db.insert_data(doc)
        if result:
            print(f"✅ Inserido ID: {result.inserted_id}")
        else:
            print("❌ Falha ao inserir documento.")

    print("\n📄 Documentos após inserção:")
    for doc in db.find():
        print(doc)


def test_update(db: BDMongo):
    print("\n🛠️ Iniciando testes de atualização...\n")

    filtro1 = {"Criador": "Maria Silva"}
    novo_valor1 = {"$set": {"Descrição": "Atualizado com sucesso"}}
    resultado1 = db.update_one_data(filtro1, novo_valor1)
    print(
        f"🔄 update_one modificou: {resultado1.modified_count if resultado1 else 0} documento(s)")

    filtro2 = {"Criador": "Pablo Alves"}
    novo_valor2 = {"$set": {"Descrição": "Atualização em massa"}}
    resultado2 = db.update_many_data(filtro2, novo_valor2)
    print(
        f"🔁 update_many modificou: {resultado2.modified_count if resultado2 else 0} documento(s)")

    print("\n📄 Documentos após atualizações:")
    for doc in db.find():
        print(doc)


def test_delete(db: BDMongo):
    print("\n🧹 Iniciando testes de deleção...\n")

    resultado1 = db.delete_one_data({"Criador": "João Souza"})
    print(
        f"🗑️ delete_one removeu: {resultado1.deleted_count if resultado1 else 0} documento(s)")

    resultado2 = db.delete_many_data({"Criador": "Pablo Alves"})
    print(
        f"🗑️ delete_many removeu: {resultado2.deleted_count if resultado2 else 0} documento(s)")

    print("\n📄 Documentos restantes na coleção:")
    for doc in db.find():
        print(doc)


def main():
    uri = os.getenv("URI_MONGO")
    collection = 'testcollection'

    if not uri:
        raise ValueError("❗ URI_MONGO não configurada no .env")

    print("\n🔗 Conectando ao MongoDB...\n")
    db = BDMongo(uri)

    try:
        test_insert(db, collection)
        test_update(db)
        test_delete(db)
    finally:
        print("\n🧨 Limpando coleção de testes...")
        db.drop_collection(collection)
        db.close()
        print("✅ Conexão encerrada.")


if __name__ == "__main__":
    main()
