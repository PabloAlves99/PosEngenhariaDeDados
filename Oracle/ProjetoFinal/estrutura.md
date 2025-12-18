├── ProjetoFinal/
│   ├── data_generator/          
│   ├── mongo/                   # Volume MongoDB
│   ├── oracle/                  # Volume Oracle XE
│   │
│   ├── 01_users.py   # Infra lógica Oracle (pré-requisitos)
│   ├── 02_tables.py   # Modelo dimensional (DDL)
│   ├── config.py                
│   │
│   ├──ETL.py
│   │
│   ├── docker-compose.yml       # Infra física (containers)
│   ├── requirements.txt         # Dependências Python
│   │
│   ├── transform.py             # tratamento dos dados
│   ├── view_data.py             # Validação / consulta
│   │
│   ├── estrutura.md             # Documentação arquitetural
│   ├── guia.md                  # Guia de execução
│   └── .gitignore