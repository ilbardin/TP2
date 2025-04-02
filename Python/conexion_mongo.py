import requests
from pymongo import MongoClient

# Conexión a MongoDB
print("Conectando a la base de datos MongoDB...")
client = MongoClient('mongodb://localhost:27017/')
db = client['paises_db']
coleccion = db['paises']
print("Conexión establecida correctamente.")

for i in range(1, 301):
    code = str(i)
    url = f"https://restcountries.com/v3.1/alpha/{code}"
    print(f"Consultando datos para el código de país: {code}")

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            pais = data[0]
            documento = {
                "codigoPais": pais.get('callingCodes', [None])[0] if pais.get('callingCodes') else None,
                "nombrePais": pais.get('name', {}).get('common', ''),
                "capitalPais": pais.get('capital', [''])[0] if pais.get('capital') else '',
                "region": pais.get('region', ''),
                "poblacion": pais.get('population', 0),
                "latitud": pais.get('latlng', [None, None])[0],
                "longitud": pais.get('latlng', [None, None])[1],
                "superficie": pais.get('area', 0)
            }
            coleccion.insert_one(documento)
            print(f"Datos insertados para el país: {documento['nombrePais']}")
        else:
            print(f"No se encontraron datos para el código de país: {code}")
    else:
        print(f"Error {response.status_code} al consultar el código de país: {code}")
