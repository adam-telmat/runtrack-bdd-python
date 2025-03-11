-- Job 17
-- Sélectionner la base de données
USE LaPlateforme;

-- Modifier l'âge de Betty Spaghetti (ID = 1)
UPDATE etudiant
SET age = 20
WHERE id = 1;

-- Vérifier la modification
SELECT * FROM etudiant WHERE id = 1;
