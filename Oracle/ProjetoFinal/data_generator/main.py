from .generator import insert_documents

if __name__ == "__main__":
    QTD = 5000
    total = insert_documents(QTD)
    print(f"Documentos inseridos: {total}")
