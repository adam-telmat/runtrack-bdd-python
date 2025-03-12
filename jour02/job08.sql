-- Création de la base de données zoo
CREATE DATABASE IF NOT EXISTS zoo;
USE zoo;

-- Création de la table cage
CREATE TABLE IF NOT EXISTS cage (
    id INT PRIMARY KEY AUTO_INCREMENT,
    superficie FLOAT,
    capacite_max INT
);

-- Création de la table animal
CREATE TABLE IF NOT EXISTS animal (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255),
    race VARCHAR(255),
    id_cage INT,
    date_naissance DATE,
    pays_origine VARCHAR(255),
    FOREIGN KEY (id_cage) REFERENCES cage(id)
);

-- Requête pour ajouter une cage
-- INSERT INTO cage (superficie, capacite_max) VALUES (100, 5);

-- Requête pour ajouter un animal
-- INSERT INTO animal (nom, race, id_cage, date_naissance, pays_origine) 
-- VALUES ('Leo', 'Lion', 1, '2018-05-12', 'Kenya');

-- Requête pour afficher tous les animaux avec les informations de leur cage
-- SELECT a.id, a.nom, a.race, a.id_cage, a.date_naissance, a.pays_origine, c.superficie, c.capacite_max
-- FROM animal a
-- JOIN cage c ON a.id_cage = c.id
-- ORDER BY a.id;

-- Requête pour afficher les cages et le nombre d'animaux qu'elles contiennent
-- SELECT c.id, c.superficie, c.capacite_max, COUNT(a.id) as nb_animaux
-- FROM cage c
-- LEFT JOIN animal a ON c.id = a.id_cage
-- GROUP BY c.id
-- ORDER BY c.id;

-- Requête pour calculer la superficie totale des cages
-- SELECT SUM(superficie) FROM cage; 