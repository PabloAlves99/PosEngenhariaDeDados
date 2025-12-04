from typing import Optional, Union, List, Dict
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertOneResult, DeleteResult, UpdateResult


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

    def insert_data(self, data: Dict) -> Optional[InsertOneResult]:
        """Insere um documento na coleção."""
        try:
            return self.collection.insert_one(data)
        except errors.PyMongoError as e:
            print(f"Erro ao inserir: {e}")
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

    def find(self, query: Optional[Dict] = None) -> Union[List[Dict], Collection]:
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
