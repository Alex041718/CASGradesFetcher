-- Suppression du schema si il existe
DROP SCHEMA IF EXISTS db;

-- Création du schema :
CREATE SCHEMA db;

-- Utilisation du schema
USE db;

CREATE TABLE _notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data JSON
);