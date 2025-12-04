from .generator import insert_documents

if __name__ == "__main__":
    qtd = 5000
    total = insert_documents(qtd)
    print(f"Documentos inseridos: {total}")
