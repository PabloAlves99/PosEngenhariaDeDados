import mysql.connector
import os

CAMINHO = os.path.dirname(__file__)

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

        
class IndEstado:
    
    def __init__(self):
        self.con = self.con = mysql.connector.connect(
            host='localhost',
            database='puc',
            user='root',
            password='mysql',
            port='1433',
        )
        if self.con.is_connected():
            db_info = self.con.get_server_info()
            print("Conectado ao servidor MySQL versão ", db_info)
            self.cursor = self.con.cursor()
  
    def fechaConexao(self):
        if self.con.is_connected():
            self.cursor.close()
            self.con.close()
            print("Conexão ao MySQL foi encerrada")
            
    def incluirDados(self, dados):
        if self.con.is_connected():
            sql = """
            INSERT INTO indEstado (
                id, ano, cod_estado, nome_estado, 
                cod_municipio, nome_municipio, esperanca_nascer, mortalidade
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (
                dados.id,
                dados.ano,
                dados.cod_estado,
                dados.nome_estado,
                dados.cod_municipio,
                dados.nome_municipio,
                dados.esperanca_nascer,
                dados.mortalidade
            )
            self.cursor.execute(sql, valores)
            self.con.commit()
        else:
            print("Conexão Fechada ...")



def le_arquivo(nomeArquivo):
    registros = []
    with open(f'{nomeArquivo}.csv', "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    indEst = IndEstado()

    id = 0
    for linha in linhas[1:]:
        dados = linha.strip().split(";")
        registro = AtbIndEstado()

        registro.id = id
        registro.ano = int(dados[0])
        registro.cod_estado = int(dados[1])
        registro.nome_estado = dados[2]
        registro.cod_municipio = int(dados[3])
        registro.nome_municipio = dados[4]
        registro.esperanca_nascer = dados[5]
        registro.mortalidade = dados[6]

        indEst.incluirDados(registro)
        registros.append(registro)
        id += 1

    indEst.fechaConexao()
    return registros



le_arquivo(fr'{CAMINHO}\IDH_MG')