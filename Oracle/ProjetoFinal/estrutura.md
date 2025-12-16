├── ProjetoFinal/
│   ├── data_generator/          
│   ├── mongo/                   # Volume MongoDB
│   ├── oracle/                  # Volume Oracle XE
│   │
│   ├── 01_bootstrap_oracle.py   # Infra lógica Oracle (pré-requisitos)
│   ├── 02_create_dw_tables.py   # Modelo dimensional (DDL)
│   ├── config.py                
│   │
│   ├── docker-compose.yml       # Infra física (containers)
│   ├── requirements.txt         # Dependências Python
│   │
│   ├── transform.py             # ETL (Mongo → STAGING → DW)
│   ├── view_data.py             # Validação / consulta
│   │
│   ├── estrutura.md             # Documentação arquitetural
│   ├── guia.md                  # Guia de execução
│   └── .gitignore