from flask import Flask, request, jsonify, render_template,redirect,url_for
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

DB_CONFIG = {
    'host': "localhost",
    'user': "root",
    'password': '10080805Tohbi',  # Stockez le mot de passe dans une variable d'environnement
    'database': "anstat_base_regionale"
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/add')
def add_page():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT idIndicateurs, nomIndicateur FROM Indicateurs")
        indicateurs = cursor.fetchall()
        cursor.execute("SELECT idAnnees, valAnnees FROM Annees")
        annees = cursor.fetchall()  # Récupérer les années de la base de données

        return render_template('add.html', indicateurs=indicateurs, annees=annees)
    except Error as e:
        return jsonify({'error': f"Erreur de base de données : {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_dimensions', methods=['GET'])
def get_dimensions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT idDimensions, nomDimension FROM Dimensions")
        dimensions = cursor.fetchall()
        return jsonify(dimensions)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_modalites/<idDimension>', methods=['GET'])
def get_modalites(idDimension):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT idModalites, nomModalites FROM Modalites WHERE f_idDimensions = %s", (idDimension,))
        modalites = cursor.fetchall()
        return jsonify(modalites)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()




@app.route('/add_data', methods=['GET'])
def add_data():
    try:
        # Récupération des paramètres
        idIndicateur = request.args.get('idIndicateur')
        idAnnees = request.args.get('idAnnees')
        valeur = request.args.get('valeur')
        dimensions = request.args.getlist('dimensions[]')
        modalites_1 = request.args.getlist('modalites_1[]')
        modalites_2 = request.args.getlist('modalites_2[]')
        modalites_3 = request.args.getlist('modalites_3[]')
        modalites_4 = request.args.getlist('modalites_4[]')

        # Association des dimensions et modalités
        modalites = {}
        for i, dimension in enumerate(dimensions):
            if i == 0:
                modalites[dimension] = modalites_1
            elif i == 1:
                modalites[dimension] = modalites_2
            elif i == 2:
                modalites[dimension] = modalites_3
            elif i == 3:
                modalites[dimension] = modalites_4

        # Connexion à la base de données
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insertion des données principales
        cursor.execute("""
            INSERT INTO Donnees (f_idIndicateurs, f_idAnnees, valDonnees)
            VALUES (%s, %s, %s)
        """, (idIndicateur, idAnnees, valeur))
        conn.commit()
        idDonnees = cursor.lastrowid

        # Insertion des dimensions et modalités
        for dimension, mods in modalites.items():
            for mod in mods:
                cursor.execute("""
                    INSERT INTO Donnees_modalites (f_idDonnees, f_idModalites)
                    VALUES (%s, %s)
                """, (idDonnees, mod))
        conn.commit()

        return redirect(url_for('add_page'))

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    app.run(debug=True)
