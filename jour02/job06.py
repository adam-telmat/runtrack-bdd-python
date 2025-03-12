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
    
    # Exécution de la requête pour calculer la capacité totale
    cursor.execute("SELECT SUM(capacite) FROM salle")
    
    # Récupération du résultat
    resultat = cursor.fetchone()[0]  # Le premier élément du premier tuple
    
    # Affichage du résultat
    print(f"La capacité totale des salles est de {resultat}")
    
    # Fermeture du curseur et de la connexion
    cursor.close()
    db.close()
    
except mysql.connector.Error as err:
    print(f"Erreur: {err}") 