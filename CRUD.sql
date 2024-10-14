CREATE DATABASE IF NOT EXISTS clientesdb;
USE clientesdb;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(100),
    apellidos VARCHAR(100),
    sexo ENUM('M', 'F')
);

select * from usuarios;