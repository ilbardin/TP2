import axios from 'axios';
import mysql from 'mysql2/promise';

async function main() {
    const connection = await mysql.createConnection({
        host: 'localhost',
        user: 'root',
        password: 'barnach',
        database: 'tp2_node'
    });

    try {
        const [rows] = await connection.execute('SELECT 1');
        console.log(rows);
    } catch (err) {
        console.error('Error executing query:', err);
    }

    await migrarDatos(connection);
    await connection.end();
}

async function migrarDatos(connection) {
    for (let i = 1; i < 1000; i++) {
        const code = i.toString().padStart(3, '0');
        const url = `https://restcountries.com/v3.1/alpha/${code}`;

        try {
            const response = await axios.get(url);
            const data = response.data;
            if (data && data.length > 0) {
                const pais = data[0];
                const codigoPais = parseInt(code);
                const nombrePais = pais.name?.common || '';
                const capitalPais = pais.capital?.[0] || '';
                const region = pais.region || '';
                const subregion = pais.subregion || '';
                const poblacion = pais.population || 0;
                const [latitud, longitud] = pais.latlng || [0, 0];

                const sql = `
                    INSERT INTO Pais (codigoPais, nombrePais, capitalPais, region, subregion, poblacion, latitud, longitud)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                `;

                await connection.execute(sql, [codigoPais, nombrePais, capitalPais, region, subregion, poblacion, latitud, longitud]);
            }
        } catch (error) {
            console.warn(`Skipping country code ${code} due to error:`, error.message);
        }
    }
}

main().catch(console.error);
