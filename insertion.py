
import pandas as pd
import mysql.connector
import logging
import re
db_config= {
    'host': 'localhost',
    'user': 'root',
    'password': '10080805Tohbi',
    'database': 'anstat_base_regionale'
}

# Fonction principale pour insérer des données à partir d'un fichier Excel
def insert_data_from_excel(excel_file):
    try:
        # Lecture du fichier Excel
        df = pd.read_excel(excel_file)

        # Vérification des colonnes attendues
        expected_columns = ['Année', 'Indicateurs', 'Dimension', 'Modalites', 'Valeurs']
        if not all(col in df.columns for col in expected_columns):
            logging.error("Erreur : Certaines colonnes attendues manquent dans le fichier Excel.")
            return

        # Nettoyage des colonnes pertinentes
        for col in expected_columns:
            df[col] = df[col].astype(str).str.strip()

        # Connexion à la base de données
        with mysql.connector.connect(**db_config) as mydb:
            with mydb.cursor(buffered=True) as cursor:
                # Charger les dimensions et modalités existantes
                cursor.execute("SELECT idDimensions, nomDimension FROM Dimensions")
                dimensions = {row[1]: row[0] for row in cursor.fetchall()}
                cursor.execute("SELECT idModalites, nomModalites, f_idDimensions FROM Modalites")
                modalites = {(row[1], row[2]): row[0] for row in cursor.fetchall()}

                # Traitement ligne par ligne du DataFrame
                for index, row in df.iterrows():
                    try:
                        # Récupérer ou ignorer si les valeurs principales sont manquantes
                        cursor.execute("SELECT idAnnees FROM Annees WHERE valAnnees = %s", (row['Année'],))
                        annee_id = cursor.fetchone()
                        if not annee_id:
                            logging.warning(f"Année introuvable pour la ligne {index + 1}. Ignorer cette ligne.")
                            continue

                        cursor.execute("SELECT idIndicateurs FROM Indicateurs WHERE nomIndicateur = %s", (row['Indicateurs'],))
                        indicateur_id = cursor.fetchone()
                        if not indicateur_id:
                            logging.warning(f"Indicateur introuvable pour la ligne {index + 1}. Ignorer cette ligne.")
                            continue

                        # Insérer les données principales
                        cursor.execute(
                            "INSERT INTO Donnees (f_idIndicateurs, f_idAnnees, valDonnees) VALUES (%s, %s, %s)",
                            (indicateur_id[0], annee_id[0], row['Valeurs'])
                        )
                        donnees_id = cursor.lastrowid
                        # Traitement des dimensions et modalités
                        dimensions_list = [dim.strip() for dim in re.split(r'\s*/\s*', row['Dimension']) if dim.strip()]
                        modalites_list = [mod.strip() for mod in re.split(r'\s*/\s*', row['Modalites']) if mod.strip()]

                        if len(dimensions_list) != len(modalites_list):
                            logging.warning(f"Incompatibilité Dimensions/Modalités pour la ligne {index + 1}. Ignorer cette ligne.")
                            continue

                        for dimension, modalite in zip(dimensions_list, modalites_list):
                            # Gestion des dimensions
                            dimension_id = dimensions.get(dimension)
                            if not dimension_id:
                                cursor.execute("INSERT INTO Dimensions (nomDimension) VALUES (%s)", (dimension,))
                                dimension_id = cursor.lastrowid
                                dimensions[dimension] = dimension_id

                            # Gestion des modalités
                            modalite_key = (modalite, dimension_id)
                            modalite_id = modalites.get(modalite_key)
                            if not modalite_id:
                                cursor.execute(
                                    "INSERT INTO Modalites (nomModalites, f_idDimensions) VALUES (%s, %s)",
                                    (modalite, dimension_id)
                                )
                                modalite_id = cursor.lastrowid
                                modalites[modalite_key] = modalite_id

                            # Associer modalités et données
                            cursor.execute(
                                "INSERT INTO Donnees_modalites (f_idDonnees, f_idModalites) VALUES (%s, %s)",
                                (donnees_id, modalite_id)
                            )

                    except Exception as e:
                        logging.error(f"Erreur lors du traitement de la ligne {index + 1}: {e}")
                        continue

                # Validation de la transaction
                mydb.commit()
                print("Données insérées avec succès !")

    except mysql.connector.Error as err:
        logging.error(f"Erreur MySQL : {err}")
    except FileNotFoundError:
        logging.error(f"Erreur : Fichier Excel '{excel_file}' non trouvé.")
    except Exception as e:
        logging.error(f"Une erreur est survenue : {e}")

# Chemin du fichier Excel
excel_file_path = "C:\\Users\\DELL\\OneDrive - ENSEA\\Desktop\\ANStat base\\Appliction_web\\data2.xlsx"

# Exécution du script
insert_data_from_excel(excel_file_path)