"""Cœur comptable GMES : règles métier de l'épargne, SANS accès à la base de données.

Ce module décide de ce qui est permis et produit des ÉCRITURES à partie double :
chaque opération a toujours une jambe sur le compte du client et une jambe sur un compte
interne de GMES, et la somme des crédits est TOUJOURS égale à la somme des débits.

    Dépôt           client crédité      /  GMES-CAISSE débitée
    Retrait         client débité       /  GMES-CAISSE créditée
    Intérêts        client crédité      /  GMES-INTERETS débitée   (charge pour GMES)
    Frais, pénalité client débité       /  GMES-FRAIS créditée     (produit pour GMES)

Tous les montants sont des Decimal arrondis à 0,01 (arrondi commercial : 0,005 -> 0,01).
Convention : un montant limite à 0 signifie « pas de limite » (dépôt max, solde max, plafonds).
"""
import calendar
import re
from dataclasses import dataclass
from datetime import date
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

CENT = Decimal("0.01")
ZERO = Decimal("0.00")

CLIENT = "CLIENT"
CAISSE = "GMES-CAISSE"
FRAIS = "GMES-FRAIS"
INTERETS = "GMES-INTERETS"

# code -> (libellé, nature). Le solde d'un compte interne augmente au DÉBIT pour les natures
# « actif » et « charge », et au CRÉDIT pour « passif » et « produit ».
COMPTES_INTERNES = {
    CAISSE: ("Caisse : liquidités reçues et versées", "actif"),
    FRAIS: ("Produits : frais et pénalités encaissés", "produit"),
    INTERETS: ("Charges : intérêts versés aux clients", "charge"),
}
NATURES_AU_DEBIT = {"actif", "charge"}


class ErreurMetier(Exception):
    """Opération refusée par une règle métier (message affichable à l'utilisateur)."""


# --------------------------------------------------------------------------- #
# Montants
# --------------------------------------------------------------------------- #
def D(valeur):
    """Convertit en Decimal à 2 décimales. Accepte int, float, str ('1 250,50'), Decimal, None."""
    if valeur is None:
        return ZERO
    if isinstance(valeur, Decimal):
        brut = valeur
    else:
        try:
            brut = Decimal(str(valeur).strip().replace(" ", "").replace(",", "."))
        except InvalidOperation:
            raise ErreurMetier("Montant invalide.")
    if not brut.is_finite():
        raise ErreurMetier("Montant invalide.")
    return brut.quantize(CENT, rounding=ROUND_HALF_UP)


def pourcentage_de(montant, pct):
    return (D(montant) * Decimal(str(pct or 0)) / Decimal(100)).quantize(CENT, rounding=ROUND_HALF_UP)


def fmt(montant):
    return f"{D(montant):,.2f}".replace(",", " ") + " Gdes"


# --------------------------------------------------------------------------- #
# Dates
# --------------------------------------------------------------------------- #
def ajouter_mois(d, n):
    m = d.month - 1 + n
    annee, mois = d.year + m // 12, m % 12 + 1
    return date(annee, mois, min(d.day, calendar.monthrange(annee, mois)[1]))


def fin_blocage(date_ouverture, duree_mois):
    """Date à partir de laquelle les fonds sont libres (None s'il n'y a pas de blocage)."""
    if not duree_mois or date_ouverture is None:
        return None
    return ajouter_mois(date_ouverture, int(duree_mois))


def bornes_periode(periode):
    """'2026-10' -> (date(2026,10,1), date(2026,11,1)) : début inclus, fin exclue."""
    if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", periode or ""):
        raise ErreurMetier("Période invalide : format attendu AAAA-MM (ex. 2026-10).")
    annee, mois = int(periode[:4]), int(periode[5:])
    debut = date(annee, mois, 1)
    return debut, ajouter_mois(debut, 1)


# --------------------------------------------------------------------------- #
# Conditions du produit
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Conditions:
    taux_annuel: Decimal = ZERO
    depot_min: Decimal = ZERO
    depot_max: Decimal = ZERO
    solde_min: Decimal = ZERO
    solde_max: Decimal = ZERO
    frais_ouverture: Decimal = ZERO
    frais_mensuel: Decimal = ZERO
    frais_cloture: Decimal = ZERO
    plafond_depot_mensuel: Decimal = ZERO
    plafond_retrait_mensuel: Decimal = ZERO
    duree_blocage_mois: int = 0
    penalite_pct: Decimal = ZERO

    @classmethod
    def depuis_produit(cls, p):
        return cls(
            taux_annuel=Decimal(str(p.taux_interet_annuel or 0)),
            depot_min=D(p.depot_initial_min),
            depot_max=D(p.depot_initial_max),
            solde_min=D(p.solde_min),
            solde_max=D(p.solde_max),
            frais_ouverture=D(p.frais_ouverture),
            frais_mensuel=D(p.frais_tenue_compte_mensuel),
            frais_cloture=D(p.frais_cloture),
            plafond_depot_mensuel=D(p.plafond_depot_mensuel),
            plafond_retrait_mensuel=D(p.plafond_retrait_mensuel),
            duree_blocage_mois=int(p.duree_blocage_mois or 0),
            penalite_pct=Decimal(str(p.penalite_retrait_anticipe or 0)),
        )


# --------------------------------------------------------------------------- #
# Écritures
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Ecriture:
    compte: str      # CLIENT ou code d'un compte interne
    type: str        # depot_initial, depot, retrait, interets, frais_ouverture, ...
    sens: str        # "credit" | "debit"
    montant: Decimal


@dataclass(frozen=True)
class Plan:
    ecritures: tuple
    solde_apres: Decimal


def variation_interne(nature, sens, montant):
    """Variation (signée) du solde d'un compte interne pour une écriture."""
    au_debit = nature in NATURES_AU_DEBIT
    return montant if (sens == "debit") == au_debit else -montant


def _jambes(compte_interne, type_op, sens_client, montant):
    sens_interne = "debit" if sens_client == "credit" else "credit"
    return [Ecriture(CLIENT, type_op, sens_client, montant),
            Ecriture(compte_interne, type_op, sens_interne, montant)]


def _plan(solde, ecritures):
    ecritures = tuple(ecritures)
    credit = sum((e.montant for e in ecritures if e.sens == "credit"), ZERO)
    debit = sum((e.montant for e in ecritures if e.sens == "debit"), ZERO)
    if credit != debit:
        raise ErreurMetier("Écritures déséquilibrées : opération refusée.")
    delta = sum((e.montant if e.sens == "credit" else -e.montant
                 for e in ecritures if e.compte == CLIENT), ZERO)
    apres = D(solde) + delta
    if apres < 0:
        raise ErreurMetier("Solde insuffisant.")
    return Plan(ecritures, apres)


def _montant_positif(montant):
    m = D(montant)
    if m <= 0:
        raise ErreurMetier("Le montant doit être supérieur à zéro.")
    return m


# --------------------------------------------------------------------------- #
# Opérations
# --------------------------------------------------------------------------- #
def plan_activation(cond, depot_initial, solde=ZERO):
    """Ouverture : dépôt initial, puis frais d'ouverture prélevés sur ce dépôt."""
    depot = _montant_positif(depot_initial)
    if depot < cond.depot_min:
        raise ErreurMetier(f"Dépôt initial inférieur au minimum du produit ({fmt(cond.depot_min)}).")
    if cond.depot_max > 0 and depot > cond.depot_max:
        raise ErreurMetier(f"Dépôt initial supérieur au maximum du produit ({fmt(cond.depot_max)}).")
    net = depot - cond.frais_ouverture
    if net < 0:
        raise ErreurMetier(f"Le dépôt initial ne couvre pas les frais d'ouverture ({fmt(cond.frais_ouverture)}).")
    if net < cond.solde_min:
        raise ErreurMetier(f"Après les frais d'ouverture, le solde ({fmt(net)}) serait inférieur "
                           f"au solde minimum du produit ({fmt(cond.solde_min)}).")
    if cond.solde_max > 0 and D(solde) + net > cond.solde_max:
        raise ErreurMetier(f"Le solde dépasserait le maximum du produit ({fmt(cond.solde_max)}).")
    ecr = _jambes(CAISSE, "depot_initial", "credit", depot)
    if cond.frais_ouverture > 0:
        ecr += _jambes(FRAIS, "frais_ouverture", "debit", cond.frais_ouverture)
    return _plan(solde, ecr)


def plan_depot(cond, solde, montant, deja_depose_mois=ZERO):
    m = _montant_positif(montant)
    if cond.solde_max > 0 and D(solde) + m > cond.solde_max:
        raise ErreurMetier(f"Le solde dépasserait le maximum du produit ({fmt(cond.solde_max)}).")
    if cond.plafond_depot_mensuel > 0 and D(deja_depose_mois) + m > cond.plafond_depot_mensuel:
        reste = max(cond.plafond_depot_mensuel - D(deja_depose_mois), ZERO)
        raise ErreurMetier(f"Plafond de dépôt mensuel dépassé (reste {fmt(reste)} ce mois-ci).")
    return _plan(solde, _jambes(CAISSE, "depot", "credit", m))


def plan_retrait(cond, solde, montant, deja_retire_mois=ZERO, fin_blocage_le=None, aujourdhui=None):
    """Retrait. En période de blocage : refusé s'il n'y a pas de pénalité, sinon pénalité en %
    du montant retiré, prélevée EN PLUS du montant."""
    m = _montant_positif(montant)
    aujourdhui = aujourdhui or date.today()
    en_blocage = fin_blocage_le is not None and aujourdhui < fin_blocage_le
    if en_blocage and cond.penalite_pct <= 0:
        raise ErreurMetier(f"Fonds bloqués jusqu'au {fin_blocage_le:%d/%m/%Y}.")
    if cond.plafond_retrait_mensuel > 0 and D(deja_retire_mois) + m > cond.plafond_retrait_mensuel:
        reste = max(cond.plafond_retrait_mensuel - D(deja_retire_mois), ZERO)
        raise ErreurMetier(f"Plafond de retrait mensuel dépassé (reste {fmt(reste)} ce mois-ci).")
    penalite = pourcentage_de(m, cond.penalite_pct) if en_blocage else ZERO
    total = m + penalite
    if total > D(solde):
        detail = f" (dont pénalité de retrait anticipé {fmt(penalite)})" if penalite > 0 else ""
        raise ErreurMetier(f"Solde insuffisant : {fmt(total)} nécessaires{detail}, solde {fmt(solde)}.")
    if D(solde) - total < cond.solde_min:
        raise ErreurMetier(f"Le solde ne peut pas descendre sous le solde minimum ({fmt(cond.solde_min)}).")
    ecr = _jambes(CAISSE, "retrait", "debit", m)
    if penalite > 0:
        ecr += _jambes(FRAIS, "penalite", "debit", penalite)
    return _plan(solde, ecr)


def plan_interets(cond, solde):
    """Intérêts d'un mois = solde x taux annuel / 12 (arrondi à 0,01). None s'il n'y en a pas."""
    solde = D(solde)
    if solde <= 0 or cond.taux_annuel <= 0:
        return None
    montant = (solde * cond.taux_annuel / Decimal(100) / Decimal(12)).quantize(CENT, rounding=ROUND_HALF_UP)
    if montant <= 0:
        return None
    return _plan(solde, _jambes(INTERETS, "interets", "credit", montant))


def plan_frais_mensuel(cond, solde):
    """Frais de tenue de compte. None s'il n'y en a pas ; refusé si le solde ne les couvre pas."""
    if cond.frais_mensuel <= 0:
        return None
    if D(solde) < cond.frais_mensuel:
        raise ErreurMetier(f"Solde insuffisant pour les frais mensuels ({fmt(cond.frais_mensuel)}).")
    return _plan(solde, _jambes(FRAIS, "frais_mensuel", "debit", cond.frais_mensuel))


def plan_cloture(cond, solde, fin_blocage_le=None, aujourdhui=None):
    """Clôture : frais de clôture (+ pénalité si fonds encore bloqués), le reste est versé au client.
    Les frais sont plafonnés au solde (le client ne peut pas rester débiteur)."""
    solde = D(solde)
    aujourdhui = aujourdhui or date.today()
    en_blocage = fin_blocage_le is not None and aujourdhui < fin_blocage_le
    if en_blocage and cond.penalite_pct <= 0:
        raise ErreurMetier(f"Fonds bloqués jusqu'au {fin_blocage_le:%d/%m/%Y} : clôture impossible avant.")
    penalite = pourcentage_de(solde, cond.penalite_pct) if en_blocage else ZERO
    frais_c = min(cond.frais_cloture, solde)
    pen_c = min(penalite, solde - frais_c)
    net = solde - frais_c - pen_c
    ecr = []
    if frais_c > 0:
        ecr += _jambes(FRAIS, "frais_cloture", "debit", frais_c)
    if pen_c > 0:
        ecr += _jambes(FRAIS, "penalite", "debit", pen_c)
    if net > 0:
        ecr += _jambes(CAISSE, "retrait_cloture", "debit", net)
    return _plan(solde, ecr)
