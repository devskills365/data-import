import pandas as pd
from sqlalchemy import create_engine

# 1. Connexion à la base de données MySQL
engine = create_engine("mysql+pymysql://username:password@localhost/SchemaRegionale")

# 2. Lecture du fichier Excel
# Remplacez 'fichier.xlsx' par le chemin de votre fichier Excel
excel_file = 'data.xlsx'
data = pd.read_excel(excel_file)

# 3. Traitement des données pour les adapter à la base
def prepare_data(row):
    # Séparer les dimensions et modalités
    dimensions = row['Dimension'].split(" / ")  # Gestion des sous-dimensions
    modalites = row['Modalites'].split(" / ")

    # Retourner un dictionnaire prêt pour l'insertion
    return {
        "nomDimension": dimensions[-1],  # Dernière dimension
        "nomModalites": modalites[-1],  # Dernière modalité
        "nomIndicateur": row['Indicateurs'],
        "valAnnees": row['Année'],
        "valDonnees": row['Valeurs']
    }

processed_data = data.apply(prepare_data, axis=1).tolist()

# 4. Insérer les données dans les tables correspondantes
with engine.connect() as connection:
    for item in processed_data:
        # 4.1. Insérer les dimensions si elles n'existent pas
        connection.execute("""
            INSERT IGNORE INTO Dimensions (nomDimension) VALUES (%s)
        """, (item['nomDimension'],))

        # 4.2. Récupérer l'idDimensions
        result = connection.execute("""
            SELECT idDimensions FROM Dimensions WHERE nomDimension = %s
        """, (item['nomDimension'],))
        id_dimensions = result.fetchone()['idDimensions']

        # 4.3. Insérer les modalités si elles n'existent pas
        connection.execute("""
            INSERT IGNORE INTO Modalites (idDimensions, nomModalites) VALUES (%s, %s)
        """, (id_dimensions, item['nomModalites']))

        # 4.4. Récupérer l'idModalites
        result = connection.execute("""
            SELECT idModalites FROM Modalites WHERE nomModalites = %s
        """, (item['nomModalites'],))
        id_modalites = result.fetchone()['idModalites']

        # 4.5. Insérer les années si elles n'existent pas
        connection.execute("""
            INSERT IGNORE INTO Annees (valAnnees) VALUES (%s)
        """, (item['valAnnees'],))

        # 4.6. Récupérer l'idAnnees
        result = connection.execute("""
            SELECT idAnnees FROM Annees WHERE valAnnees = %s
        """, (item['valAnnees'],))
        id_annees = result.fetchone()['idAnnees']

        # 4.7. Insérer les données dans la table Donnees
        connection.execute("""
            INSERT INTO Donnees (idIndicateurs, idAnnees, valDonnees) 
            VALUES (%s, %s, %s)
        """, (id_modalites, id_annees, item['valDonnees']))
