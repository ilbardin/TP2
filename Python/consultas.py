from pymongo import MongoClient

print("Conectando a la base de datos MongoDB...")
client = MongoClient('mongodb://localhost:27017/')
db = client['paises_db']
coleccion = db['paises']
print("Conexión establecida correctamente.")


# 6.1. Seleccionar documentos donde la región sea "Americas"
def consulta_region_americas():
    for pais in coleccion.find({"region": "Americas"}):
        print(pais)


# 6.2. Seleccionar documentos donde la región sea "Americas" y la población sea mayor a 100000000
def consulta_americas_millon():
    for doc in coleccion.find({"region": "Americas", "poblacion": {"$gt": 100000000}}):
        print(doc)


# 6.3. Seleccionar documentos donde la región sea distinta de "Africa"
def consulta_distinta_africa():
    for doc in coleccion.find({"region": {"$ne": "Africa"}}):
        print(doc)


# 6.4. Actualizar el documento donde el nombre (name) sea "Egypt"
coleccion.update_one(
    {"nombrePais": "Egypt"},
    {"$set": {"nombrePais": "Egipto", "poblacion": 95000000}}
)

# 6.5. Eliminar el documento donde el código del país sea 258
coleccion.delete_one({"codigoPais": 258})

# 6.6. Descripción de drop() en una colección y en una base de datos
#
#     drop() en una colección:
#     El método drop() elimina todos los documentos y los índices de la colección, borrándola completamente del sistema.
#
#     drop() en una base de datos:
#     Cuando se ejecuta dropDatabase() en una base de datos (o se selecciona la base y se ejecuta db.dropDatabase()
#     en el mongo shell), se elimina la base de datos completa junto con todas sus colecciones y sus datos.

# 6.7. Seleccionar documentos donde la población sea mayor a 50000000 y menor a 150000000
for doc in coleccion.find({"poblacion": {"$gt": 50000000, "$lt": 150000000}}):
    print(doc)

# 6.8. Seleccionar documentos ordenados por nombre (campo "nombrePais") de forma ascendente
for doc in coleccion.find().sort("nombrePais", 1):
    print(doc)

# 6.9. Descripción y ejemplo de skip() en una colección
cursor = coleccion.find().skip(5)
for doc in cursor:
    print(doc)

# 6.10. Uso de expresiones regulares en MongoDB vs. cláusula LIKE de SQL
# En MongoDB se pueden usar expresiones regulares para buscar patrones en cadenas. Por ejemplo, para buscar países cuyo
# nombre contenga la cadena "land" (sin importar mayúsculas/minúsculas):
for doc in coleccion.find({"nombrePais": {"$regex": ".*land.*", "$options": "i"}}):
    print(doc)

# Esto es equivalente a usar en SQL:
# SELECT * FROM paises WHERE nombrePais LIKE '%land%';

# 6.11. Creación de un índice en la colección "paises" para el campo "codigoPais"
coleccion.create_index({"codigoPais": 1})

# 6.12. Realizar un backup de la base de datos Mongo "paises_db"
# Para realizar un respaldo (backup) de la base de datos se puede utilizar la herramienta mongodump. Por ejemplo,
# desde la línea de comandos:
# mongodump --db paises_db --out /ruta/del/backup


consulta_region_americas()

consulta_americas_millon()

consulta_distinta_africa()
