import pymysql
import pandas as pd
from connect import get_mysql_connection
# Configuration de la base de données

def importer_domaines_excel(file):
    try:
        df = pd.read_excel(file, sheet_name="domaines")
        # Vérifier les colonnes requises et leurs types
        colonnes_requises = {'id':str,'domaines':str}
        for col, expected_type in colonnes_requises.items():
            if col not in df.columns:
                raise ValueError(f"Colonne manquante dans Excel : {col}")
            df[col] = df[col].astype(expected_type).fillna('')

        # Connexion à la base de données
        connection = get_mysql_connection()
        if not connection:
            return
        cursor = connection.cursor()

        # Préparer la requête SQL
        sql = "INSERT INTO Domaines(idDomaines ,nomDomaines ) VALUES (%s,%s)"
        print("Importation des données dans la base de données...")

        # Insérer les données dans la base
        for index, row in df.iterrows():
            try:
                valeurs = (row['id'],row['domaines'])#, row['definition']
                cursor.execute(sql, valeurs)
            except pymysql.Error as err:
                connection.rollback()
                print(f"Erreur à la ligne {index + 2} : {err}")
                continue

        # Valider les transactions
        connection.commit()
        print(f"{cursor.rowcount} Succès.")

    except FileNotFoundError:
        print(f"Fichier non trouvé : {file}")
    except pd.errors.ParserError:
        print("Erreur de lecture du fichier Excel. Vérifiez le format.")
    except ValueError as err:
        print(f"Erreur dans les données : {err}")
    except pymysql.Error as err:
        print(f"Erreur MySQL : {err}")
    finally:
        # Fermeture de la connexion
        if 'connection' in locals() and connection.open:
            connection.close()
            print("Connexion MySQL fermée.")

# Exemple d'utilisation
file_name = "C:\\Users\\DELL\\OneDrive - ENSEA\\Desktop\\ANStat base\\Appliction_web\\parametre1.xlsx"
importer_domaines_excel(file=file_name)
