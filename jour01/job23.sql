-- Job 23
-- Récupérer les informations de l'étudiant le plus âgé

USE LaPlateforme;

SELECT * FROM etudiant WHERE age = (SELECT MAX(age) FROM etudiant);
