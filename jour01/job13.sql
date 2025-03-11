-- Job 13
-- Sélectionner les étudiants dont l'âge est entre 18 et 25 ans, excluant 18 et 25.

USE LaPlateforme;

SELECT * FROM etudiant WHERE age > 18 AND age < 25;
