import requests
import pymysql

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='barnach',
        database='tp2',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("✅ Conexión exitosa a MySQL")

    with conn.cursor() as cursor:
        for i in range(1, 1000):
            code = str(i).zfill(3)
            url = f"https://restcountries.com/v3.1/alpha/{code}"

            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()

                if isinstance(data, list) and data:
                    pais = data[0]

                    codigoPais = int(code)
                    nombrePais = pais.get('name', {}).get('common', 'Desconocido')
                    capitalPais = pais.get('capital', ['Desconocida'])[0]
                    region = pais.get('region', 'Desconocida')
                    subregion = pais.get('subregion', 'Desconocida')
                    poblacion = pais.get('population', 0)
                    latlng = pais.get('latlng', [0, 0])
                    latitud = latlng[0]
                    longitud = latlng[1]

                    sql = """
                    INSERT INTO Pais (codigoPais, nombrePais, capitalPais, region, subregion, poblacion, latitud, longitud)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    nombrePais = VALUES(nombrePais), capitalPais = VALUES(capitalPais),
                    region = VALUES(region), subregion = VALUES(subregion),
                    poblacion = VALUES(poblacion), latitud = VALUES(latitud),
                    longitud = VALUES(longitud);
                    """
                    valores = (codigoPais, nombrePais, capitalPais, region, subregion, poblacion, latitud, longitud)
                    cursor.execute(sql, valores)
                    conn.commit()
                    print(f"✅ País {nombrePais} ({code}) insertado correctamente")

            except requests.exceptions.RequestException as e:
                print(f"⚠️ Error con código {code}: {e}")
                continue

except pymysql.MySQLError as e:
    print(f"❌ Error al conectar a MySQL: {e}")

finally:
    if 'conn' in locals() and conn.open:
        conn.close()
        print("🔌 Conexión cerrada correctamente")
