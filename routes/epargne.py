"""Blueprint Épargne : produits d'épargne GMES + opérations sur les comptes + rapports.

Fonctionne avec votre modèle `ProduitEpargne` tel quel (aucune modification requise).

Produits (super admin)
    GET     /epargne/produits                      page de configuration
    GET     /epargne/api/produits                  liste (JSON)
    POST    /epargne/api/produits                  création (multipart/form-data)
    GET     /epargne/api/produits/<id>             détail
    PUT     /epargne/api/produits/<id>             mise à jour
    DELETE  /epargne/api/produits/<id>             suppression (refusée si des comptes l'utilisent)

Comptes (employés ; clôture : super admin / direction)
    GET     /epargne/comptes/<id>                  page : conditions, opérations, relevé
    POST    /epargne/api/comptes/<id>/activation   dépôt initial + frais d'ouverture
    POST    /epargne/api/comptes/<id>/depot
    POST    /epargne/api/comptes/<id>/retrait
    POST    /epargne/api/comptes/<id>/cloture      frais de clôture, solde versé
    GET     /epargne/api/comptes/<id>/transactions relevé (JSON)

Rapports (super admin)
    GET     /epargne/rapport                       comptes de GMES, totaux par type d'opération
    GET     /epargne/api/rapport                   idem (JSON)

Commandes
    flask epargne init-comptable                   crée les comptes internes GMES (une seule fois)
    flask epargne cloture-mensuelle [--periode AAAA-MM]   intérêts + frais mensuels (cron le 1er du mois)
    flask epargne verifier-equilibre               contrôle d'intégrité du grand livre
    flask epargne seed                             insère des produits de démonstration

Enregistrement dans votre application :
    from routes.epargne import epargne_bp
    app.register_blueprint(epargne_bp)
"""
import json
import math
import os
import re
import uuid
from datetime import date
from functools import wraps

import click
from flask import Blueprint, abort, current_app, jsonify, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from database import db  # <- adaptez : votre instance Flask-SQLAlchemy
from models import Epargne, ProduitEpargne  # <- adaptez : là où vos modèles sont importés
from services import comptabilite as compta
from services import epargne_ops as ops

epargne_bp = Blueprint("epargne", __name__, url_prefix="/epargne")

# Rôles autorisés à configurer les produits (rôles de votre application : 'employe',
# 'super_admin', 'direction'). Ajoutez "direction" si elle doit aussi pouvoir le faire.
ROLES_AUTORISES = {"super_admin"}
# Rôles autorisés à activer un compte, déposer et retirer ; la clôture est plus restreinte.
ROLES_OPERATIONS = {"employe", "super_admin", "direction"}
ROLES_CLOTURE = {"super_admin", "direction"}

# (valeur stockée en base, libellé affiché) : reprend la liste de votre modèle
TYPES_PRODUIT = [
    ("classique", "Classique"),
    ("jeune", "Jeune"),
    ("senior", "Senior"),
    ("entreprise", "Entreprise"),
    ("termine", "À terme"),
]
VALEURS_TYPES = {v for v, _ in TYPES_PRODUIT}

EXTENSIONS_OK = {"pdf", "jpg", "jpeg", "png"}
TAILLE_MAX_FICHIER = 5 * 1024 * 1024  # 5 Mo
CODE_RE = re.compile(r"^[A-Z0-9][A-Z0-9_-]{2,19}$")  # String(20) en base
MAX_MONTANT = 1e15


# --------------------------------------------------------------------------- #
# Sécurité
# --------------------------------------------------------------------------- #
def _roles_requis(roles):
    def decorateur(vue):
        @wraps(vue)
        def wrapper(*args, **kwargs):
            if getattr(current_user, "role", None) not in roles:
                abort(403)
            return vue(*args, **kwargs)

        return login_required(wrapper)
    return decorateur


def admin_required(vue):
    return _roles_requis(ROLES_AUTORISES)(vue)


def operations_required(vue):
    return _roles_requis(ROLES_OPERATIONS)(vue)


@epargne_bp.errorhandler(403)
def _interdit(_e):
    if request.path.startswith("/epargne/api/"):
        return jsonify(erreur="Accès refusé."), 403
    return "Accès refusé.", 403


# --------------------------------------------------------------------------- #
# Sérialisation
# --------------------------------------------------------------------------- #
def serialiser(p):
    return {
        "id": p.id,
        "code": p.code,
        "nom": p.nom,
        "description": p.description or "",
        "type_produit": p.type_produit,
        "statut": "Actif" if p.est_actif else "Inactif",
        "est_actif": bool(p.est_actif),
        "taux_interet_annuel": p.taux_interet_annuel,
        "taux_interet_mensuel": p.taux_interet_mensuel,
        "depot_initial_min": p.depot_initial_min,
        "depot_initial_max": p.depot_initial_max,
        "solde_min": p.solde_min,
        "solde_max": p.solde_max,
        "frais_ouverture": p.frais_ouverture,
        "frais_tenue_compte_mensuel": p.frais_tenue_compte_mensuel,
        "frais_cloture": p.frais_cloture,
        "plafond_depot_mensuel": p.plafond_depot_mensuel,
        "plafond_retrait_mensuel": p.plafond_retrait_mensuel,
        "duree_blocage_mois": p.duree_blocage_mois,
        "penalite_retrait_anticipe": p.penalite_retrait_anticipe,
        "age_min": p.age_min,
        "age_max": p.age_max,
        "date_lancement": p.date_lancement.isoformat() if p.date_lancement else "",
    }


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #
def _nombre(form, cle, erreurs, *, obligatoire=False, defaut=0.0, maximum=MAX_MONTANT, decimales=2):
    brut = (form.get(cle) or "").strip().replace(" ", "").replace(",", ".")
    if brut == "":
        if obligatoire:
            erreurs[cle] = "Champ obligatoire."
        return defaut
    try:
        valeur = float(brut)
    except ValueError:
        erreurs[cle] = "Nombre invalide."
        return defaut
    if not math.isfinite(valeur) or valeur < 0:
        erreurs[cle] = "Doit être un nombre positif."
    elif valeur > maximum:
        erreurs[cle] = f"Ne peut pas dépasser {maximum:g}."
    return round(valeur, decimales)


def _entier(form, cle, erreurs, *, defaut, minimum=0, maximum=1000):
    brut = (form.get(cle) or "").strip()
    if brut == "":
        return defaut
    try:
        valeur = int(brut)
    except ValueError:
        erreurs[cle] = "Nombre entier requis."
        return defaut
    if not minimum <= valeur <= maximum:
        erreurs[cle] = f"Doit être compris entre {minimum} et {maximum}."
    return valeur


def valider(form, produit_id=None):
    """Retourne (valeurs_pour_le_modèle, erreurs) à partir d'un formulaire multipart."""
    e = {}
    v = {}

    v["code"] = (form.get("code") or "").strip().upper()
    if not CODE_RE.match(v["code"]):
        e["code"] = "Code requis (3 à 20 caractères : A-Z, 0-9, - et _)."

    v["nom"] = (form.get("nom") or "").strip()
    if not v["nom"]:
        e["nom"] = "Champ obligatoire."
    elif len(v["nom"]) > 100:
        e["nom"] = "100 caractères maximum."

    v["type_produit"] = (form.get("type_produit") or "").strip()
    if v["type_produit"] not in VALEURS_TYPES:
        e["type_produit"] = "Type invalide."

    statut = (form.get("statut") or "").strip()
    if statut not in ("Actif", "Inactif"):
        e["statut"] = "Statut invalide."
    v["est_actif"] = statut == "Actif"

    v["description"] = (form.get("description") or "").strip()
    if len(v["description"]) > 500:
        e["description"] = "500 caractères maximum."

    v["taux_interet_annuel"] = _nombre(form, "taux_interet_annuel", e, obligatoire=True, maximum=100, decimales=4)
    if (form.get("taux_interet_mensuel") or "").strip():
        v["taux_interet_mensuel"] = _nombre(form, "taux_interet_mensuel", e, maximum=100, decimales=4)
    else:  # calculé automatiquement
        v["taux_interet_mensuel"] = round(v["taux_interet_annuel"] / 12, 4)

    v["depot_initial_min"] = _nombre(form, "depot_initial_min", e, obligatoire=True)
    v["depot_initial_max"] = _nombre(form, "depot_initial_max", e, obligatoire=True)
    v["solde_min"] = _nombre(form, "solde_min", e)
    v["solde_max"] = _nombre(form, "solde_max", e)
    v["frais_ouverture"] = _nombre(form, "frais_ouverture", e, obligatoire=True)
    v["frais_tenue_compte_mensuel"] = _nombre(form, "frais_tenue_compte_mensuel", e, obligatoire=True)
    v["frais_cloture"] = _nombre(form, "frais_cloture", e)
    v["plafond_depot_mensuel"] = _nombre(form, "plafond_depot_mensuel", e)
    v["plafond_retrait_mensuel"] = _nombre(form, "plafond_retrait_mensuel", e)
    v["penalite_retrait_anticipe"] = _nombre(form, "penalite_retrait_anticipe", e, maximum=100)  # en %
    v["duree_blocage_mois"] = _entier(form, "duree_blocage_mois", e, defaut=0, maximum=600)
    v["age_min"] = _entier(form, "age_min", e, defaut=18, maximum=120)
    v["age_max"] = _entier(form, "age_max", e, defaut=120, maximum=120)

    brut_date = (form.get("date_lancement") or "").strip()
    v["date_lancement"] = None
    if not brut_date:
        e["date_lancement"] = "Champ obligatoire."
    else:
        try:
            v["date_lancement"] = date.fromisoformat(brut_date)
        except ValueError:
            e["date_lancement"] = "Date invalide."

    # Cohérence entre champs (seulement si les champs eux-mêmes sont valides)
    if "depot_initial_min" not in e and "depot_initial_max" not in e \
            and v["depot_initial_min"] > v["depot_initial_max"]:
        e["depot_initial_min"] = "Le dépôt initial minimum dépasse le maximum."
    if "solde_min" not in e and "solde_max" not in e and v["solde_min"] > v["solde_max"]:
        e["solde_min"] = "Le solde minimum dépasse le maximum."
    if "depot_initial_max" not in e and "solde_max" not in e \
            and v["solde_max"] > 0 and v["depot_initial_max"] > v["solde_max"]:
        e["depot_initial_max"] = "Le dépôt initial maximum dépasse le solde maximum."
    if "age_min" not in e and "age_max" not in e and v["age_min"] > v["age_max"]:
        e["age_min"] = "L'âge minimum dépasse l'âge maximum."

    # Unicité du code
    if "code" not in e:
        autre = ProduitEpargne.query.filter(ProduitEpargne.code == v["code"])
        if produit_id:
            autre = autre.filter(ProduitEpargne.id != produit_id)
        if autre.first():
            e["code"] = "Ce code de produit existe déjà."

    return v, e


def _reponse_erreurs(erreurs):
    doublon = erreurs.keys() == {"code"} and "existe" in erreurs["code"]
    return jsonify(erreur=" ".join(erreurs.values()), erreurs=erreurs), (409 if doublon else 400)


def _sauver_fichier(fichier):
    """Enregistre la pièce jointe, retourne le chemin relatif (ou lève ValueError)."""
    nom = secure_filename(fichier.filename or "")
    extension = nom.rsplit(".", 1)[-1].lower() if "." in nom else ""
    if extension not in EXTENSIONS_OK:
        raise ValueError("Pièce jointe : formats acceptés PDF, JPG, PNG.")
    fichier.stream.seek(0, os.SEEK_END)
    taille = fichier.stream.tell()
    fichier.stream.seek(0)
    if taille > TAILLE_MAX_FICHIER:
        raise ValueError("Pièce jointe : 5 Mo maximum.")
    dossier = os.path.join(
        current_app.config.get("UPLOAD_FOLDER", os.path.join(current_app.instance_path, "uploads")),
        "produits_epargne",
    )
    os.makedirs(dossier, exist_ok=True)
    nom_final = f"{uuid.uuid4().hex}.{extension}"
    fichier.save(os.path.join(dossier, nom_final))
    return f"produits_epargne/{nom_final}"


def _enregistrer(produit, valeurs):
    """Applique les valeurs, commit. Retourne (produit, réponse_erreur | None)."""
    # La pièce jointe est validée et enregistrée sur disque, mais votre modèle n'a pas de
    # colonne pour la stocker : ajoutez `piece_jointe = db.Column(db.String(255))` pour la conserver.
    fichier = request.files.get("piece_jointe")
    if fichier and fichier.filename:
        try:
            chemin = _sauver_fichier(fichier)
        except ValueError as exc:
            return None, _reponse_erreurs({"piece_jointe": str(exc)})
        if hasattr(ProduitEpargne, "piece_jointe"):
            valeurs["piece_jointe"] = chemin
    for cle, valeur in valeurs.items():
        setattr(produit, cle, valeur)
    if produit.id is None:
        db.session.add(produit)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None, _reponse_erreurs({"code": "Ce code de produit existe déjà."})
    return produit, None


def _nb_comptes(produit):
    """Nombre de comptes d'épargne rattachés à ce produit."""
    return db.session.execute(
        db.select(func.count()).select_from(Epargne).where(Epargne.produit_epargne_id == produit.id)).scalar()


# --------------------------------------------------------------------------- #
# Page
# --------------------------------------------------------------------------- #
@epargne_bp.get("/produits")
@admin_required
def page_produits():
    return render_template("epargne/produits.html", types=TYPES_PRODUIT)


# --------------------------------------------------------------------------- #
# API JSON
# --------------------------------------------------------------------------- #
@epargne_bp.get("/api/produits")
@admin_required
def api_liste():
    produits = ProduitEpargne.query.order_by(ProduitEpargne.id).all()
    return jsonify([serialiser(p) for p in produits])


@epargne_bp.get("/api/produits/<int:produit_id>")
@admin_required
def api_detail(produit_id):
    return jsonify(serialiser(db.get_or_404(ProduitEpargne, produit_id)))


@epargne_bp.post("/api/produits")
@admin_required
def api_creer():
    valeurs, erreurs = valider(request.form)
    if erreurs:
        return _reponse_erreurs(erreurs)
    produit, echec = _enregistrer(ProduitEpargne(), valeurs)
    return echec or (jsonify(serialiser(produit)), 201)


@epargne_bp.put("/api/produits/<int:produit_id>")
@admin_required
def api_modifier(produit_id):
    produit = db.get_or_404(ProduitEpargne, produit_id)
    valeurs, erreurs = valider(request.form, produit_id=produit_id)
    if erreurs:
        return _reponse_erreurs(erreurs)
    produit, echec = _enregistrer(produit, valeurs)
    return echec or jsonify(serialiser(produit))


@epargne_bp.delete("/api/produits/<int:produit_id>")
@admin_required
def api_supprimer(produit_id):
    produit = db.get_or_404(ProduitEpargne, produit_id)
    if _nb_comptes(produit) > 0:
        return jsonify(erreur="Des comptes utilisent ce produit : désactivez-le plutôt que de le supprimer."), 409
    db.session.delete(produit)
    db.session.commit()
    return "", 204


# --------------------------------------------------------------------------- #
# Comptes : page, opérations, relevé
# --------------------------------------------------------------------------- #
def _transaction_json(t):
    return {"id": t.id, "date": t.created_at.isoformat(timespec="seconds"), "type": t.type, "sens": t.sens,
            "montant": str(t.montant), "solde_apres": None if t.solde_apres is None else str(t.solde_apres),
            "libelle": t.libelle, "periode": t.periode}


@epargne_bp.get("/comptes/<int:compte_id>")
@operations_required
def page_compte(compte_id):
    compte = db.get_or_404(Epargne, compte_id)
    return render_template(
        "epargne/compte.html", compte=compte,
        produit=db.session.get(ProduitEpargne, compte.produit_epargne_id),
        transactions=ops.releve(compte_id),
        actif=compte.statut == ops.STATUT_ACTIF,
        cloture=compte.statut == ops.STATUT_CLOTURE,
        deja_active=ops.est_active(compte_id),
        peut_cloturer=getattr(current_user, "role", None) in ROLES_CLOTURE)


@epargne_bp.get("/api/comptes/<int:compte_id>/transactions")
@operations_required
def api_releve(compte_id):
    db.get_or_404(Epargne, compte_id)
    return jsonify([_transaction_json(t) for t in ops.releve(compte_id, limite=request.args.get("limite", 200, type=int))])


@epargne_bp.post("/api/comptes/<int:compte_id>/<operation>")
@operations_required
def api_operation(compte_id, operation):
    """Corps JSON ou formulaire : montant, cle (clé d'idempotence : évite le double envoi)."""
    if operation not in ("activation", "depot", "retrait", "cloture"):
        abort(404)
    if operation == "cloture" and getattr(current_user, "role", None) not in ROLES_CLOTURE:
        return jsonify(erreur="La clôture est réservée à la direction."), 403
    donnees = request.get_json(silent=True) or request.form
    utilisateur, cle = getattr(current_user, "id", None), donnees.get("cle")
    try:
        if operation == "activation":
            res = ops.activer_compte(compte_id, donnees.get("montant"), utilisateur)
        elif operation == "depot":
            res = ops.deposer(compte_id, donnees.get("montant"), utilisateur, cle)
        elif operation == "retrait":
            res = ops.retirer(compte_id, donnees.get("montant"), utilisateur, cle)
        else:
            res = ops.cloturer_compte(compte_id, utilisateur)
    except compta.ErreurMetier as exc:
        return jsonify(erreur=str(exc)), 400
    return jsonify(solde=str(res["solde"]), deja_traite=res.get("deja_traite", False))


# --------------------------------------------------------------------------- #
# Rapports (super admin)
# --------------------------------------------------------------------------- #
def _periode_demandee():
    periode = request.args.get("periode") or date.today().strftime("%Y-%m")
    compta.bornes_periode(periode)  # valide le format
    return periode


@epargne_bp.get("/rapport")
@admin_required
def page_rapport():
    try:
        periode = _periode_demandee()
    except compta.ErreurMetier:
        abort(400)
    return render_template(
        "epargne/rapport.html", periode=periode, comptes=ops.comptes_internes(),
        totaux_periode=ops.totaux_par_type(periode), totaux_global=ops.totaux_par_type(),
        controle=ops.verifier_equilibre() if request.args.get("controle") else None)


@epargne_bp.get("/api/rapport")
@admin_required
def api_rapport():
    try:
        periode = _periode_demandee()
    except compta.ErreurMetier as exc:
        return jsonify(erreur=str(exc)), 400
    return jsonify(
        periode=periode,
        comptes_internes=[{"code": ci.code, "libelle": ci.libelle, "nature": ci.nature, "solde": str(ci.solde)}
                          for ci in ops.comptes_internes()],
        totaux_periode=[{**t, "total": str(t["total"])} for t in ops.totaux_par_type(periode)])


# --------------------------------------------------------------------------- #
# Commandes : flask epargne ...
# --------------------------------------------------------------------------- #
@epargne_bp.cli.command("init-comptable")
def cli_init_comptable():
    """Crée les comptes internes de GMES (caisse, frais, intérêts). À lancer une seule fois."""
    crees = ops.initialiser_comptes_internes()
    print("Comptes créés : " + ", ".join(crees) if crees else "Les comptes internes existent déjà.")


@epargne_bp.cli.command("cloture-mensuelle")
@click.option("--periode", default=None, help="Mois à traiter, AAAA-MM (défaut : le mois précédent).")
def cli_cloture_mensuelle(periode):
    """Verse les intérêts et prélève les frais mensuels de tous les comptes actifs.
    Sans risque à relancer : un compte n'est traité qu'une fois par période."""
    if not periode:
        periode = compta.ajouter_mois(date.today().replace(day=1), -1).strftime("%Y-%m")
    print(json.dumps(ops.cloture_mensuelle(periode), indent=2, ensure_ascii=False, default=str))


@epargne_bp.cli.command("verifier-equilibre")
def cli_verifier_equilibre():
    """Contrôle que chaque opération est équilibrée et que les soldes correspondent au grand livre."""
    print(json.dumps(ops.verifier_equilibre(), indent=2, ensure_ascii=False, default=str))


@epargne_bp.cli.command("seed")
def seed():
    """Insère les produits d'exemple s'ils n'existent pas encore."""
    exemples = [
        ("EPARGNE-CLASSIQUE", "Épargne classique GMES", "classique", True, 0),
        ("EPARGNE-JEUNE", "Épargne Jeune", "jeune", True, 2),
        ("EPARGNE-SENIOR", "Épargne Senior", "senior", True, 4),
        ("EPARGNE-TERME", "Épargne à terme", "termine", False, 3),
    ]
    ajoutes = 0
    for code, nom, type_produit, actif, taux in exemples:
        if ProduitEpargne.query.filter_by(code=code).first():
            continue
        db.session.add(ProduitEpargne(
            code=code, nom=nom, type_produit=type_produit, est_actif=actif,
            taux_interet_annuel=taux, taux_interet_mensuel=round(taux / 12, 4),
            date_lancement=date(2025, 10, 16),
        ))
        ajoutes += 1
    db.session.commit()
    print(f"{ajoutes} produit(s) ajouté(s).")
