import mysql.connector
from pymongo import MongoClient

class AtbIndEstado:

    def __init__(self):
        self.id = 0                      
        self.ano = 0                     
        self.cod_estado = 0            
        self.nome_estado = ""           
        self.cod_municipio = 0         
        self.nome_municipio = ""       
        self.esperanca_nascer = ""      
        self.mortalidade = ""  

class Conecta:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="aula_puc", collection_name="IDH"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]


    def incluir(self, documento):
        resultado = self.collection.insert_one(documento)
        print(f"Documento inserido com _id: {resultado.inserted_id}")

    def abreConexao(self):
        self.con = mysql.connector.connect(host='localhost',  database='puc', port='1433',  user='root', password='mysql')
        if self.con.is_connected():
            db_info = self.con.get_server_info()
            print("Conectado ao servidor MySQL versão ", db_info)
            self.cursor = self.con.cursor()
    
    def fechaConexao(self):
        if self.con.is_connected():
            self.cursor.close()
            self.con.close()
            print("Conexão ao MySQL foi encerrada")

    def le_banco(self):
        url = "select * from indEstado"
        self.cursor.execute(url)
        result = self.cursor.fetchall()
        registros = []

        for dados in result:
            registro = AtbIndEstado()

            registro.id = dados[0]
            registro.ano = dados[1]
            registro.cod_estado = dados[2]
            registro.nome_estado = dados[3]
            registro.cod_municipio = dados[4]
            registro.nome_municipio = dados[5]
            registro.esperanca_nascer = dados[6]
            registro.mortalidade = dados[7]

            registros.append(registro) 
        return registros

if __name__ == "__main__":
    conecta = Conecta()
    conecta.abreConexao()
    lista = conecta.le_banco()
    conecta.fechaConexao()

    for p in lista:
        novo_doc = {
            "id": p.id,
            "ano": p.ano,
            "cod_estado": p.cod_estado,
            "nome_estado": p.nome_estado,
            "cod_municipio": p.cod_municipio,
            "nome_municipio": p.nome_municipio,
            "esperanca_nascer": p.esperanca_nascer,
            "mortalidade": p.mortalidade
        }
        conecta.incluir(novo_doc)


