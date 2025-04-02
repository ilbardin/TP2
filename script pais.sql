CREATE TABLE Pais (
  codigoPais INT PRIMARY KEY,
  nombrePais VARCHAR(50) NOT NULL,
  capitalPais VARCHAR(50) NOT NULL,
  region VARCHAR(50) NOT NULL,
  subregion VARCHAR(50) NOT NULL,
  poblacion BIGINT NOT NULL,
  latitud DECIMAL(10,6) NOT NULL,
  longitud DECIMAL(10,6) NOT NULL
);
