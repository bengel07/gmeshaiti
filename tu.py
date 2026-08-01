import requests

BASE_URL = "http://127.0.0.1:5000"
# BASE_URL = "https://gmeshaiti-aeo3.onrender.com"

EMAIL_CLIENT = "contactbegingeler@gmail.com"
MOT_DE_PASSE = "Admin123$"
CLIENT_ID = 15

session = requests.Session()

# ----------------------------
# Connexion
# ----------------------------

login_data = {
    "email": EMAIL_CLIENT,
    "password": MOT_DE_PASSE
}

r = session.post(
    f"{BASE_URL}/login",
    data=login_data,
    allow_redirects=True
)

print("Connexion :", r.status_code)

# ----------------------------
# Demande de prêt
# ----------------------------

payload = {
    "client_id": CLIENT_ID,

    "nom": "Jean",
    "prenom": "Pierre",
    "sexe": "M",
    "date_naissance": "1990-05-12",
    "lieu_naissance": "Jacmel",
    "nationalite": "Haïtienne",
    "cin_nif": "1234567890",

    "telephone": "34567890",
    "email": EMAIL_CLIENT,

    "adresse": "Jacmel",
    "commune": "Jacmel",
    "departement": "Sud-Est",
    "duree_adresse": "5",

    "etat_civil": "celibataire",
    "nb_enfants": "0",

    "profession": "Commerçant",
    "entreprise": "GMES",
    "adresse_travail": "Jacmel",
    "revenu_mensuel": "80000",

    "montant_demande": "250000",
    "duree": "24",
    "taux_interet": "12",

    "objet": "Commerce",

    "type_pret": "commerce",

    "date_demande": "2026-08-01",

    "signature": "TEST_SIGNATURE"
}

r = session.post(
    f"{BASE_URL}/prets/demande-pret",
    data=payload,
    allow_redirects=True
)

print("Status :", r.status_code)
print("----------------------------------")
print(r.text[:5000])