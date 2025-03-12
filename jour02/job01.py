import mysql.connector

# Connexion à la base de données
try:
    # Établir la connexion à la base de données
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="LaPlateforme"
    )
    
    # Créer un curseur pour exécuter des requêtes SQL
    cursor = db.cursor()
    
    # Exécuter la requête pour récupérer tous les étudiants
    cursor.execute("SELECT * FROM etudiant")
    
    # Récupérer tous les résultats
    etudiants = cursor.fetchall()
    
    # Afficher les résultats
    print("Voici la liste des étudiants :")
    for etudiant in etudiants:
        print(etudiant)
    
    # Fermer le curseur et la connexion
    cursor.close()
    db.close()
    
except mysql.connector.Error as err:
    print(f"Erreur: {err}") 