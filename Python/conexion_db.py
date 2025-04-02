from pymongo import MongoClient

def get_database():
    """Establece la conexión con MongoDB y devuelve la colección"""
    print("Conectando a la base de datos MongoDB...")
    client = MongoClient('mongodb://localhost:27017/')
    db = client['paises_db']
    print("Conexión establecida correctamente.")
    return db['paises']
