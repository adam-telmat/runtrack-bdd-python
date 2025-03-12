-- Création de la base de données
CREATE DATABASE IF NOT EXISTS entreprise;
USE entreprise;

-- Création de la table employe
CREATE TABLE IF NOT EXISTS employe (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    salaire DECIMAL(10,2),
    id_service INT
);

-- Création de la table service
CREATE TABLE IF NOT EXISTS service (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255)
);

-- Insertion des services
INSERT INTO service (nom) VALUES 
('Informatique'),
('Ressources Humaines'),
('Comptabilité'),
('Direction'),
('Commercial');

-- Insertion des employés
INSERT INTO employe (nom, prenom, salaire, id_service) VALUES
('Dupont', 'Jean', 3500.00, 5),
('Martin', 'Marie', 3200.00, 2),
('Durand', 'Pierre', 2800.00, 3),
('Lefebvre', 'Sophie', 4200.00, 4),
('Garcia', 'Thomas', 3100.00, 5);

-- Requête pour récupérer les employés avec un salaire > 3000
SELECT * FROM employe WHERE salaire > 3000;

-- Requête pour récupérer les employés avec leur service
SELECT e.id, e.nom, e.prenom, e.salaire, s.nom as service
FROM employe e
LEFT JOIN service s ON e.id_service = s.id; 