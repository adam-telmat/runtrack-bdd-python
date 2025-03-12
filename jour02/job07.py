import mysql.connector

class Employe:
    def __init__(self, host="localhost", user="root", password="", database="entreprise"):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()
        
    def create_tables(self):
        # Création de la table employe si elle n'existe pas
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS employe (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nom VARCHAR(255),
            prenom VARCHAR(255),
            salaire DECIMAL(10,2),
            id_service INT
        )
        """)
        
        # Création de la table service si elle n'existe pas
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS service (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nom VARCHAR(255)
        )
        """)
        
        self.connection.commit()
        
    def create_employe(self, nom, prenom, salaire, id_service):
        # Ajouter un employé
        query = "INSERT INTO employe (nom, prenom, salaire, id_service) VALUES (%s, %s, %s, %s)"
        values = (nom, prenom, salaire, id_service)
        self.cursor.execute(query, values)
        self.connection.commit()
        return self.cursor.lastrowid
        
    def read_employe(self, employe_id=None):
        # Lire un employé spécifique ou tous les employés
        if employe_id:
            query = "SELECT * FROM employe WHERE id = %s"
            self.cursor.execute(query, (employe_id,))
            return self.cursor.fetchone()
        else:
            query = "SELECT * FROM employe"
            self.cursor.execute(query)
            return self.cursor.fetchall()
            
    def update_employe(self, employe_id, nom=None, prenom=None, salaire=None, id_service=None):
        # Mettre à jour un employé
        updates = []
        values = []
        
        if nom:
            updates.append("nom = %s")
            values.append(nom)
        if prenom:
            updates.append("prenom = %s")
            values.append(prenom)
        if salaire:
            updates.append("salaire = %s")
            values.append(salaire)
        if id_service:
            updates.append("id_service = %s")
            values.append(id_service)
            
        if not updates:
            return False
            
        query = f"UPDATE employe SET {', '.join(updates)} WHERE id = %s"
        values.append(employe_id)
        
        self.cursor.execute(query, tuple(values))
        self.connection.commit()
        return self.cursor.rowcount > 0
        
    def delete_employe(self, employe_id):
        # Supprimer un employé
        query = "DELETE FROM employe WHERE id = %s"
        self.cursor.execute(query, (employe_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0
        
    def create_service(self, nom):
        # Ajouter un service
        query = "INSERT INTO service (nom) VALUES (%s)"
        self.cursor.execute(query, (nom,))
        self.connection.commit()
        return self.cursor.lastrowid
        
    def get_employes_with_service(self):
        # Récupérer tous les employés avec leur service
        query = """
        SELECT e.id, e.nom, e.prenom, e.salaire, s.nom as service
        FROM employe e
        LEFT JOIN service s ON e.id_service = s.id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
        
    def get_employes_high_salary(self):
        # Récupérer les employés avec un salaire > 3000
        query = "SELECT * FROM employe WHERE salaire > 3000"
        self.cursor.execute(query)
        return self.cursor.fetchall()
        
    def close(self):
        # Fermer la connexion
        self.cursor.close()
        self.connection.close()

# Fonction principale pour tester la classe
def main():
    try:
        # Création de la base de données si elle n'existe pas
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS entreprise")
        cursor.close()
        connection.close()
        
        # Initialisation de la classe Employe
        employe_manager = Employe()
        
        # Création des tables
        employe_manager.create_tables()
        
        # Ajout des services
        services = ["Informatique", "Ressources Humaines", "Comptabilité", "Direction", "Commercial"]
        service_ids = {}
        for service in services:
            service_ids[service] = employe_manager.create_service(service)
        
        # Ajout des employés
        employes = [
            ("Dupont", "Jean", 3500.00, service_ids["Commercial"]),
            ("Martin", "Marie", 3200.00, service_ids["Ressources Humaines"]),
            ("Durand", "Pierre", 2800.00, service_ids["Comptabilité"]),
            ("Lefebvre", "Sophie", 4200.00, service_ids["Direction"]),
            ("Garcia", "Thomas", 3100.00, service_ids["Commercial"])
        ]
        
        for nom, prenom, salaire, id_service in employes:
            employe_manager.create_employe(nom, prenom, salaire, id_service)
        
        # Récupération des employés avec un salaire > 3000
        print("Employés avec un salaire supérieur à 3000 € :")
        high_salary_employes = employe_manager.get_employes_high_salary()
        for employe in high_salary_employes:
            print(f"ID: {employe[0]}, Nom: {employe[1]}, Prénom: {employe[2]}, Salaire: {employe[3]} €")
        
        # Récupération des employés avec leur service
        print("\nListe des employés avec leur service :")
        employes_with_service = employe_manager.get_employes_with_service()
        for employe in employes_with_service:
            print(f"ID: {employe[0]}, Nom: {employe[1]}, Prénom: {employe[2]}, Salaire: {employe[3]} €, Service: {employe[4]}")
        
        # Fermeture de la connexion
        employe_manager.close()
        
    except mysql.connector.Error as err:
        print(f"Erreur: {err}")

if __name__ == "__main__":
    main() 