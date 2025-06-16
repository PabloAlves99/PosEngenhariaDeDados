import os
from typing import Optional, Union, List, Dict
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertOneResult, DeleteResult, UpdateResult, InsertManyResult
from pymongo.cursor import Cursor

from dotenv import load_dotenv
load_dotenv()


class BDMongo:
    def __init__(self, uri: str, database: str = 'mydatabase') -> None:
        self.uri: str = uri
        self.client: MongoClient = MongoClient(
            self.uri, server_api=ServerApi('1'))
        self.db: Database = self.client[database]
        self.collection: Collection = self.get_collection(database)

    def get_collection(self, collection_name: str) -> Collection:
        """Seleciona e retorna uma coleção."""
        self.collection = self.db[collection_name]
        return self.collection

    def insert_one_data(self, data: Dict) -> Optional[InsertOneResult]:
        """Insere um único documento na coleção."""
        try:
            return self.collection.insert_one(data)
        except errors.PyMongoError as e:
            print(f"Erro ao inserir um documento: {e}")
            return None

    def insert_many_data(self, data_list: List[Dict]) -> Optional[InsertManyResult]:
        """Insere múltiplos documentos na coleção."""
        try:
            return self.collection.insert_many(data_list)
        except errors.PyMongoError as e:
            print(f"Erro ao inserir múltiplos documentos: {e}")
            return None

    def delete_one_data(self, data: Dict) -> Optional[DeleteResult]:
        """Deleta um documento da coleção."""
        try:
            return self.collection.delete_one(data)
        except errors.PyMongoError as e:
            print(f"Erro ao deletar: {e}")
            return None

    def delete_many_data(self, data: Dict) -> Optional[DeleteResult]:
        """Deleta vários documentos da coleção."""
        try:
            return self.collection.delete_many(data)
        except errors.PyMongoError as e:
            print(f"Erro ao deletar muitos: {e}")
            return None

    def update_one_data(self, _filter: Dict, new_data: Dict) -> Optional[UpdateResult]:
        """Atualiza um documento da coleção."""
        try:
            return self.collection.update_one(_filter, new_data)
        except errors.PyMongoError as e:
            print(f"Erro ao atualizar: {e}")
            return None

    def update_many_data(self, _filter: Dict, new_data: Dict) -> Optional[UpdateResult]:
        """Atualiza vários documentos da coleção."""
        try:
            return self.collection.update_many(_filter, new_data)
        except errors.PyMongoError as e:
            print(f"Erro ao atualizar muitos: {e}")
            return None

    def drop_collection(self, collection_name: str) -> None:
        """Apaga uma coleção inteira do banco."""
        try:
            self.db.drop_collection(collection_name)
            print(f"Collection '{collection_name}' dropped successfully.")
        except errors.PyMongoError as e:
            print(f"Erro ao apagar coleção: {e}")

    def find(self, query: Optional[Dict] = None) -> Union[List[Dict], Cursor]:
        """Busca documentos na coleção."""
        if query is None:
            query = {}
        try:
            return self.collection.find(query)
        except errors.PyMongoError as e:
            print(f"Erro ao buscar documentos: {e}")
            return []

    def close(self) -> None:
        """Fecha a conexão com o banco."""
        self.client.close()


def main():
    uri = os.getenv("URI_MONGO")
    collections = ['usuarios', 'produtos', 'pedidos', 'itens_pedido']

    if not uri:
        raise ValueError("❗ URI_MONGO não configurada no .env")

    print("\n🔗 Conectando ao MongoDB...\n")
    db = BDMongo(uri)
    try:
        for collection in collections:
            db.get_collection(collection)
            print(f"\n✅ Coleção '{collection}' conectada com sucesso.")

            # Inserir 5 documentos de exemplo
            if collection == 'usuarios':
                dados = [
                    {"nome": "Ana", "email": "ana@example.com"},
                    {"nome": "Bruno", "email": "bruno@example.com"},
                    {"nome": "Carlos", "email": "carlos@example.com"},
                    {"nome": "Diana", "email": "diana@example.com"},
                    {"nome": "Eduardo", "email": "eduardo@example.com"},
                ]
                filtro_update = {"nome": "Carlos"}
                novos_dados = {"$set": {"email": "carlos@novoemail.com"}}
                filtro_delete = {"nome": "Eduardo"}

            elif collection == 'produtos':
                dados = [
                    {"nome": "Notebook", "preco": 3500.0},
                    {"nome": "Mouse", "preco": 80.0},
                    {"nome": "Teclado", "preco": 150.0},
                    {"nome": "Monitor", "preco": 900.0},
                    {"nome": "Webcam", "preco": 200.0},
                ]
                filtro_update = {"nome": "Mouse"}
                novos_dados = {"$set": {"preco": 75.0}}
                filtro_delete = {"nome": "Webcam"}

            elif collection == 'pedidos':
                dados = [
                    {"usuario": "Ana", "data": "2025-06-10"},
                    {"usuario": "Bruno", "data": "2025-06-11"},
                    {"usuario": "Carlos", "data": "2025-06-12"},
                    {"usuario": "Diana", "data": "2025-06-13"},
                    {"usuario": "Eduardo", "data": "2025-06-14"},
                ]
                filtro_update = {"usuario": "Bruno"}
                novos_dados = {"$set": {"data": "2025-06-01"}}
                filtro_delete = {"usuario": "Eduardo"}

            elif collection == 'itens_pedido':
                dados = [
                    {"pedido_id": 1, "produto": "Notebook", "quantidade": 1},
                    {"pedido_id": 2, "produto": "Mouse", "quantidade": 2},
                    {"pedido_id": 3, "produto": "Teclado", "quantidade": 1},
                    {"pedido_id": 4, "produto": "Monitor", "quantidade": 2},
                    {"pedido_id": 5, "produto": "Webcam", "quantidade": 1},
                ]
                filtro_update = {"produto": "Teclado"}
                novos_dados = {"$set": {"quantidade": 3}}
                filtro_delete = {"produto": "Webcam"}

            else:
                dados, filtro_update, novos_dados, filtro_delete = [], {}, {}, {}

            # Inserção
            result_insert = db.insert_many_data(dados)
            if result_insert:
                print(
                    f"📝 Inseridos {len(dados)} documentos em '{collection}'.")

            # Atualização
            result_update = db.update_one_data(filtro_update, novos_dados)
            if result_update and result_update.modified_count > 0:
                print(f"🔁 Documento atualizado em '{collection}'.")
            else:
                print(f"⚠️ Nenhum documento atualizado em '{collection}'.")

            # Exclusão
            result_delete = db.delete_one_data(filtro_delete)
            if result_delete and result_delete.deleted_count > 0:
                print(f"❌ Documento excluído de '{collection}'.")
            else:
                print(f"⚠️ Nenhum documento excluído de '{collection}'.")

    except Exception as e:
        print(f"\n❌ Erro durante a execução: {e}")

    finally:
        print("\n🧨 Finalizando...")
        db.close()
        print("✅ Conexão encerrada.")


if __name__ == "__main__":
    main()
