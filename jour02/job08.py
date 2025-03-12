import mysql.connector

class ZooManager:
    def __init__(self, host="localhost", user="root", password=""):
        # Connexion à MySQL
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.connection.cursor()
        
        # Création de la base de données zoo si elle n'existe pas
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS zoo")
        self.cursor.execute("USE zoo")
        
        # Création des tables
        self.create_tables()
    
    def create_tables(self):
        # Création de la table cage
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS cage (
            id INT PRIMARY KEY AUTO_INCREMENT,
            superficie FLOAT,
            capacite_max INT
        )
        """)
        
        # Création de la table animal
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS animal (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nom VARCHAR(255),
            race VARCHAR(255),
            id_cage INT,
            date_naissance DATE,
            pays_origine VARCHAR(255),
            FOREIGN KEY (id_cage) REFERENCES cage(id)
        )
        """)
        
        self.connection.commit()
    
    def ajouter_cage(self, superficie, capacite_max):
        """Ajoute une cage et retourne son ID"""
        query = "INSERT INTO cage (superficie, capacite_max) VALUES (%s, %s)"
        self.cursor.execute(query, (superficie, capacite_max))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def modifier_cage(self, cage_id, superficie=None, capacite_max=None):
        """Modifie une cage existante"""
        updates = []
        values = []
        
        if superficie is not None:
            updates.append("superficie = %s")
            values.append(superficie)
        if capacite_max is not None:
            updates.append("capacite_max = %s")
            values.append(capacite_max)
            
        if not updates:
            return False
            
        query = f"UPDATE cage SET {', '.join(updates)} WHERE id = %s"
        values.append(cage_id)
        
        self.cursor.execute(query, tuple(values))
        self.connection.commit()
        return True
    
    def supprimer_cage(self, cage_id):
        """Supprime une cage si elle ne contient pas d'animaux"""
        # Vérifier si la cage contient des animaux
        self.cursor.execute("SELECT COUNT(*) FROM animal WHERE id_cage = %s", (cage_id,))
        count = self.cursor.fetchone()[0]
        
        if count > 0:
            print(f"Impossible de supprimer la cage {cage_id} car elle contient {count} animal(aux).")
            return False
        
        # Supprimer la cage
        self.cursor.execute("DELETE FROM cage WHERE id = %s", (cage_id,))
        self.connection.commit()
        return True
    
    def ajouter_animal(self, nom, race, id_cage, date_naissance, pays_origine):
        """Ajoute un animal et retourne son ID"""
        # Vérifier si la cage existe
        self.cursor.execute("SELECT capacite_max FROM cage WHERE id = %s", (id_cage,))
        result = self.cursor.fetchone()
        
        if not result:
            print(f"La cage {id_cage} n'existe pas.")
            return False
        
        capacite_max = result[0]
        
        # Vérifier si la cage a encore de la place
        self.cursor.execute("SELECT COUNT(*) FROM animal WHERE id_cage = %s", (id_cage,))
        count = self.cursor.fetchone()[0]
        
        if count >= capacite_max:
            print(f"La cage {id_cage} est pleine (capacité max: {capacite_max}).")
            return False
        
        # Ajouter l'animal
        query = """
        INSERT INTO animal (nom, race, id_cage, date_naissance, pays_origine) 
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (nom, race, id_cage, date_naissance, pays_origine))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def modifier_animal(self, animal_id, nom=None, race=None, id_cage=None, date_naissance=None, pays_origine=None):
        """Modifie un animal existant"""
        updates = []
        values = []
        
        if nom:
            updates.append("nom = %s")
            values.append(nom)
        if race:
            updates.append("race = %s")
            values.append(race)
        if id_cage:
            # Vérifier si la cage existe et a de la place
            self.cursor.execute("SELECT capacite_max FROM cage WHERE id = %s", (id_cage,))
            result = self.cursor.fetchone()
            
            if not result:
                print(f"La cage {id_cage} n'existe pas.")
                return False
            
            capacite_max = result[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM animal WHERE id_cage = %s", (id_cage,))
            count = self.cursor.fetchone()[0]
            
            if count >= capacite_max:
                print(f"La cage {id_cage} est pleine (capacité max: {capacite_max}).")
                return False
                
            updates.append("id_cage = %s")
            values.append(id_cage)
        if date_naissance:
            updates.append("date_naissance = %s")
            values.append(date_naissance)
        if pays_origine:
            updates.append("pays_origine = %s")
            values.append(pays_origine)
            
        if not updates:
            return False
            
        query = f"UPDATE animal SET {', '.join(updates)} WHERE id = %s"
        values.append(animal_id)
        
        self.cursor.execute(query, tuple(values))
        self.connection.commit()
        return True
    
    def supprimer_animal(self, animal_id):
        """Supprime un animal"""
        self.cursor.execute("DELETE FROM animal WHERE id = %s", (animal_id,))
        self.connection.commit()
        return True
    
    def afficher_tous_animaux(self):
        """Affiche tous les animaux du zoo"""
        self.cursor.execute("""
        SELECT a.id, a.nom, a.race, a.id_cage, a.date_naissance, a.pays_origine, c.superficie, c.capacite_max
        FROM animal a
        JOIN cage c ON a.id_cage = c.id
        ORDER BY a.id
        """)
        
        animaux = self.cursor.fetchall()
        
        if not animaux:
            print("Aucun animal dans le zoo.")
            return
        
        print("\n=== Liste de tous les animaux du zoo ===")
        print("ID | Nom | Race | Cage | Date de naissance | Pays d'origine | Superficie cage | Capacité max")
        print("-" * 100)
        
        for animal in animaux:
            animal_id, nom, race, id_cage, date_naissance, pays_origine, superficie, capacite_max = animal
            print(f"{animal_id} | {nom} | {race} | {id_cage} | {date_naissance} | {pays_origine} | {superficie} m² | {capacite_max}")
    
    def afficher_animaux_par_cage(self):
        """Affiche les animaux regroupés par cage"""
        self.cursor.execute("""
        SELECT c.id, c.superficie, c.capacite_max, COUNT(a.id) as nb_animaux
        FROM cage c
        LEFT JOIN animal a ON c.id = a.id_cage
        GROUP BY c.id
        ORDER BY c.id
        """)
        
        cages = self.cursor.fetchall()
        
        if not cages:
            print("Aucune cage dans le zoo.")
            return
        
        print("\n=== Liste des cages et leurs animaux ===")
        
        for cage in cages:
            cage_id, superficie, capacite_max, nb_animaux = cage
            print(f"\nCage {cage_id} - Superficie: {superficie} m² - Capacité: {capacite_max} - Animaux: {nb_animaux}")
            
            if nb_animaux > 0:
                self.cursor.execute("""
                SELECT id, nom, race, date_naissance, pays_origine
                FROM animal
                WHERE id_cage = %s
                """, (cage_id,))
                
                animaux = self.cursor.fetchall()
                
                print("  ID | Nom | Race | Date de naissance | Pays d'origine")
                print("  " + "-" * 80)
                
                for animal in animaux:
                    animal_id, nom, race, date_naissance, pays_origine = animal
                    print(f"  {animal_id} | {nom} | {race} | {date_naissance} | {pays_origine}")
    
    def calculer_superficie_totale(self):
        """Calcule et affiche la superficie totale des cages"""
        self.cursor.execute("SELECT SUM(superficie) FROM cage")
        superficie_totale = self.cursor.fetchone()[0] or 0
        print(f"\nLa superficie totale de toutes les cages est de {superficie_totale} m²")
        return superficie_totale
    
    def close(self):
        """Ferme la connexion à la base de données"""
        self.cursor.close()
        self.connection.close()

def menu():
    try:
        # Initialisation du gestionnaire de zoo
        zoo = ZooManager()
        
        # Ajouter quelques cages et animaux pour démonstration si la base est vide
        zoo.cursor.execute("SELECT COUNT(*) FROM cage")
        cage_count = zoo.cursor.fetchone()[0]
        
        if cage_count == 0:
            print("Initialisation de quelques données de démonstration...")
            cage1 = zoo.ajouter_cage(100, 5)
            cage2 = zoo.ajouter_cage(200, 10)
            cage3 = zoo.ajouter_cage(50, 2)
            
            zoo.ajouter_animal("Leo", "Lion", cage1, "2018-05-12", "Kenya")
            zoo.ajouter_animal("Dumbo", "Éléphant", cage2, "2015-03-20", "Inde")
            zoo.ajouter_animal("Simba", "Lion", cage1, "2019-07-15", "Tanzanie")
            zoo.ajouter_animal("Baloo", "Ours", cage3, "2017-11-30", "Canada")
            print("Données de démonstration ajoutées avec succès.")
        
        while True:
            print("\n===== GESTION DU ZOO =====")
            print("1. Ajouter un animal")
            print("2. Modifier un animal")
            print("3. Supprimer un animal")
            print("4. Ajouter une cage")
            print("5. Modifier une cage")
            print("6. Supprimer une cage")
            print("7. Afficher tous les animaux")
            print("8. Afficher les animaux par cage")
            print("9. Calculer la superficie totale des cages")
            print("0. Quitter")
            
            choix = input("\nVotre choix: ")
            
            if choix == "1":
                nom = input("Nom de l'animal: ")
                race = input("Race de l'animal: ")
                
                # Afficher les cages disponibles
                zoo.cursor.execute("SELECT id, superficie, capacite_max FROM cage")
                cages = zoo.cursor.fetchall()
                
                print("\nCages disponibles:")
                for cage in cages:
                    cage_id, superficie, capacite_max = cage
                    zoo.cursor.execute("SELECT COUNT(*) FROM animal WHERE id_cage = %s", (cage_id,))
                    nb_animaux = zoo.cursor.fetchone()[0]
                    print(f"ID: {cage_id}, Superficie: {superficie} m², Capacité: {capacite_max}, Occupée: {nb_animaux}/{capacite_max}")
                
                id_cage = int(input("ID de la cage: "))
                date_str = input("Date de naissance (AAAA-MM-JJ): ")
                pays_origine = input("Pays d'origine: ")
                
                animal_id = zoo.ajouter_animal(nom, race, id_cage, date_str, pays_origine)
                if animal_id:
                    print(f"L'animal {nom} a été ajouté avec succès (ID: {animal_id}).")
                else:
                    print("Échec de l'ajout de l'animal.")
            
            elif choix == "2":
                # Afficher les animaux existants
                zoo.afficher_tous_animaux()
                
                animal_id = int(input("\nID de l'animal à modifier: "))
                
                print("Laissez vide pour ne pas modifier")
                nom = input("Nouveau nom (ou vide): ")
                race = input("Nouvelle race (ou vide): ")
                
                id_cage_str = input("Nouvel ID de cage (ou vide): ")
                id_cage = int(id_cage_str) if id_cage_str else None
                
                date_str = input("Nouvelle date de naissance (AAAA-MM-JJ) (ou vide): ")
                pays_origine = input("Nouveau pays d'origine (ou vide): ")
                
                if zoo.modifier_animal(animal_id, 
                                      nom if nom else None, 
                                      race if race else None, 
                                      id_cage, 
                                      date_str if date_str else None, 
                                      pays_origine if pays_origine else None):
                    print(f"L'animal ID {animal_id} a été modifié avec succès.")
                else:
                    print("Échec de la modification de l'animal.")
            
            elif choix == "3":
                # Afficher les animaux existants
                zoo.afficher_tous_animaux()
                
                animal_id = int(input("\nID de l'animal à supprimer: "))
                
                if zoo.supprimer_animal(animal_id):
                    print(f"L'animal ID {animal_id} a été supprimé avec succès.")
                else:
                    print("Échec de la suppression de l'animal.")
            
            elif choix == "4":
                superficie = float(input("Superficie de la cage (m²): "))
                capacite_max = int(input("Capacité maximale de la cage: "))
                
                cage_id = zoo.ajouter_cage(superficie, capacite_max)
                print(f"La cage a été ajoutée avec succès. ID: {cage_id}")
            
            elif choix == "5":
                # Afficher les cages existantes
                zoo.cursor.execute("SELECT id, superficie, capacite_max FROM cage")
                cages = zoo.cursor.fetchall()
                
                print("\nCages existantes:")
                for cage in cages:
                    cage_id, superficie, capacite_max = cage
                    print(f"ID: {cage_id}, Superficie: {superficie} m², Capacité: {capacite_max}")
                
                cage_id = int(input("\nID de la cage à modifier: "))
                
                print("Laissez vide pour ne pas modifier")
                superficie_str = input("Nouvelle superficie (m²) (ou vide): ")
                capacite_str = input("Nouvelle capacité maximale (ou vide): ")
                
                superficie = float(superficie_str) if superficie_str else None
                capacite = int(capacite_str) if capacite_str else None
                
                if zoo.modifier_cage(cage_id, superficie, capacite):
                    print(f"La cage ID {cage_id} a été modifiée avec succès.")
                else:
                    print("Échec de la modification de la cage.")
            
            elif choix == "6":
                # Afficher les cages existantes
                zoo.cursor.execute("SELECT id, superficie, capacite_max FROM cage")
                cages = zoo.cursor.fetchall()
                
                print("\nCages existantes:")
                for cage in cages:
                    cage_id, superficie, capacite_max = cage
                    zoo.cursor.execute("SELECT COUNT(*) FROM animal WHERE id_cage = %s", (cage_id,))
                    nb_animaux = zoo.cursor.fetchone()[0]
                    print(f"ID: {cage_id}, Superficie: {superficie} m², Capacité: {capacite_max}, Animaux: {nb_animaux}")
                
                cage_id = int(input("\nID de la cage à supprimer: "))
                
                if zoo.supprimer_cage(cage_id):
                    print(f"La cage ID {cage_id} a été supprimée avec succès.")
                else:
                    print("Échec de la suppression de la cage.")
            
            elif choix == "7":
                zoo.afficher_tous_animaux()
            
            elif choix == "8":
                zoo.afficher_animaux_par_cage()
            
            elif choix == "9":
                zoo.calculer_superficie_totale()
            
            elif choix == "0":
                print("Au revoir!")
                zoo.close()
                break
            
            else:
                print("Choix invalide. Veuillez réessayer.")
    
    except mysql.connector.Error as err:
        print(f"Erreur MySQL: {err}")
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    menu() 