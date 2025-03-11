-- Job 12
-- Utilisation de la base de données "LaPlateforme"
USE LaPlateforme;

-- Ajouter un nouvel étudiant : Martin Dupuis
INSERT INTO etudiant (nom, prenom, age, email)
VALUES ('Dupuis', 'Martin', 18, 'martin.dupuis@laplateforme.io');

-- Récupérer les membres de la famille "Dupuis"
SELECT * FROM etudiant WHERE nom = 'Dupuis';
