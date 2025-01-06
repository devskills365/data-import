# .\.venv\Scripts\Activate   
from sqlalchemy import create_engine, text
import pymysql
import pandas as pd
import mysql.connector
# Configuration de la base de données


def get_mysql_connection():
    config = {
    'host': 'localhost',
    'user': 'root',
    'password': '10080805Tohbi',
    'database': 'anstat_base_regionale'
}
  
    try:
        connection = pymysql.connect(**config)
        print("Connexion réussie à MySQL !")
        return connection
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la connexion à MySQL : {e}")
        return None

get_mysql_connection()

