# Guia de Execução 

## 1. Subir a Infraestrutura com Docker

### Pré-requisitos

* Docker instalado
* Docker Compose instalado
* Arquivo `docker-compose.yml` na raiz do projeto (`ProjetoFinal`)

### Comando

```bash
docker compose up -d
```

### Verificar containers ativos

```bash
docker ps
```

Containers esperados:

* `mongo_sales`
* `oracle_dw`

---

## 2. Instalar Dependências Python

Executar apenas uma vez:

```bash
pip install -r requirements.txt
```

---

## 3. Gerar Documentos no MongoDB (Origem)

### Executar o gerador

```bash
python data_generator/main.py
```

### Saída esperada

```text
Gerados: 5000
```

Isso popula a collection `orders` no banco `salesdb`.

---

## 4. Visualizar Documentos Criados no MongoDB

```bash
python view_data.py
```

### Comportamento

* Exibe os documentos originais
* Exibe os documentos formatados
* Mostra apenas uma amostra (ex.: 1 ou 5 registros)

---

## 5. Bootstrap do Oracle (Infra Lógica)

Cria os schemas necessários (`STAGING`, `DW`) e permissões.

```bash
python 01_bootstrap_oracle.py
```

### Resultado esperado

* Schemas criados (ou ignorados se já existirem)
* Grants aplicados
* Nenhuma tabela de negócio criada ainda

---

## 6. Criação do Modelo Dimensional (DDL)

Cria todas as tabelas, sequências e índices do Data Warehouse.

```bash
python 02_create_dw_tables.py
```

### Estruturas criadas

* `STAGING.STG_SALES`
* `STAGING.ETL_EXECUTION_LOG`
* `DW.DIM_CUSTOMER` (SCD Tipo 2)
* `DW.DIM_PRODUCT` (SCD Tipo 2)
* `DW.DIM_DATE`
* `DW.FCT_SALES`

---

## 7. Executar o Processo de Transformação (ETL)

Responsável por:

* Ler dados do MongoDB
* Normalizar strings (UPPER, TRIM, sem acento)
* Converter datas UTC → America/São_Paulo
* Calcular métricas de negócio
* Carregar dados na STAGING
* Aplicar SCD Tipo 2 nas dimensões
* Popular a tabela fato

### Execução

```bash
python transform.py
```


---

## Observações Importantes

* O Oracle não requer acesso manual via `sqlplus`
* Toda a infraestrutura lógica é criada via scripts Python
* A ordem de execução deve ser respeitada
