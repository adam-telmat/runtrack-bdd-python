-- Utilisation de la base de données LaPlateforme
USE LaPlateforme;

-- Création de la table etage
CREATE TABLE IF NOT EXISTS etage (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255),
    numero INT,
    superficie INT
);

-- Création de la table salle
CREATE TABLE IF NOT EXISTS salle (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255),
    id_etage INT,
    capacite INT
); 