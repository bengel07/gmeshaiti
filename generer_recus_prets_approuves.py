from app import generer_recu_pour_pret
from models import Pret

def generer_recu_pour_un_pret(pret_id):
    pret = Pret.query.get(pret_id)

    if not pret:
        return None

    return generer_recu_pour_pret(pret)