-- Job 20
-- Sélectionner la base de données
USE LaPlateforme;

-- Compter le nombre d'étudiants mineurs
SELECT COUNT(*) FROM etudiant WHERE age < 18;
