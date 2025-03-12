import mysql.connector

try:
    # Connexion à la base de données
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="LaPlateforme"
    )
    
    # Création d'un curseur
    cursor = db.cursor()
    
    # Exécution de la requête pour récupérer les noms et capacités des salles
    cursor.execute("SELECT nom, capacite FROM salle")
    
    # Récupération des résultats
    salles = cursor.fetchall()
    
    # Affichage des résultats
    for salle in salles:
        nom, capacite = salle
        print(f"{nom} ({capacite})")
    
    # Fermeture du curseur et de la connexion
    cursor.close()
    db.close()
    
except mysql.connector.Error as err:
    print(f"Erreur: {err}") 