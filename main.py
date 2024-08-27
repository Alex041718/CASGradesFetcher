import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import mysql.connector
import json
import schedule
import time

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Informations d'authentification et de plateforme
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
domain = os.getenv('DOMAIN')
cas_domain = os.getenv('CAS_DOMAIN')

# Informations de connexion à la base de données
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

def get_csrf_token(session, cas_server_url):
    """Récupère le jeton CSRF depuis la page de login CAS."""
    response = session.get(cas_server_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find('input', {'name': 'execution'}).get('value')

def authenticate(session, cas_server_url, username, password, csrf_token):
    """Effectue l'authentification CAS avec les informations fournies."""
    payload = {
        'username': username,
        'password': password,
        'execution': csrf_token,
        '_eventId': 'submit',
        'submit': 'LOGIN'
    }
    response = session.post(cas_server_url, data=payload)
    return 'PHPSESSID' in session.cookies.get_dict() and 'TGC' in session.cookies.get_dict()

def get_data(username, password, domain, cas_domain):
    """Récupère les données de notes de l'utilisateur après authentification CAS."""
    cas_server_url = f'https://{cas_domain}/login?service=https%3A%2F%2F{domain}%2Fservices%2FdoAuth.php%3Fhref%3Dhttps%253A%252F%252F{domain}%252F'
    session = requests.Session()

    try:
        csrf_token = get_csrf_token(session, cas_server_url)
        if authenticate(session, cas_server_url, username, password, csrf_token):
            print('Authentification au serveur CAS réussie ✅\n')
            print("Cookies de la session CAS :\n")
            print("PHPSESSID :", session.cookies.get('PHPSESSID'),"\n")
            print("TGC :", session.cookies.get('TGC'),"\n")
        else:
            print('Authentication failed ❌\n',"\n")
            return None

        print("RÉCUPÉRATION DES NOTES")
        url = f'https://{domain}/services/data.php?q=dataPremièreConnexion'
        response = session.get(url)
        response.raise_for_status()  # Vérifie si la requête a réussi
        print("\n")
        print("Données récupérées avec succès ✅\n")
        data = response.json()
        return data

    except requests.RequestException as e:
        print(f'Une erreur s\'est produite : {e} ❌ \n')
        return None

def save_data_to_db(data):
    """Enregistre les données dans la table _notes de la base de données MySQL."""
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = connection.cursor()

        add_note = ("INSERT INTO _notes (data) VALUES (%s)")
        data_json = json.dumps(data)
        cursor.execute(add_note, (data_json,))

        connection.commit()
        cursor.close()
        connection.close()
        print("Données enregistrées dans la base de données avec succès ✅\n")
    except mysql.connector.Error as err:
        print(f'Erreur lors de la connexion à la base de données : {err} ❌\n')

def job():
    res = get_data(username, password, domain, cas_domain)
    if res:
        #print(res)
        save_data_to_db(res)
        print("Sauvegarde des données dans la base de données.\n")
    else:
        print("Impossible de récupérer les données.\n")

# Planifier la tâche pour qu'elle s'exécute toutes les heures
schedule.every().hour.do(job)

# Boucle infinie pour exécuter les tâches planifiées
while True:
    schedule.run_pending()
    time.sleep(1)