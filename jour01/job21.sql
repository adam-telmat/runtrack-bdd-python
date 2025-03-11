-- Job 21
-- Sélectionner la base de données
USE LaPlateforme;

-- Compter le nombre d'étudiants âgés entre 18 et 25 ans
SELECT COUNT(*) FROM etudiant WHERE age BETWEEN 18 AND 25;
