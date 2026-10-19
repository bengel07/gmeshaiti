"""Opérations d'épargne sur la base de données (SQLAlchemy). Les RÈGLES sont dans comptabilite.py ;
ce module ne fait que : verrouiller le compte, appliquer les écritures, enregistrer, valider.

Garanties :
- une opération = une transaction SQL : tout est enregistré ou rien (commit/rollback) ;
- le compte client est verrouillé (SELECT ... FOR UPDATE) pendant l'opération ;
- les soldes des comptes internes sont mis à jour par des UPDATE atomiques ;
- les opérations avec `reference` sont idempotentes (rejouer ne double jamais l'écriture).
"""
import logging
import uuid
from datetime import date, datetime
from decimal import Decimal
from functools import wraps

from sqlalchemy import case, func
from sqlalchemy.exc import IntegrityError

from database import db # <- adaptez
from models import Epargne, ProduitEpargne  # <- adaptez si vos modèles sont ailleurs
from models import CompteInterne, TransactionEpargne
from services import comptabilite as c

log = logging.getLogger(__name__)

# Valeurs de la colonne Epargne.statut  <- adaptez à vos statuts réels
STATUT_ACTIF = "actif"
STATUT_CLOTURE = "cloture"
# Statuts dans lesquels l'activation (dépôt initial) est permise. None = tous sauf clôturé.
# Exemple si vous voulez exiger la signature des conditions : {"approuve", "en_attente_depot"}
STATUTS_ACTIVABLES = None


# --------------------------------------------------------------------------- #
# Utilitaires
# --------------------------------------------------------------------------- #
def atomique(fonction):
    """Valide la transaction si tout va bien, l'annule à la moindre exception."""
    @wraps(fonction)
    def wrapper(*args, **kwargs):
        try:
            resultat = fonction(*args, **kwargs)
            db.session.commit()
            return resultat
        except Exception:
            db.session.rollback()
            raise
    return wrapper


def initialiser_comptes_internes():
    """Crée les comptes internes GMES manquants. Idempotent. Retourne la liste des codes créés."""
    existants = set(db.session.execute(db.select(CompteInterne.code)).scalars())
    crees = []
    for code, (libelle, nature) in c.COMPTES_INTERNES.items():
        if code not in existants:
            db.session.add(CompteInterne(code=code, libelle=libelle, nature=nature, solde=0))
            crees.append(code)
    db.session.commit()
    return crees


def _ids_internes():
    ids = dict(db.session.execute(db.select(CompteInterne.code, CompteInterne.id)).all())
    manquants = set(c.COMPTES_INTERNES) - set(ids)
    if manquants:
        raise c.ErreurMetier("Comptes internes GMES absents : lancez « flask epargne init-comptable ».")
    return ids


def _verrouiller(compte_id):
    compte = db.session.execute(
        db.select(Epargne).where(Epargne.id == compte_id).with_for_update()).scalar_one_or_none()
    if compte is None:
        raise c.ErreurMetier("Compte introuvable.")
    return compte


def _produit(compte):
    produit = db.session.get(ProduitEpargne, compte.produit_epargne_id)
    if produit is None:
        raise c.ErreurMetier("Produit d'épargne introuvable pour ce compte.")
    return produit


def _conditions(compte):
    return c.Conditions.depuis_produit(_produit(compte))


def _exiger_actif(compte):
    if compte.statut != STATUT_ACTIF:
        raise c.ErreurMetier(f"Le compte n'est pas actif (statut : {compte.statut}).")


def _solde(compte):
    return c.D(compte.solde)


def _poser_solde(compte, valeur):
    """Écrit le solde en conservant le type de colonne existant (Decimal ou Float)."""
    for champ in ("solde", "solde_disponible"):
        if hasattr(compte, champ):
            actuel = getattr(compte, champ)
            setattr(compte, champ, valeur if isinstance(actuel, Decimal) else float(valeur))


def _somme_mois(compte_id, types, jour):
    debut, fin = c.bornes_periode(f"{jour.year:04d}-{jour.month:02d}")
    q = db.select(func.coalesce(func.sum(TransactionEpargne.montant), 0)).where(
        TransactionEpargne.compte_id == compte_id,
        TransactionEpargne.type.in_(types),
        TransactionEpargne.created_at >= datetime.combine(debut, datetime.min.time()),
        TransactionEpargne.created_at < datetime.combine(fin, datetime.min.time()))
    return c.D(db.session.execute(q).scalar())


def _date_ouverture(compte):
    """Date d'ouverture : 1er dépôt initial du grand livre, sinon un champ date de l'Epargne."""
    q = db.select(func.min(TransactionEpargne.created_at)).where(
        TransactionEpargne.compte_id == compte.id, TransactionEpargne.type == "depot_initial")
    premiere = db.session.execute(q).scalar()
    if premiere:
        return premiere.date() if hasattr(premiere, "date") else premiere
    for champ in ("created_at", "date_creation", "date_ouverture"):
        valeur = getattr(compte, champ, None)
        if valeur:
            return valeur.date() if isinstance(valeur, datetime) else valeur
    return None


def _fin_blocage(compte, cond):
    return c.fin_blocage(_date_ouverture(compte), cond.duree_blocage_mois)


def _deja_enregistre(reference):
    return db.session.execute(
        db.select(TransactionEpargne.id).where(TransactionEpargne.reference == reference)).first() is not None


def est_active(compte_id):
    """Le dépôt initial de ce compte a-t-il déjà été encaissé ?"""
    return _deja_enregistre(f"OUV-{compte_id}")


def _ecrire(compte, plan, *, reference=None, periode=None, created_by=None, libelle=None):
    """Enregistre les écritures du plan et met à jour les soldes. Retourne le groupe_id,
    ou None si `reference` existe déjà (opération déjà faite)."""
    if reference and _deja_enregistre(reference):
        return None
    ids = _ids_internes()
    groupe = uuid.uuid4().hex
    courant = _solde(compte)
    premiere_jambe_client = True
    for e in plan.ecritures:
        commun = dict(groupe_id=groupe, type=e.type, sens=e.sens, montant=e.montant,
                      periode=periode, libelle=libelle or e.type.replace("_", " "), created_by=created_by)
        if e.compte == c.CLIENT:
            courant += e.montant if e.sens == "credit" else -e.montant
            db.session.add(TransactionEpargne(
                compte_id=compte.id, solde_apres=courant,
                reference=reference if premiere_jambe_client else None, **commun))
            premiere_jambe_client = False
        else:
            nature = c.COMPTES_INTERNES[e.compte][1]
            delta = c.variation_interne(nature, e.sens, e.montant)
            db.session.execute(db.update(CompteInterne).where(CompteInterne.id == ids[e.compte])
                               .values(solde=CompteInterne.solde + delta))
            db.session.add(TransactionEpargne(compte_interne_id=ids[e.compte], **commun))
    if courant != plan.solde_apres:  # garde-fou : ne devrait jamais arriver
        raise c.ErreurMetier("Incohérence de solde détectée : opération annulée.")
    _poser_solde(compte, courant)
    db.session.flush()
    return groupe


def _reference(prefixe, cle):
    if not cle:
        return None
    cle = "".join(ch for ch in str(cle) if ch.isalnum() or ch in "-_")[:60]
    return f"{prefixe}-{cle}" if cle else None


# --------------------------------------------------------------------------- #
# Opérations unitaires
# --------------------------------------------------------------------------- #
@atomique
def activer_compte(compte_id, depot_initial, created_by=None):
    """Active le compte : encaisse le dépôt initial et prélève les frais d'ouverture."""
    compte = _verrouiller(compte_id)
    if compte.statut == STATUT_CLOTURE:
        raise c.ErreurMetier("Ce compte est clôturé.")
    if STATUTS_ACTIVABLES is not None and compte.statut not in STATUTS_ACTIVABLES:
        raise c.ErreurMetier(f"Activation impossible dans le statut « {compte.statut} ».")
    if _deja_enregistre(f"OUV-{compte.id}"):
        raise c.ErreurMetier("Ce compte a déjà été activé.")
    plan = c.plan_activation(_conditions(compte), depot_initial, _solde(compte))
    _ecrire(compte, plan, reference=f"OUV-{compte.id}", created_by=created_by, libelle="Ouverture du compte")
    compte.statut = STATUT_ACTIF
    return {"solde": plan.solde_apres}


@atomique
def deposer(compte_id, montant, created_by=None, cle=None):
    compte = _verrouiller(compte_id)
    _exiger_actif(compte)
    cond = _conditions(compte)
    deja = _somme_mois(compte.id, ("depot", "depot_initial"), date.today())
    plan = c.plan_depot(cond, _solde(compte), montant, deja)
    groupe = _ecrire(compte, plan, reference=_reference("DEP", cle), created_by=created_by, libelle="Dépôt")
    return {"solde": plan.solde_apres, "deja_traite": groupe is None}


@atomique
def retirer(compte_id, montant, created_by=None, cle=None):
    compte = _verrouiller(compte_id)
    _exiger_actif(compte)
    cond = _conditions(compte)
    deja = _somme_mois(compte.id, ("retrait",), date.today())
    plan = c.plan_retrait(cond, _solde(compte), montant, deja, _fin_blocage(compte, cond))
    groupe = _ecrire(compte, plan, reference=_reference("RET", cle), created_by=created_by, libelle="Retrait")
    return {"solde": plan.solde_apres, "deja_traite": groupe is None}


@atomique
def cloturer_compte(compte_id, created_by=None):
    compte = _verrouiller(compte_id)
    _exiger_actif(compte)
    cond = _conditions(compte)
    plan = c.plan_cloture(cond, _solde(compte), _fin_blocage(compte, cond))
    _ecrire(compte, plan, reference=f"CLO-{compte.id}", created_by=created_by, libelle="Clôture du compte")
    compte.statut = STATUT_CLOTURE
    return {"solde": plan.solde_apres}


# --------------------------------------------------------------------------- #
# Traitement mensuel : intérêts puis frais de tenue de compte
# --------------------------------------------------------------------------- #
@atomique
def _traiter_compte_mensuel(compte_id, periode, debut_periode, created_by):
    compte = _verrouiller(compte_id)
    resultat = {"interets": c.ZERO, "frais": c.ZERO, "frais_impayes": False, "ignore": None}
    if compte.statut != STATUT_ACTIF:
        resultat["ignore"] = "compte non actif"
        return resultat
    ouverture = _date_ouverture(compte)
    if ouverture is not None and ouverture >= debut_periode:
        resultat["ignore"] = "ouvert pendant la période"  # pas d'intérêts ni de frais le mois d'ouverture
        return resultat
    cond = _conditions(compte)

    plan = c.plan_interets(cond, _solde(compte))
    if plan and _ecrire(compte, plan, reference=f"INT-{compte.id}-{periode}", periode=periode,
                        created_by=created_by, libelle=f"Intérêts {periode}"):
        resultat["interets"] = sum((e.montant for e in plan.ecritures if e.compte == c.CLIENT), c.ZERO)

    try:
        plan = c.plan_frais_mensuel(cond, _solde(compte))
    except c.ErreurMetier:
        resultat["frais_impayes"] = True  # solde insuffisant : à traiter par un humain
        return resultat
    if plan and _ecrire(compte, plan, reference=f"FRM-{compte.id}-{periode}", periode=periode,
                        created_by=created_by, libelle=f"Frais de tenue de compte {periode}"):
        resultat["frais"] = cond.frais_mensuel
    return resultat


def cloture_mensuelle(periode, created_by=None):
    """Verse les intérêts et prélève les frais mensuels de TOUS les comptes actifs pour `periode`
    ('AAAA-MM'). Peut être relancé sans risque : chaque compte n'est traité qu'une fois par période."""
    debut, _ = c.bornes_periode(periode)
    ids = list(db.session.execute(
        db.select(Epargne.id).where(Epargne.statut == STATUT_ACTIF).order_by(Epargne.id)).scalars())
    rapport = {"periode": periode, "comptes": len(ids), "interets_verses": 0, "total_interets": c.ZERO,
               "frais_preleves": 0, "total_frais": c.ZERO, "frais_impayes": [], "ignores": 0, "erreurs": []}
    for cid in ids:
        try:
            r = _traiter_compte_mensuel(cid, periode, debut, created_by)
        except IntegrityError:  # exécution concurrente : l'autre processus a déjà écrit la référence
            db.session.rollback()
            rapport["ignores"] += 1
            continue
        except Exception as exc:  # noqa: BLE001 : un compte en erreur ne bloque pas les autres
            log.exception("cloture_mensuelle : compte %s", cid)
            rapport["erreurs"].append({"compte_id": cid, "erreur": str(exc)})
            continue
        if r["ignore"]:
            rapport["ignores"] += 1
        if r["interets"] > 0:
            rapport["interets_verses"] += 1
            rapport["total_interets"] += r["interets"]
        if r["frais"] > 0:
            rapport["frais_preleves"] += 1
            rapport["total_frais"] += r["frais"]
        if r["frais_impayes"]:
            rapport["frais_impayes"].append(cid)
    return rapport


# --------------------------------------------------------------------------- #
# Lecture et contrôles
# --------------------------------------------------------------------------- #
def releve(compte_id, limite=200):
    q = (db.select(TransactionEpargne)
         .where(TransactionEpargne.compte_id == compte_id)
         .order_by(TransactionEpargne.created_at.desc(), TransactionEpargne.id.desc()).limit(limite))
    return list(db.session.execute(q).scalars())


def comptes_internes():
    return list(db.session.execute(db.select(CompteInterne).order_by(CompteInterne.code)).scalars())


def totaux_par_type(periode=None):
    """Totaux du grand livre côté clients, par type (ex. total des frais d'ouverture)."""
    q = (db.select(TransactionEpargne.type, func.count(), func.coalesce(func.sum(TransactionEpargne.montant), 0))
         .where(TransactionEpargne.compte_id.is_not(None)).group_by(TransactionEpargne.type))
    if periode:
        debut, fin = c.bornes_periode(periode)
        q = q.where(TransactionEpargne.created_at >= datetime.combine(debut, datetime.min.time()),
                    TransactionEpargne.created_at < datetime.combine(fin, datetime.min.time()))
    return [{"type": t, "nombre": n, "total": c.D(s)} for t, n, s in db.session.execute(q).all()]


def verifier_equilibre():
    """Contrôle d'intégrité : (1) chaque opération équilibre crédits et débits ;
    (2) le solde de chaque compte client correspond au grand livre."""
    credit = func.sum(case((TransactionEpargne.sens == "credit", TransactionEpargne.montant), else_=0))
    debit = func.sum(case((TransactionEpargne.sens == "debit", TransactionEpargne.montant), else_=0))
    desequilibres = db.session.execute(
        db.select(TransactionEpargne.groupe_id, credit, debit)
        .group_by(TransactionEpargne.groupe_id).having(credit != debit)).all()

    ecarts = []
    lignes = db.session.execute(
        db.select(TransactionEpargne.compte_id, credit, debit)
        .where(TransactionEpargne.compte_id.is_not(None)).group_by(TransactionEpargne.compte_id)).all()
    for compte_id, cr, de in lignes:
        compte = db.session.get(Epargne, compte_id)
        attendu = c.D(cr) - c.D(de)
        if compte is not None and _solde(compte) != attendu:
            ecarts.append({"compte_id": compte_id, "solde": _solde(compte), "grand_livre": attendu})
    return {"operations_desequilibrees": [r[0] for r in desequilibres], "comptes_en_ecart": ecarts}
