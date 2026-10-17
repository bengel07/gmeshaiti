"""
Applique deux corrections a app.py (version locale) :
  1. parse_date accepte JJ/MM/AAAA et AAAA-MM-JJ
  2. detail_investisseur_json renvoie 'interet' pour chaque investissement

Sans danger si on le relance : une correction deja presente est ignoree.
A lancer dans le dossier du projet :  python appliquer_correctifs.py
"""
import re
import sys

FICHIER = "app.py"

with open(FICHIER, "r", encoding="utf-8", newline="") as f:
    texte = f.read()

nl = "\r\n" if "\r\n" in texte else "\n"      # conserve le style de fins de ligne du fichier
resultats = []

# ---------- 1. parse_date ----------
if '("%d/%m/%Y", "%Y-%m-%d")' in texte:
    resultats.append("parse_date : deja corrige")
else:
    ancien = re.compile(
        r"def parse_date\(valeur\):\r?\n"
        r"    try:\r?\n"
        r"        return datetime\.strptime\(valeur, '%Y-%m-%d'\)\.date\(\)\r?\n"
        r"    except \(TypeError, ValueError\):\r?\n"
        r"        return None"
    )
    nouveau = nl.join([
        "def parse_date(valeur):",
        '    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):',
        "        try:",
        '            return datetime.strptime((valeur or "").strip(), fmt).date()',
        "        except ValueError:",
        "            continue",
        "    return None",
    ])
    texte, n = ancien.subn(lambda _m: nouveau, texte, count=1)
    resultats.append("parse_date : corrige" if n else "parse_date : ERREUR, bloc introuvable")

# ---------- 2. 'interet' dans detail_investisseur_json ----------
if "'interet': i.interet_total" in texte:
    resultats.append("interet : deja present")
else:
    cible = "'taux': float(i.taux_annuel), 'echeance'"
    if texte.count(cible) == 1:
        texte = texte.replace(cible, "'taux': float(i.taux_annuel), 'interet': i.interet_total, 'echeance'")
        resultats.append("interet : ajoute")
    else:
        resultats.append("interet : ERREUR, ligne introuvable ou en plusieurs exemplaires")

with open(FICHIER, "w", encoding="utf-8", newline="") as f:
    f.write(texte)

print("\n".join(resultats))
sys.exit(1 if any("ERREUR" in r for r in resultats) else 0)