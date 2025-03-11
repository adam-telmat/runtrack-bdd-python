-- Job 16
-- Récupérer tous les étudiants dont le prénom commence par un "B"

USE LaPlateforme;

SELECT * FROM etudiant WHERE prenom LIKE 'B%';
