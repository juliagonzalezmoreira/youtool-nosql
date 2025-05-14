import os
from pymongo import MongoClient
from dotenv import load_dotenv

def reset_database():
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")

    if not mongo_uri or not db_name:
        print("Verifique se MONGO_URI e DB_NAME estão definidos no .env")
        return

    client = MongoClient(mongo_uri)
    db = client[db_name]

    collections = db.list_collection_names()
    if not collections:
        print(f"Nenhuma coleção encontrada em '{db_name}'.")
        return

    print(f"Apagando coleções do banco '{db_name}'...")
    for name in collections:
        db[name].drop()
        print(f"✅ Coleção '{name}' removida.")

    print("Banco limpo com sucesso!")

if __name__ == "__main__":
    reset_database()
