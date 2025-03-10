-- Utilisation de la base de données "LaPlateforme"
USE LaPlateforme;

-- Création de la table "etudiant" avec les champs spécifiés
CREATE TABLE etudiant (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    prenom VARCHAR(25) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- Vérification de la création de la table
SHOW TABLES;
