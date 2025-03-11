-- Job 14

-- Sélectionner les étudiants dont l'âge est compris entre 18 et 25 ans, triés par âge croissant
USE LaPlateforme;

SELECT * FROM etudiant 
WHERE age >= 18 AND age <= 25
ORDER BY age ASC;
