# Guia de Execução do Ambiente MongoDB e Geração dos Documentos

## 1. Subir o Docker

### Pré-requisitos

-   Docker instalado
-   Docker Compose instalado
-   Arquivo `docker-compose.yml` na raiz do projeto

### Comando

No diretório do projeto:

    docker compose up -d

### Verificar se o container está rodando

    docker ps

O container `mongo_sales` deve aparecer na lista.

------------------------------------------------------------------------

## 2. Gerar os Documentos (5.000 registros)

### Instalar dependências

    pip install -r requirements.txt

### Executar o gerador

    python -m data_generator.main

### Saída esperada

    Gerados: 5000

------------------------------------------------------------------------

## 3. Visualizar Documentos Criados

    python -m view_data

Isso exibirá os primeiros 5 documentos da coleção.

------------------------------------------------------------------------

## 4. Apagar Todos os Documentos (opcional)

    python - <<EOF
    from view_data import drop_content
    drop_content()
    EOF

Saída esperada:

    Removidos: 5000
