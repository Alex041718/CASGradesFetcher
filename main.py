import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Informations d'authentification et de plateforme
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
domain = os.getenv('DOMAIN')
cas_domain = os.getenv('CAS_DOMAIN')

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

# Appel de la fonction
res = get_data(username, password, domain, cas_domain)
if res:
    print(res)
else:
    print("Impossible de récupérer les données.\n")
