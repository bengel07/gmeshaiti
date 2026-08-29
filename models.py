

# import sys
#
# if "models" in sys.modules:
#     del sys.modules["models"]

from database import db
from datetime import datetime, date

user_permissions = db.Table(
    'user_permissions',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'))
)

# Table d'association pour la relation many-to-many entre Dossier et Document
dossier_documents = db.Table('dossier_documents',
                             db.Column('dossier_id', db.Integer, db.ForeignKey('dossiers.id'), primary_key=True),
                             db.Column('document_id', db.Integer, db.ForeignKey('documents.id'), primary_key=True),
                             db.Column('date_ajout', db.DateTime, default=datetime.utcnow)
                             )

import os  # ← AJOUTEZ CETTE LIGNE
import pickle


import requests
import flet as ft  # Assurez-vous d'avoir importé votre bibliothèque d'interface
# from deepface import DeepFace
from werkzeug.security import generate_password_hash, check_password_hash



import sqlite3
from flask_login import UserMixin  # ← AJOUTEZ CETTE LIGNE

import random
import string

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DecimalField, DateField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Optional


# from sqlalchemy import MetaData
# metadata = MetaData()
#


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # Champs communs à tous les utilisateurs
    username = db.Column(db.String(800), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(200), default='client')  # client, employe, admin, superviseur
    statut = db.Column(db.String(200), default='actif')  # 'actif', 'en_attente', 'inactif'

    # approuve_par = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Admin qui a approuvé

    # permissions = db.Column(db.Text)  # Stocke les permissions en JSON
    nom_complet=db.Column(db.String(100))
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    telephone = db.Column(db.String(200))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    groupe_id = db.Column(db.Integer, db.ForeignKey('groupes.id'), nullable=True)

    # Champs spécifiques aux clients
    id_client = db.Column(db.String(200), unique=True, nullable=True)
    adresse = db.Column(db.Text)
    cin_nif = db.Column(db.String(500), unique=True, nullable=True)
    date_naissance = db.Column(db.DateTime, nullable=True)
    profession = db.Column(db.String(1000))
    lieu_naissance = db.Column(db.String(1000))
    nationalite = db.Column(db.String(1000))
    autre_nationalite = db.Column(db.String(100))
    commune = db.Column(db.String(1000))
    duree_adresse = db.Column(db.Integer)
    etat_civil = db.Column(db.String(1000))
    nom_conjoint = db.Column(db.String(1000))
    nb_enfants = db.Column(db.Integer)

    revenu_mensuel = db.Column(db.Float, default=0)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)

    # ⚠️ AJOUTEZ CES CHAMPS MANQUANTS :
    niveau_habilitation = db.Column(db.Integer, default=1)  # Niveau 1-4
    derniere_activite = db.Column(db.DateTime, default=datetime.utcnow)
    verifications_completes = db.Column(db.Boolean, default=False)
    formation_aml_cft = db.Column(db.Boolean, default=False)
    matricule = db.Column(db.String(200), unique=True, default=lambda: "EMP-" + ''.join(random.choices("0123456789", k=6)))  # Matricule d'employé

    # Nouveaux champs
    depenses_mensuelles = db.Column(db.Float, default=0)
    capacite_remboursement = db.Column(db.Float, default=0)
    photo_id = db.Column(db.String(2505))
    photo_selfie = db.Column(db.String(2505))
    verification_faciale = db.Column(db.Boolean, default=False)
    score_verification = db.Column(db.Float, default=0)
    terms_accepted = db.Column(db.Boolean, default=False, nullable=False)  # This should exist

    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=True)

    succursale = db.relationship('Succursale',
                                 foreign_keys=[succursale_id],
                                 back_populates='users')

    role_succursale = db.Column(db.String(50))  # directeur, caissier, conseiller_succursale

    # Champs pour l'historique
    date_embauche = db.Column(db.DateTime, nullable=True)
    date_depart = db.Column(db.DateTime, nullable=True)
    motif_depart = db.Column(db.String(1000), nullable=True)
    fonction = db.Column(db.String(1000), nullable=True)  # si vous avez ajouté ce champ

    # Dans models.py, classe User
    cree_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    token_signature = db.Column(db.Text, unique=True, nullable=True)
    date_envoi_terms = db.Column(db.DateTime, nullable=True)
    date_signature = db.Column(db.DateTime, nullable=True)
    sexe = db.Column(db.String(10), nullable=True)  # 'M' ou 'F'

    parent_nom = db.Column(db.String(1000), nullable=True)
    parent_signature = db.Column(db.Text, nullable=True)
    date_expiration_token = db.Column(db.DateTime, nullable=True)
    date_signature_terms = db.Column(db.DateTime, nullable=True)

    date_approbation = db.Column(db.DateTime, nullable=True)
    approuve_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    motif_rejet = db.Column(db.Text, nullable=True)
    date_rejet = db.Column(db.DateTime, nullable=True)
    rejete_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    derniere_connexion = db.Column(db.DateTime, nullable=True)

    photo_profil = db.Column(db.String(2505))
    photo_recto = db.Column(db.String(2505))
    photo_verso = db.Column(db.String(2055))

    id_number = db.Column(db.String(1000), unique=True)
    id_type = db.Column(db.String(500))

    carte_generee = db.Column(db.Boolean, default=False)
    carte_path = db.Column(db.String(200))


    photo = db.Column(db.String(200))
    qr_code = db.Column(db.String(200))
    qr_token = db.Column(db.String(200), unique=True)
    carte_expiration = db.Column(db.DateTime)
    actif = db.Column(db.Boolean, default=False)
    departement = db.Column(db.String(100), nullable=True)
    # Exigences BRH
    # date_embauche = db.Column(db.Date, default=datetime.utcnow)
    verification_antecedents = db.Column(db.Boolean, default=False)
    date_verification_antecedents = db.Column(db.DateTime)
    # formation_aml_cft = db.Column(db.Boolean, default=False)
    date_formation_aml_cft = db.Column(db.DateTime)
    statut_conformite = db.Column(db.String(50), default='en_attente')  # 'en_attente', 'conforme', 'non_conforme'

    carte_numero = db.Column(db.String(500), unique=True, nullable=True)
    est_actif = db.Column(db.Boolean, default=True)

    # Relation avec Partner


    # Ajoute cette ligne pour la relation avec Partner



    # ➕ AJOUTEZ CETTE RELATION (vers ligne ~600)
    permissions = db.relationship(
        "Permission",
        secondary='user_permissions',
        back_populates="users",
        lazy="select"
    )

    def generer_matricule(self):
        import random
        import string
        return "EMP-" + ''.join(random.choices(string.digits, k=6))

    def generate_unique_carte_numero(self):
        while True:
            numero = generate_carte_numero()
            if not User.query.filter_by(carte_numero=numero).first():
                return numero



    # Relations

    modifications_effectuees = db.relationship("HistoriqueEmploye", foreign_keys="HistoriqueEmploye.modifie_par_id", back_populates="modifie_par")

    # 🔐 Gestion du premier changement
    premier_connexion = db.Column(db.Boolean, default=True)  # True = doit changer son mot de passe
    date_premiere_connexion = db.Column(db.DateTime, nullable=True)

    # 📝 Questions secrètes
    question_secrete_1 = db.Column(db.String(200), nullable=True)
    reponse_secrete_1 = db.Column(db.String(200), nullable=True)
    question_secrete_2 = db.Column(db.String(200), nullable=True)
    reponse_secrete_2 = db.Column(db.String(200), nullable=True)
    question_secrete_3 = db.Column(db.String(200), nullable=True)
    reponse_secrete_3 = db.Column(db.String(200), nullable=True)

    # 🔑 Demande de changement de mot de passe
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)
    demande_reset_date = db.Column(db.DateTime, nullable=True)

    # 🆔 Changement d'username
    nouveau_username_demande = db.Column(db.String(80), nullable=True)
    demande_username_status = db.Column(db.String(20), default='aucune')  # 'en_attente', 'approuve', 'rejete'
    demande_username_date = db.Column(db.DateTime, nullable=True)

    entreprise = db.Column(db.String(200), nullable=True)
    adresse_travail = db.Column(db.String(500), nullable=True)
    tel_travail = db.Column(db.String(50), nullable=True)
    autres_revenus = db.Column(db.Float, default=0)
    photo_face = db.Column(db.String(500), nullable=True)
    photo_dos = db.Column(db.String(500), nullable=True)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission_name):
        """
        Vérifie si l'utilisateur a une permission spécifique
        Version robuste avec gestion d'erreurs
        """
        # Sécurité : si l'utilisateur n'existe pas
        if not self or not self.is_authenticated:
            return False

        # 1️⃣ SUPER ADMIN - Tous les accès
        if self.role == 'super_admin':
            return True

        # 2️⃣ ADMIN - Tous les accès
        if self.role == 'admin':
            return True

        # 3️⃣ ADMIN SUCCURSALE - Accès à toutes les permissions de sa succursale
        if self.role == 'admin_succursale':
            # Les admins de succursale ont accès à toutes les permissions
            return True

        # 4️⃣ SUPERVISEUR - Accès à tous les dashboards employés
        if self.role == 'superviseur':
            superviseur_permissions = [
                'caissier',
                'conseiller',
                'analyste_credit',
                'gestionnaire_groupe',
                'rapports',
                'agent_credit',
                'agent_remboursement'
            ]
            return permission_name in superviseur_permissions

        # 5️⃣ EMPLOYÉ - Vérification des permissions spécifiques
        if self.role == 'employe':
            # Vérifier d'abord par la fonction (plus simple)
            if hasattr(self, 'fonction') and self.fonction == permission_name:
                return True

            # Ensuite vérifier par la liste JSON des permissions
            if hasattr(self, 'permissions') and self.permissions:
                try:
                    import json
                    # Si c'est déjà une liste, pas besoin de json.loads
                    if isinstance(self.permissions, list):
                        return permission_name in self.permissions
                    # Sinon, essayer de parser le JSON
                    elif isinstance(self.permissions, str):
                        permissions_list = json.loads(self.permissions)
                        return permission_name in permissions_list
                except (json.JSONDecodeError, TypeError, ValueError) as e:
                    # Log l'erreur pour debug
                    print(f"⚠️ Erreur parsing permissions pour {self.username}: {e}")
                    # Fallback: vérification par la fonction (déjà fait)
                    pass

            # Vérifier par l'attribut fonction (fallback)
            return getattr(self, 'fonction', None) == permission_name

        # 6️⃣ CLIENT - Pas de permissions spéciales
        if self.role == 'client':
            return False

        # 7️⃣ AUTRES RÔLES - Par défaut, pas de permissions
        return False

    def has_any_permission(self, *permission_names):
        """
        Vérifie si l'utilisateur a au moins une des permissions
        Utile pour les pages accessibles par plusieurs rôles
        """
        return any(self.has_permission(p) for p in permission_names)

    def has_all_permissions(self, *permission_names):
        """
        Vérifie si l'utilisateur a toutes les permissions
        Utile pour les actions sensibles
        """
        return all(self.has_permission(p) for p in permission_names)




# =============================================
# CONSTANTES POUR LES INTERACTIONS
# =============================================

TYPES_INTERACTION = {
    'appel_telephonique': 'Appel téléphonique',
    'email': 'Email',
    'visite': 'Visite physique',
    'reunion': 'Réunion',
    'message': 'Message (WhatsApp/SMS)',
    'autre': 'Autre'
}

RESULTATS_INTERACTION = {
    'positif': 'Positif',
    'negatif': 'Négatif',
    'neutre': 'Neutre',
    'en_attente': 'En attente'
}

STATUTS_INTERACTION = {
    'actif': 'Actif',
    'archive': 'Archivé',
    'supprime': 'Supprimé'
}

PRIORITES_INTERACTION = {
    'basse': 'Basse',
    'normale': 'Normale',
    'haute': 'Haute',
    'urgente': 'Urgente'
}


class Interaction(db.Model):
    """Modèle pour les interactions avec les clients"""

    __tablename__ = 'interactions'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    relation_client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Type d'interaction
    type_interaction = db.Column(db.String(50), nullable=False)
    # Options: 'appel_telephonique', 'email', 'visite', 'reunion', 'message', 'autre'

    # Contenu
    sujet = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    # Résultat
    resultat = db.Column(db.String(50), nullable=True)
    # Options: 'positif', 'negatif', 'neutre', 'en_attente'

    # Satisfaction (1-5)
    satisfaction = db.Column(db.Integer, nullable=True)

    # Suivi
    suivi_necessaire = db.Column(db.Boolean, default=False)
    suivi_date = db.Column(db.DateTime, nullable=True)
    suivi_effectue = db.Column(db.Boolean, default=False)

    # Dates
    date_interaction = db.Column(db.DateTime, default=datetime.utcnow)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Statut
    statut = db.Column(db.String(50), default='actif')
    # Options: 'actif', 'archive', 'supprime'

    # Métadonnées
    duree = db.Column(db.Integer, nullable=True)  # Durée en minutes
    priorite = db.Column(db.String(20), default='normale')
    # Options: 'basse', 'normale', 'haute', 'urgente'

    # Relations inverses
    client = db.relationship('Client', backref='interactions', lazy=True)
    agent = db.relationship('User', foreign_keys=[agent_id], backref='interactions_agent', lazy=True)
    relation_client = db.relationship('User', foreign_keys=[relation_client_id], backref='interactions_relation',
                                      lazy=True)

    def __init__(self, client_id, agent_id, type_interaction, sujet, **kwargs):
        self.client_id = client_id
        self.agent_id = agent_id
        self.type_interaction = type_interaction
        self.sujet = sujet
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<Interaction {self.id} - {self.client.prenom} {self.client.nom} - {self.type_interaction}>'

    @staticmethod
    def get_interactions_client(client_id, limit=None):
        """Récupère toutes les interactions d'un client"""
        query = Interaction.query.filter_by(client_id=client_id, statut='actif').order_by(
            Interaction.date_interaction.desc()
        )
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_interactions_agent(agent_id, limit=None):
        """Récupère toutes les interactions d'un agent"""
        query = Interaction.query.filter_by(agent_id=agent_id, statut='actif').order_by(
            Interaction.date_interaction.desc()
        )
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_suivi_necessaire():
        """Récupère les interactions nécessitant un suivi"""
        return Interaction.query.filter_by(
            suivi_necessaire=True,
            suivi_effectue=False,
            statut='actif'
        ).order_by(Interaction.suivi_date.asc()).all()

    @staticmethod
    def get_statistiques_agent(agent_id, date_debut=None, date_fin=None):
        """Statistiques des interactions d'un agent"""
        query = Interaction.query.filter_by(agent_id=agent_id, statut='actif')

        if date_debut:
            query = query.filter(Interaction.date_interaction >= date_debut)
        if date_fin:
            query = query.filter(Interaction.date_interaction <= date_fin)

        interactions = query.all()

        total = len(interactions)
        positives = len([i for i in interactions if i.resultat == 'positif'])
        negatives = len([i for i in interactions if i.resultat == 'negatif'])
        neutres = len([i for i in interactions if i.resultat == 'neutre'])

        satisfaction = [i.satisfaction for i in interactions if i.satisfaction]
        satisfaction_moyenne = sum(satisfaction) / len(satisfaction) if satisfaction else 0

        return {
            'total': total,
            'positives': positives,
            'negatives': negatives,
            'neutres': neutres,
            'satisfaction_moyenne': round(satisfaction_moyenne, 2),
            'taux_positif': round((positives / total * 100), 2) if total > 0 else 0,
            'taux_negatif': round((negatives / total * 100), 2) if total > 0 else 0
        }

    @staticmethod
    def get_activite_recente(agent_id, limit=10):
        """Récupère l'activité récente d'un agent"""
        return Interaction.query.filter_by(
            agent_id=agent_id,
            statut='actif'
        ).order_by(Interaction.date_interaction.desc()).limit(limit).all()

    def to_dict(self):
        """Convertit l'interaction en dictionnaire"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'client_nom': f"{self.client.prenom} {self.client.nom}" if self.client else None,
            'agent_id': self.agent_id,
            'agent_nom': f"{self.agent.prenom} {self.agent.nom}" if self.agent else None,
            'type_interaction': self.type_interaction,
            'sujet': self.sujet,
            'description': self.description,
            'notes': self.notes,
            'resultat': self.resultat,
            'satisfaction': self.satisfaction,
            'suivi_necessaire': self.suivi_necessaire,
            'suivi_date': self.suivi_date.isoformat() if self.suivi_date else None,
            'suivi_effectue': self.suivi_effectue,
            'date_interaction': self.date_interaction.isoformat(),
            'duree': self.duree,
            'priorite': self.priorite,
            'statut': self.statut
        }


class MembreGroupe(db.Model):
    """Modèle pour les membres d'un groupe"""

    __tablename__ = 'membres_groupes'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    groupe_id = db.Column(db.Integer, db.ForeignKey('groupes.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    ajoute_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Rôle dans le groupe
    role = db.Column(db.String(50), default='membre')
    # Options: 'membre', 'chef_groupe', 'secretaire', 'tresorier', 'animateur_adjoint'

    # Date d'adhésion
    date_adhesion = db.Column(db.DateTime, default=datetime.utcnow)
    date_sortie = db.Column(db.DateTime, nullable=True)

    # Statut
    statut = db.Column(db.String(200), default='actif')
    # Options: 'actif', 'inactif', 'suspendu', 'sorti'

    # Métadonnées
    notes = db.Column(db.Text, nullable=True)

    # Relations inverses
    groupe = db.relationship('Groupe', backref='membres', lazy=True)
    client = db.relationship('Client', backref='groupes_membres', lazy=True)
    ajoute_par = db.relationship('User', foreign_keys=[ajoute_par_id], backref='membres_ajoutes', lazy=True)

    def __repr__(self):
        return f'<MembreGroupe {self.id} - {self.client.prenom} {self.client.nom} - {self.groupe.nom}>'

    @staticmethod
    def get_membres_groupe(groupe_id):
        """Récupère tous les membres d'un groupe"""
        return MembreGroupe.query.filter_by(groupe_id=groupe_id, statut='actif').all()

    @staticmethod
    def get_groupes_client(client_id):
        """Récupère tous les groupes d'un client"""
        return MembreGroupe.query.filter_by(client_id=client_id, statut='actif').all()

    def to_dict(self):
        return {
            'id': self.id,
            'groupe_id': self.groupe_id,
            'groupe_nom': self.groupe.nom if self.groupe else None,
            'client_id': self.client_id,
            'client_nom': f"{self.client.prenom} {self.client.nom}" if self.client else None,
            'role': self.role,
            'date_adhesion': self.date_adhesion.isoformat(),
            'statut': self.statut,
            'notes': self.notes
        }


# =============================================
# MODÈLE POUR LES SESSIONS DE GROUPES
# =============================================

class SessionGroupe(db.Model):
    """Modèle pour les sessions d'un groupe"""

    __tablename__ = 'sessions_groupes'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    groupe_id = db.Column(db.Integer, db.ForeignKey('groupes.id'), nullable=False)
    animateur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Informations
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    objectif = db.Column(db.Text, nullable=True)

    # Dates
    date_debut = db.Column(db.DateTime, nullable=False)
    date_fin = db.Column(db.DateTime, nullable=True)

    # Lieu
    lieu = db.Column(db.String(200), nullable=True)
    adresse = db.Column(db.String(300), nullable=True)

    # Participants
    nb_participants = db.Column(db.Integer, default=0)
    capacite = db.Column(db.Integer, default=20)
    taux_participation = db.Column(db.Float, default=0.0)

    # Évaluation
    evaluation = db.Column(db.Float, nullable=True)  # Note sur 5
    commentaires = db.Column(db.Text, nullable=True)

    # Statut
    statut = db.Column(db.String(20), default='planifiee')
    # Options: 'planifiee', 'en_cours', 'terminee', 'annulee', 'reportee'

    # Métadonnées
    materiel_necessaire = db.Column(db.Text, nullable=True)
    notes_preparation = db.Column(db.Text, nullable=True)

    # Dates système
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations inverses
    groupe = db.relationship('Groupe', backref='sessions', lazy=True)
    animateur = db.relationship('User', foreign_keys=[animateur_id], backref='sessions_animees', lazy=True)

    def __repr__(self):
        return f'<SessionGroupe {self.id} - {self.titre} - {self.groupe.nom}>'

    def get_participants(self):
        """Récupère les participants à la session"""
        return ParticipationSession.query.filter_by(session_id=self.id, statut='confirme').all()

    def get_nb_participants(self):
        """Retourne le nombre de participants"""
        return ParticipationSession.query.filter_by(session_id=self.id, statut='confirme').count()

    def update_taux_participation(self):
        """Met à jour le taux de participation"""
        total_membres = self.groupe.nb_membres or 1
        self.taux_participation = round((self.nb_participants / total_membres * 100), 2) if total_membres > 0 else 0
        db.session.commit()

    def peut_ajouter_participant(self):
        """Vérifie si la session peut accueillir un participant supplémentaire"""
        return self.nb_participants < self.capacite

    def ajouter_participant(self, client_id):
        """Ajoute un participant à la session"""
        if not self.peut_ajouter_participant():
            return False, "Capacité maximale atteinte"

        # Vérifier si déjà inscrit
        existing = ParticipationSession.query.filter_by(
            session_id=self.id,
            client_id=client_id
        ).first()
        if existing:
            return False, "Déjà inscrit"

        participation = ParticipationSession(
            session_id=self.id,
            client_id=client_id,
            statut='confirme'
        )
        db.session.add(participation)
        self.nb_participants += 1
        self.update_taux_participation()
        db.session.commit()
        return True, "Participant ajouté"

    def to_dict(self):
        return {
            'id': self.id,
            'groupe_id': self.groupe_id,
            'groupe_nom': self.groupe.nom if self.groupe else None,
            'animateur_id': self.animateur_id,
            'animateur_nom': f"{self.animateur.prenom} {self.animateur.nom}" if self.animateur else None,
            'titre': self.titre,
            'description': self.description,
            'objectif': self.objectif,
            'date_debut': self.date_debut.isoformat(),
            'date_fin': self.date_fin.isoformat() if self.date_fin else None,
            'lieu': self.lieu,
            'nb_participants': self.nb_participants,
            'capacite': self.capacite,
            'taux_participation': self.taux_participation,
            'evaluation': self.evaluation,
            'statut': self.statut
        }


# =============================================
# MODÈLE POUR LES PARTICIPATIONS AUX SESSIONS
# =============================================

class ParticipationSession(db.Model):
    """Modèle pour les participations aux sessions de groupe"""

    __tablename__ = 'participations_sessions'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    session_id = db.Column(db.Integer, db.ForeignKey('sessions_groupes.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    # Dates
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)
    date_presence = db.Column(db.DateTime, nullable=True)

    # Statut
    statut = db.Column(db.String(20), default='confirme')
    # Options: 'confirme', 'present', 'absent', 'annule'

    # Évaluation individuelle
    evaluation = db.Column(db.Float, nullable=True)  # Note sur 5
    commentaire = db.Column(db.Text, nullable=True)

    # Métadonnées
    a_ponctuel = db.Column(db.Boolean, default=True)

    # Relations inverses
    session = db.relationship('SessionGroupe', backref='participations', lazy=True)
    client = db.relationship('Client', backref='participations_sessions', lazy=True)

    def __repr__(self):
        return f'<ParticipationSession {self.id} - {self.client.prenom} {self.client.nom} - {self.session.titre}>'

    def marquer_present(self):
        """Marque le participant comme présent"""
        self.statut = 'present'
        self.date_presence = datetime.utcnow()
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'client_id': self.client_id,
            'client_nom': f"{self.client.prenom} {self.client.nom}" if self.client else None,
            'statut': self.statut,
            'date_inscription': self.date_inscription.isoformat(),
            'evaluation': self.evaluation,
            'commentaire': self.commentaire
        }


class DossierSaisie(db.Model):
    """Modèle pour les dossiers à saisir par l'agent saisie"""

    __tablename__ = 'dossiers_saisie'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    agent_saisie_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    superviseur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Informations du dossier
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Type de document
    type_document = db.Column(db.String(50), nullable=False)
    # Options: 'formulaire', 'contrat', 'facture', 'document_identite', 'justificatif', 'autre'

    # Priorité
    priorite = db.Column(db.String(20), default='normale')
    # Options: 'basse', 'normale', 'haute', 'urgente'

    # Dates
    date_reception = db.Column(db.DateTime, default=datetime.utcnow)
    date_saisie = db.Column(db.DateTime, nullable=True)
    date_validation = db.Column(db.DateTime, nullable=True)
    date_limite = db.Column(db.DateTime, nullable=True)

    # Statut
    statut = db.Column(db.String(50), default='a_saisir')
    # Options: 'a_saisir', 'en_cours', 'saisi', 'en_attente_validation', 'valide', 'rejete', 'archive'

    # Métadonnées
    fichier_original = db.Column(db.String(255), nullable=True)
    fichier_saisie = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    commentaires_validation = db.Column(db.Text, nullable=True)

    # Temps passé
    temps_saisie = db.Column(db.Integer, nullable=True)  # en minutes
    temps_validation = db.Column(db.Integer, nullable=True)  # en minutes

    # Dates système
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations inverses
    client = db.relationship('Client', backref='dossiers_saisie', lazy=True)
    agent_saisie = db.relationship('User', foreign_keys=[agent_saisie_id], backref='dossiers_a_saisir', lazy=True)
    superviseur = db.relationship('User', foreign_keys=[superviseur_id], backref='dossiers_a_valider', lazy=True)

    def __repr__(self):
        return f'<DossierSaisie {self.id} - {self.titre} - {self.statut}>'

    @staticmethod
    def get_a_saisir(agent_id, limit=None):
        """Récupère les dossiers à saisir pour un agent"""
        query = DossierSaisie.query.filter_by(
            agent_saisie_id=agent_id,
            statut='a_saisir'
        ).order_by(DossierSaisie.priorite.desc(), DossierSaisie.date_limite.asc())
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_en_cours(agent_id, limit=None):
        """Récupère les dossiers en cours de saisie"""
        query = DossierSaisie.query.filter_by(
            agent_saisie_id=agent_id,
            statut='en_cours'
        ).order_by(DossierSaisie.date_modification.desc())
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_en_attente_validation(agent_id, limit=None):
        """Récupère les dossiers en attente de validation"""
        query = DossierSaisie.query.filter_by(
            agent_saisie_id=agent_id,
            statut='en_attente_validation'
        ).order_by(DossierSaisie.date_saisie.desc())
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_statistiques_agent(agent_id):
        """Statistiques des dossiers d'un agent"""
        total = DossierSaisie.query.filter_by(agent_saisie_id=agent_id).count()
        a_saisir = DossierSaisie.query.filter_by(agent_saisie_id=agent_id, statut='a_saisir').count()
        en_cours = DossierSaisie.query.filter_by(agent_saisie_id=agent_id, statut='en_cours').count()
        saisis = DossierSaisie.query.filter_by(agent_saisie_id=agent_id, statut='saisi').count()
        en_attente = DossierSaisie.query.filter_by(agent_saisie_id=agent_id, statut='en_attente_validation').count()
        valides = DossierSaisie.query.filter_by(agent_saisie_id=agent_id, statut='valide').count()
        rejetes = DossierSaisie.query.filter_by(agent_saisie_id=agent_id, statut='rejete').count()

        # Taux de saisie
        traites = saisis + valides
        taux_saisie = round((traites / total * 100), 2) if total > 0 else 0

        # Temps moyen de saisie
        temps_total = db.session.query(db.func.sum(DossierSaisie.temps_saisie)).filter(
            DossierSaisie.agent_saisie_id == agent_id,
            DossierSaisie.temps_saisie.isnot(None)
        ).scalar() or 0
        nb_avec_temps = DossierSaisie.query.filter(
            DossierSaisie.agent_saisie_id == agent_id,
            DossierSaisie.temps_saisie.isnot(None)
        ).count()
        temps_moyen = round(temps_total / nb_avec_temps, 2) if nb_avec_temps > 0 else 0

        return {
            'total': total,
            'a_saisir': a_saisir,
            'en_cours': en_cours,
            'saisis': saisis,
            'en_attente': en_attente,
            'valides': valides,
            'rejetes': rejetes,
            'taux_saisie': taux_saisie,
            'temps_moyen_saisie': temps_moyen
        }

    @staticmethod
    def get_urgents(agent_id):
        """Récupère les dossiers urgents à saisir"""
        return DossierSaisie.query.filter(
            DossierSaisie.agent_saisie_id == agent_id,
            DossierSaisie.statut.in_(['a_saisir', 'en_cours']),
            DossierSaisie.priorite.in_(['haute', 'urgente'])
        ).order_by(DossierSaisie.priorite.desc(), DossierSaisie.date_limite.asc()).all()

    def commencer_saisie(self):
        """Démarre la saisie du dossier"""
        self.statut = 'en_cours'
        db.session.commit()

    def terminer_saisie(self, temps=None):
        """Termine la saisie du dossier"""
        self.statut = 'saisi'
        self.date_saisie = datetime.utcnow()
        if temps:
            self.temps_saisie = temps
        db.session.commit()

    def soumettre_validation(self):
        """Soumet le dossier pour validation"""
        self.statut = 'en_attente_validation'
        db.session.commit()

    def valider(self, superviseur_id, commentaires=None):
        """Valide le dossier"""
        self.statut = 'valide'
        self.superviseur_id = superviseur_id
        self.date_validation = datetime.utcnow()
        if commentaires:
            self.commentaires_validation = commentaires
        db.session.commit()

    def rejeter(self, superviseur_id, commentaires=None):
        """Rejette le dossier"""
        self.statut = 'rejete'
        self.superviseur_id = superviseur_id
        if commentaires:
            self.commentaires_validation = commentaires
        db.session.commit()

    def to_dict(self):
        """Convertit le dossier en dictionnaire"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'client_nom': f"{self.client.prenom} {self.client.nom}" if self.client else None,
            'agent_saisie_id': self.agent_saisie_id,
            'agent_nom': f"{self.agent_saisie.prenom} {self.agent_saisie.nom}" if self.agent_saisie else None,
            'titre': self.titre,
            'description': self.description,
            'type_document': self.type_document,
            'priorite': self.priorite,
            'date_reception': self.date_reception.isoformat(),
            'date_saisie': self.date_saisie.isoformat() if self.date_saisie else None,
            'date_validation': self.date_validation.isoformat() if self.date_validation else None,
            'date_limite': self.date_limite.isoformat() if self.date_limite else None,
            'statut': self.statut,
            'temps_saisie': self.temps_saisie,
            'notes': self.notes,
            'commentaires_validation': self.commentaires_validation
        }


# =============================================
# CONSTANTES POUR LES DOSSIERS DE SAISIE
# =============================================

TYPES_DOCUMENT = {
    'formulaire': 'Formulaire',
    'contrat': 'Contrat',
    'facture': 'Facture',
    'document_identite': 'Document d\'identité',
    'justificatif': 'Justificatif',
    'autre': 'Autre'
}

PRIORITES_DOSSIER = {
    'basse': 'Basse',
    'normale': 'Normale',
    'haute': 'Haute',
    'urgente': 'Urgente'
}

STATUTS_DOSSIER = {
    'a_saisir': 'À saisir',
    'en_cours': 'En cours',
    'saisi': 'Saisi',
    'en_attente_validation': 'En attente de validation',
    'valide': 'Validé',
    'rejete': 'Rejeté',
    'archive': 'Archivé'
}


class VerificationConformite(db.Model):
    """Modèle pour les vérifications de conformité"""

    __tablename__ = 'verifications_conformite'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    agent_conformite_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    superviseur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Type de vérification
    type_verification = db.Column(db.String(50), nullable=False)
    # Options: 'aml', 'kyc', 'sanctions', 'pep', 'fraude', 'reglementaire', 'autre'

    # Niveau de risque
    niveau_risque = db.Column(db.String(20), default='moyen')
    # Options: 'faible', 'moyen', 'eleve', 'critique'

    # Informations
    description = db.Column(db.Text, nullable=True)
    motifs = db.Column(db.Text, nullable=True)

    # Documents vérifiés
    documents_verifies = db.Column(db.Text, nullable=True)  # JSON ou liste séparée par virgules

    # Résultats
    conforme = db.Column(db.Boolean, default=False)
    resultat = db.Column(db.Text, nullable=True)
    recommandations = db.Column(db.Text, nullable=True)

    # Dates
    date_demande = db.Column(db.DateTime, default=datetime.utcnow)
    date_verification = db.Column(db.DateTime, nullable=True)
    date_validation = db.Column(db.DateTime, nullable=True)
    date_limite = db.Column(db.DateTime, nullable=True)

    # Statut
    statut = db.Column(db.String(500), default='en_attente')
    # Options: 'en_attente', 'en_cours', 'terminee', 'validee', 'rejetee', 'archivee'

    # Métadonnées
    priorite = db.Column(db.String(20), default='normale')
    # Options: 'basse', 'normale', 'haute', 'urgente'

    notes = db.Column(db.Text, nullable=True)
    commentaires = db.Column(db.Text, nullable=True)

    # Temps passé
    temps_verification = db.Column(db.Integer, nullable=True)  # en minutes

    # Dates système
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations inverses
    client = db.relationship('Client', backref='verifications_conformite', lazy=True)
    agent_conformite = db.relationship('User', foreign_keys=[agent_conformite_id], backref='verifications_agent',
                                       lazy=True)
    superviseur = db.relationship('User', foreign_keys=[superviseur_id], backref='verifications_superviseur', lazy=True)

    def __repr__(self):
        return f'<VerificationConformite {self.id} - {self.client.prenom} {self.client.nom} - {self.type_verification}>'

    @staticmethod
    def get_en_attente(agent_id, limit=None):
        """Récupère les vérifications en attente"""
        query = VerificationConformite.query.filter_by(
            agent_conformite_id=agent_id,
            statut='en_attente'
        ).order_by(
            VerificationConformite.priorite.desc(),
            VerificationConformite.niveau_risque.desc(),
            VerificationConformite.date_limite.asc()
        )
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_en_cours(agent_id, limit=None):
        """Récupère les vérifications en cours"""
        query = VerificationConformite.query.filter_by(
            agent_conformite_id=agent_id,
            statut='en_cours'
        ).order_by(VerificationConformite.date_modification.desc())
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_terminees(agent_id, limit=None):
        """Récupère les vérifications terminées"""
        query = VerificationConformite.query.filter_by(
            agent_conformite_id=agent_id,
            statut='terminee'
        ).order_by(VerificationConformite.date_verification.desc())
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_critiques(agent_id):
        """Récupère les vérifications critiques"""
        return VerificationConformite.query.filter(
            VerificationConformite.agent_conformite_id == agent_id,
            VerificationConformite.statut.in_(['en_attente', 'en_cours']),
            VerificationConformite.niveau_risque == 'critique'
        ).order_by(VerificationConformite.priorite.desc()).all()

    @staticmethod
    def get_statistiques(agent_id):
        """Statistiques des vérifications d'un agent"""
        total = VerificationConformite.query.filter_by(agent_conformite_id=agent_id).count()
        en_attente = VerificationConformite.query.filter_by(agent_conformite_id=agent_id, statut='en_attente').count()
        en_cours = VerificationConformite.query.filter_by(agent_conformite_id=agent_id, statut='en_cours').count()
        terminees = VerificationConformite.query.filter_by(agent_conformite_id=agent_id, statut='terminee').count()
        validees = VerificationConformite.query.filter_by(agent_conformite_id=agent_id, statut='validee').count()
        rejetees = VerificationConformite.query.filter_by(agent_conformite_id=agent_id, statut='rejetee').count()

        # Conformité
        conformes = VerificationConformite.query.filter_by(
            agent_conformite_id=agent_id,
            conforme=True
        ).count()
        taux_conformite = round((conformes / total * 100), 2) if total > 0 else 0

        # Répartition des risques
        risque_faible = VerificationConformite.query.filter_by(
            agent_conformite_id=agent_id,
            niveau_risque='faible'
        ).count()
        risque_moyen = VerificationConformite.query.filter_by(
            agent_conformite_id=agent_id,
            niveau_risque='moyen'
        ).count()
        risque_eleve = VerificationConformite.query.filter_by(
            agent_conformite_id=agent_id,
            niveau_risque='eleve'
        ).count()
        risque_critique = VerificationConformite.query.filter_by(
            agent_conformite_id=agent_id,
            niveau_risque='critique'
        ).count()

        return {
            'total': total,
            'en_attente': en_attente,
            'en_cours': en_cours,
            'terminees': terminees,
            'validees': validees,
            'rejetees': rejetees,
            'conformes': conformes,
            'taux_conformite': taux_conformite,
            'risque_faible': risque_faible,
            'risque_moyen': risque_moyen,
            'risque_eleve': risque_eleve,
            'risque_critique': risque_critique
        }

    @staticmethod
    def get_par_type(agent_id):
        """Récupère le nombre de vérifications par type"""
        types = ['aml', 'kyc', 'sanctions', 'pep', 'fraude', 'reglementaire', 'autre']
        result = {}
        for t in types:
            count = VerificationConformite.query.filter_by(
                agent_conformite_id=agent_id,
                type_verification=t
            ).count()
            result[t] = count
        return result

    def commencer_verification(self):
        """Démarre la vérification"""
        self.statut = 'en_cours'
        db.session.commit()

    def terminer_verification(self, conforme, resultat=None, recommandations=None, temps=None):
        """Termine la vérification"""
        self.statut = 'terminee'
        self.conforme = conforme
        self.date_verification = datetime.utcnow()
        if resultat:
            self.resultat = resultat
        if recommandations:
            self.recommandations = recommandations
        if temps:
            self.temps_verification = temps
        db.session.commit()

    def valider(self, superviseur_id, commentaires=None):
        """Valide la vérification"""
        self.statut = 'validee'
        self.superviseur_id = superviseur_id
        self.date_validation = datetime.utcnow()
        if commentaires:
            self.commentaires = commentaires
        db.session.commit()

    def rejeter(self, superviseur_id, commentaires=None):
        """Rejette la vérification"""
        self.statut = 'rejetee'
        self.superviseur_id = superviseur_id
        if commentaires:
            self.commentaires = commentaires
        db.session.commit()

    def to_dict(self):
        """Convertit la vérification en dictionnaire"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'client_nom': f"{self.client.prenom} {self.client.nom}" if self.client else None,
            'agent_conformite_id': self.agent_conformite_id,
            'agent_nom': f"{self.agent_conformite.prenom} {self.agent_conformite.nom}" if self.agent_conformite else None,
            'type_verification': self.type_verification,
            'niveau_risque': self.niveau_risque,
            'description': self.description,
            'motifs': self.motifs,
            'conforme': self.conforme,
            'resultat': self.resultat,
            'recommandations': self.recommandations,
            'date_demande': self.date_demande.isoformat(),
            'date_verification': self.date_verification.isoformat() if self.date_verification else None,
            'date_validation': self.date_validation.isoformat() if self.date_validation else None,
            'date_limite': self.date_limite.isoformat() if self.date_limite else None,
            'statut': self.statut,
            'priorite': self.priorite,
            'temps_verification': self.temps_verification,
            'notes': self.notes,
            'commentaires': self.commentaires
        }


# =============================================
# MODÈLE POUR LES ALERTES CONFORMITÉ
# =============================================

class AlerteConformite(db.Model):
    """Modèle pour les alertes de conformité"""

    __tablename__ = 'alertes_conformite'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    verification_id = db.Column(db.Integer, db.ForeignKey('verifications_conformite.id'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    agent_conformite_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Informations
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Niveau
    niveau = db.Column(db.String(20), default='moyen')
    # Options: 'faible', 'moyen', 'eleve', 'critique'

    # Type d'alerte
    type_alerte = db.Column(db.String(50), nullable=False)
    # Options: 'risque_aml', 'kyc_manquant', 'sanction', 'pep', 'transaction_suspecte', 'autre'

    # Statut
    statut = db.Column(db.String(20), default='active')
    # Options: 'active', 'en_cours', 'traitee', 'ignoree'

    # Dates
    date_alerte = db.Column(db.DateTime, default=datetime.utcnow)
    date_traitement = db.Column(db.DateTime, nullable=True)
    date_limite = db.Column(db.DateTime, nullable=True)

    # Métadonnées
    actions_recommandees = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    # Relations inverses
    verification = db.relationship('VerificationConformite', backref='alertes', lazy=True)
    client = db.relationship('Client', backref='alertes_conformite', lazy=True)
    agent_conformite = db.relationship('User', foreign_keys=[agent_conformite_id], backref='alertes_agent', lazy=True)

    def __repr__(self):
        return f'<AlerteConformite {self.id} - {self.titre} - {self.niveau}>'

    def traiter(self):
        """Marque l'alerte comme traitée"""
        self.statut = 'traitee'
        self.date_traitement = datetime.utcnow()
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'description': self.description,
            'niveau': self.niveau,
            'type_alerte': self.type_alerte,
            'statut': self.statut,
            'date_alerte': self.date_alerte.isoformat(),
            'date_traitement': self.date_traitement.isoformat() if self.date_traitement else None,
            'date_limite': self.date_limite.isoformat() if self.date_limite else None
        }


# =============================================
# CONSTANTES POUR LA CONFORMITÉ
# =============================================

TYPES_VERIFICATION = {
    'aml': 'Anti-blanchiment (AML)',
    'kyc': 'Know Your Customer (KYC)',
    'sanctions': 'Sanctions internationales',
    'pep': 'Personnes Politiquement Exposées (PEP)',
    'fraude': 'Détection de fraude',
    'reglementaire': 'Conformité réglementaire',
    'autre': 'Autre'
}

NIVEAUX_RISQUE = {
    'faible': 'Faible',
    'moyen': 'Moyen',
    'eleve': 'Élevé',
    'critique': 'Critique'
}

STATUTS_VERIFICATION = {
    'en_attente': 'En attente',
    'en_cours': 'En cours',
    'terminee': 'Terminée',
    'validee': 'Validée',
    'rejetee': 'Rejetée',
    'archivee': 'Archivée'
}

PRIORITES_VERIFICATION = {
    'basse': 'Basse',
    'normale': 'Normale',
    'haute': 'Haute',
    'urgente': 'Urgente'
}

TYPES_ALERTE = {
    'risque_aml': 'Risque AML détecté',
    'kyc_manquant': 'KYC manquant',
    'sanction': 'Correspondance avec liste de sanctions',
    'pep': 'Personne Politiquement Exposée',
    'transaction_suspecte': 'Transaction suspecte',
    'autre': 'Autre'
}

NIVEAUX_ALERTE = {
    'faible': 'Faible',
    'moyen': 'Moyen',
    'eleve': 'Élevé',
    'critique': 'Critique'
}

STATUTS_ALERTE = {
    'active': 'Active',
    'en_cours': 'En cours de traitement',
    'traitee': 'Traitée',
    'ignoree': 'Ignorée'
}


# =============================================
# MODÈLE POUR LES RISQUES
# =============================================

class Risque(db.Model):
    """Modèle pour les risques"""

    __tablename__ = 'risques'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    agent_risque_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)


    # Informations
    nom = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    categorie = db.Column(db.String(50), nullable=False)
    # Options: 'credit', 'operationnel', 'marche', 'juridique', 'conformite', 'strategique', 'autre'

    # Type de risque
    type_risque = db.Column(db.String(50), nullable=False)
    # Options: 'interne', 'externe', 'systemique', 'individuel', 'collectif'

    # Évaluation
    probabilite = db.Column(db.Integer, default=3)  # 1-5
    impact = db.Column(db.Integer, default=3)  # 1-5
    score = db.Column(db.Integer, default=9)  # probabilite * impact

    # Niveau de risque
    niveau = db.Column(db.String(20), default='moyen')
    # Options: 'faible', 'moyen', 'eleve', 'critique'

    # Détection
    date_detection = db.Column(db.DateTime, default=datetime.utcnow)
    detecte_par = db.Column(db.String(100), nullable=True)
    methode_detection = db.Column(db.String(100), nullable=True)

    # Traitement
    date_traitement = db.Column(db.DateTime, nullable=True)
    plan_atténuation = db.Column(db.Text, nullable=True)
    mesures_correctives = db.Column(db.Text, nullable=True)

    # Suivi
    responsable = db.Column(db.String(100), nullable=True)
    date_echeance = db.Column(db.DateTime, nullable=True)

    # Statut
    statut = db.Column(db.String(20), default='actif')
    # Options: 'actif', 'en_cours', 'maitrise', 'atténue', 'termine', 'archive'

    # Métadonnées
    priorite = db.Column(db.String(20), default='normale')
    notes = db.Column(db.Text, nullable=True)

    # Dates système
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations inverses
    agent_risque = db.relationship('User', foreign_keys=[agent_risque_id], backref='risques_agent', lazy=True)
    client = db.relationship('Client', backref='risques', lazy=True)


    def __repr__(self):
        return f'<Risque {self.id} - {self.nom} - {self.niveau}>'

    def calculer_score(self):
        """Calcule le score du risque (probabilite * impact)"""
        self.score = self.probabilite * self.impact
        self._determiner_niveau()
        return self.score

    def _determiner_niveau(self):
        """Détermine le niveau de risque basé sur le score"""
        if self.score >= 20:
            self.niveau = 'critique'
        elif self.score >= 15:
            self.niveau = 'eleve'
        elif self.score >= 8:
            self.niveau = 'moyen'
        else:
            self.niveau = 'faible'

    @staticmethod
    def get_actifs(agent_id, limit=None):
        """Récupère les risques actifs"""
        query = Risque.query.filter_by(
            agent_risque_id=agent_id,
            statut='actif'
        ).order_by(Risque.score.desc())
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_critiques(agent_id):
        """Récupère les risques critiques"""
        return Risque.query.filter_by(
            agent_risque_id=agent_id,
            niveau='critique',
            statut='actif'
        ).order_by(Risque.score.desc()).all()

    @staticmethod
    def get_statistiques(agent_id):
        """Statistiques des risques"""
        total = Risque.query.filter_by(agent_risque_id=agent_id).count()
        actifs = Risque.query.filter_by(agent_risque_id=agent_id, statut='actif').count()
        en_cours = Risque.query.filter_by(agent_risque_id=agent_id, statut='en_cours').count()
        maitrises = Risque.query.filter_by(agent_risque_id=agent_id, statut='maitrise').count()
        attenues = Risque.query.filter_by(agent_risque_id=agent_id, statut='atténue').count()
        termines = Risque.query.filter_by(agent_risque_id=agent_id, statut='termine').count()

        # Niveaux
        faible = Risque.query.filter_by(agent_risque_id=agent_id, niveau='faible').count()
        moyen = Risque.query.filter_by(agent_risque_id=agent_id, niveau='moyen').count()
        eleve = Risque.query.filter_by(agent_risque_id=agent_id, niveau='eleve').count()
        critique = Risque.query.filter_by(agent_risque_id=agent_id, niveau='critique').count()

        # Score moyen
        scores = db.session.query(db.func.avg(Risque.score)).filter_by(agent_risque_id=agent_id).scalar() or 0

        return {
            'total': total,
            'actifs': actifs,
            'en_cours': en_cours,
            'maitrises': maitrises,
            'attenues': attenues,
            'termines': termines,
            'faible': faible,
            'moyen': moyen,
            'eleve': eleve,
            'critique': critique,
            'score_moyen': round(scores, 2)
        }

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'categorie': self.categorie,
            'type_risque': self.type_risque,
            'probabilite': self.probabilite,
            'impact': self.impact,
            'score': self.score,
            'niveau': self.niveau,
            'date_detection': self.date_detection.isoformat(),
            'plan_atténuation': self.plan_atténuation,
            'statut': self.statut,
            'priorite': self.priorite
        }


# =============================================
# MODÈLE POUR LES ÉVALUATIONS DE RISQUES
# =============================================

class EvaluationRisque(db.Model):
    """Modèle pour les évaluations de risques"""

    __tablename__ = 'evaluations_risques'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    risque_id = db.Column(db.Integer, db.ForeignKey('risques.id'), nullable=False)
    agent_risque_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    evaluateur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Évaluation
    probabilite_evaluee = db.Column(db.Integer, nullable=True)  # 1-5
    impact_evalue = db.Column(db.Integer, nullable=True)  # 1-5
    score_evalue = db.Column(db.Integer, nullable=True)
    niveau_evalue = db.Column(db.String(20), nullable=True)

    # Facteurs de risque
    facteurs = db.Column(db.Text, nullable=True)
    vulnerabilites = db.Column(db.Text, nullable=True)
    capacites_controle = db.Column(db.Text, nullable=True)

    # Résultats
    resultat = db.Column(db.Text, nullable=True)
    recommandations = db.Column(db.Text, nullable=True)

    # Dates
    date_evaluation = db.Column(db.DateTime, default=datetime.utcnow)
    date_prochaine_evaluation = db.Column(db.DateTime, nullable=True)

    # Statut
    statut = db.Column(db.String(20), default='en_cours')
    # Options: 'en_cours', 'terminee', 'validee', 'annulee'

    # Métadonnées
    notes = db.Column(db.Text, nullable=True)

    # Dates système
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations inverses
    risque = db.relationship('Risque', backref='evaluations', lazy=True)
    agent_risque = db.relationship('User', foreign_keys=[agent_risque_id], backref='evaluations_agent', lazy=True)
    evaluateur = db.relationship('User', foreign_keys=[evaluateur_id], backref='evaluations_effectuees', lazy=True)

    def __repr__(self):
        return f'<EvaluationRisque {self.id} - Risque {self.risque_id}>'

    def calculer_score(self):
        """Calcule le score évalué"""
        if self.probabilite_evaluee and self.impact_evalue:
            self.score_evalue = self.probabilite_evaluee * self.impact_evalue
            self._determiner_niveau()
        return self.score_evalue

    def _determiner_niveau(self):
        """Détermine le niveau basé sur le score"""
        if self.score_evalue >= 20:
            self.niveau_evalue = 'critique'
        elif self.score_evalue >= 15:
            self.niveau_evalue = 'eleve'
        elif self.score_evalue >= 8:
            self.niveau_evalue = 'moyen'
        else:
            self.niveau_evalue = 'faible'

    def terminer(self):
        """Termine l'évaluation"""
        self.statut = 'terminee'
        self.date_evaluation = datetime.utcnow()
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'risque_id': self.risque_id,
            'risque_nom': self.risque.nom if self.risque else None,
            'probabilite_evaluee': self.probabilite_evaluee,
            'impact_evalue': self.impact_evalue,
            'score_evalue': self.score_evalue,
            'niveau_evalue': self.niveau_evalue,
            'resultat': self.resultat,
            'recommandations': self.recommandations,
            'date_evaluation': self.date_evaluation.isoformat(),
            'statut': self.statut
        }


# =============================================
# MODÈLE POUR LES CONTRÔLES
# =============================================

class Controle(db.Model):
    """Modèle pour les contrôles internes"""

    __tablename__ = 'controles'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    controleur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    superviseur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Informations
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    objet = db.Column(db.String(200), nullable=False)

    # Type de contrôle
    type_controle = db.Column(db.String(50), nullable=False)
    # Options: 'financier', 'operationnel', 'conformite', 'rh', 'it', 'qualite', 'autre'

    # Priorité
    priorite = db.Column(db.String(20), default='normale')
    # Options: 'basse', 'normale', 'haute', 'urgente'

    # Dates
    date_debut = db.Column(db.DateTime, nullable=False)
    date_fin = db.Column(db.DateTime, nullable=True)
    date_limite = db.Column(db.DateTime, nullable=False)
    date_controle = db.Column(db.DateTime, nullable=True)

    # Résultats
    conforme = db.Column(db.Boolean, default=False)
    resultat = db.Column(db.Text, nullable=True)
    constats = db.Column(db.Text, nullable=True)
    recommandations = db.Column(db.Text, nullable=True)

    # Statut
    statut = db.Column(db.String(20), default='planifie')
    # Options: 'planifie', 'en_cours', 'effectue', 'valide', 'rejete', 'annule'

    # Métadonnées
    equipe = db.Column(db.String(200), nullable=True)
    methode = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    # Dates système
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations inverses
    controleur = db.relationship('User', foreign_keys=[controleur_id], backref='controles_effectues', lazy=True)
    superviseur = db.relationship('User', foreign_keys=[superviseur_id], backref='controles_supervises', lazy=True)
    non_conformites = db.relationship('NonConformite', backref='controle', lazy=True)

    def __repr__(self):
        return f'<Controle {self.id} - {self.titre} - {self.statut}>'

    @staticmethod
    def get_a_realiser(controleur_id, limit=None):
        """Récupère les contrôles à réaliser"""
        query = Controle.query.filter_by(
            controleur_id=controleur_id,
            statut='planifie'
        ).order_by(Controle.priorite.desc(), Controle.date_limite.asc())
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_en_cours(controleur_id, limit=None):
        """Récupère les contrôles en cours"""
        query = Controle.query.filter_by(
            controleur_id=controleur_id,
            statut='en_cours'
        ).order_by(Controle.date_modification.desc())
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_statistiques(controleur_id):
        """Statistiques des contrôles"""
        total = Controle.query.filter_by(controleur_id=controleur_id).count()
        planifies = Controle.query.filter_by(controleur_id=controleur_id, statut='planifie').count()
        en_cours = Controle.query.filter_by(controleur_id=controleur_id, statut='en_cours').count()
        effectues = Controle.query.filter_by(controleur_id=controleur_id, statut='effectue').count()
        valides = Controle.query.filter_by(controleur_id=controleur_id, statut='valide').count()
        rejetes = Controle.query.filter_by(controleur_id=controleur_id, statut='rejete').count()

        # Taux de conformité
        conformes = Controle.query.filter_by(controleur_id=controleur_id, conforme=True).count()
        taux_conformite = round((conformes / total * 100), 2) if total > 0 else 0

        return {
            'total': total,
            'planifies': planifies,
            'en_cours': en_cours,
            'effectues': effectues,
            'valides': valides,
            'rejetes': rejetes,
            'conformes': conformes,
            'taux_conformite': taux_conformite
        }

    def commencer(self):
        """Démarre le contrôle"""
        self.statut = 'en_cours'
        self.date_debut = datetime.utcnow()
        db.session.commit()

    def terminer(self, conforme, resultat=None, constats=None, recommandations=None):
        """Termine le contrôle"""
        self.statut = 'effectue'
        self.conforme = conforme
        self.date_controle = datetime.utcnow()
        if resultat:
            self.resultat = resultat
        if constats:
            self.constats = constats
        if recommandations:
            self.recommandations = recommandations
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'description': self.description,
            'objet': self.objet,
            'type_controle': self.type_controle,
            'priorite': self.priorite,
            'date_debut': self.date_debut.isoformat(),
            'date_limite': self.date_limite.isoformat(),
            'date_controle': self.date_controle.isoformat() if self.date_controle else None,
            'conforme': self.conforme,
            'resultat': self.resultat,
            'statut': self.statut
        }


# =============================================
# MODÈLE POUR LES NON-CONFORMITÉS
# =============================================

class NonConformite(db.Model):
    """Modèle pour les non-conformités"""

    __tablename__ = 'non_conformites'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    controle_id = db.Column(db.Integer, db.ForeignKey('controles.id'), nullable=True)
    controleur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    responsable_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Informations
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cause = db.Column(db.Text, nullable=True)

    # Type
    type_non_conformite = db.Column(db.String(50), nullable=False)
    # Options: 'critique', 'majeure', 'mineure', 'observation'

    # Gravité
    gravite = db.Column(db.String(20), default='moyenne')
    # Options: 'faible', 'moyenne', 'elevee', 'critique'

    # Dates
    date_decouverte = db.Column(db.DateTime, default=datetime.utcnow)
    date_correction = db.Column(db.DateTime, nullable=True)
    date_verification = db.Column(db.DateTime, nullable=True)
    date_echeance = db.Column(db.DateTime, nullable=True)

    # Statut
    statut = db.Column(db.String(20), default='ouverte')
    # Options: 'ouverte', 'en_cours', 'corrigee', 'verifiee', 'fermee', 'ignoree'

    # Actions
    actions_correctives = db.Column(db.Text, nullable=True)
    actions_preventives = db.Column(db.Text, nullable=True)
    commentaires = db.Column(db.Text, nullable=True)

    # Métadonnées
    priorite = db.Column(db.String(20), default='normale')
    notes = db.Column(db.Text, nullable=True)

    # Dates système
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations inverses
    controleur = db.relationship('User', foreign_keys=[controleur_id], backref='non_conformites_decouvertes', lazy=True)
    responsable = db.relationship('User', foreign_keys=[responsable_id], backref='non_conformites_responsables',
                                  lazy=True)

    def __repr__(self):
        return f'<NonConformite {self.id} - {self.titre} - {self.gravite}>'

    @staticmethod
    def get_ouvertes(controleur_id, limit=None):
        """Récupère les non-conformités ouvertes"""
        query = NonConformite.query.filter(
            NonConformite.controleur_id == controleur_id,
            NonConformite.statut.in_(['ouverte', 'en_cours'])
        ).order_by(NonConformite.gravite.desc(), NonConformite.date_echeance.asc())
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_critiques(controleur_id):
        """Récupère les non-conformités critiques"""
        return NonConformite.query.filter(
            NonConformite.controleur_id == controleur_id,
            NonConformite.gravite.in_(['elevee', 'critique']),
            NonConformite.statut.in_(['ouverte', 'en_cours'])
        ).order_by(NonConformite.gravite.desc()).all()

    @staticmethod
    def get_statistiques(controleur_id):
        """Statistiques des non-conformités"""
        total = NonConformite.query.filter_by(controleur_id=controleur_id).count()
        ouvertes = NonConformite.query.filter_by(controleur_id=controleur_id, statut='ouverte').count()
        en_cours = NonConformite.query.filter_by(controleur_id=controleur_id, statut='en_cours').count()
        corrigees = NonConformite.query.filter_by(controleur_id=controleur_id, statut='corrigee').count()
        verifiees = NonConformite.query.filter_by(controleur_id=controleur_id, statut='verifiee').count()
        fermees = NonConformite.query.filter_by(controleur_id=controleur_id, statut='fermee').count()

        # Par gravité
        faible = NonConformite.query.filter_by(controleur_id=controleur_id, gravite='faible').count()
        moyenne = NonConformite.query.filter_by(controleur_id=controleur_id, gravite='moyenne').count()
        elevee = NonConformite.query.filter_by(controleur_id=controleur_id, gravite='elevee').count()
        critique = NonConformite.query.filter_by(controleur_id=controleur_id, gravite='critique').count()

        # Taux de correction
        corrigees_fermees = corrigees + verifiees + fermees
        taux_correction = round((corrigees_fermees / total * 100), 2) if total > 0 else 0

        return {
            'total': total,
            'ouvertes': ouvertes,
            'en_cours': en_cours,
            'corrigees': corrigees,
            'verifiees': verifiees,
            'fermees': fermees,
            'faible': faible,
            'moyenne': moyenne,
            'elevee': elevee,
            'critique': critique,
            'taux_correction': taux_correction
        }

    def corriger(self, actions_correctives=None):
        """Marque comme corrigée"""
        self.statut = 'corrigee'
        self.date_correction = datetime.utcnow()
        if actions_correctives:
            self.actions_correctives = actions_correctives
        db.session.commit()

    def verifier(self):
        """Marque comme vérifiée"""
        self.statut = 'verifiee'
        self.date_verification = datetime.utcnow()
        db.session.commit()

    def fermer(self):
        """Ferme la non-conformité"""
        self.statut = 'fermee'
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'description': self.description,
            'cause': self.cause,
            'type_non_conformite': self.type_non_conformite,
            'gravite': self.gravite,
            'date_decouverte': self.date_decouverte.isoformat(),
            'date_correction': self.date_correction.isoformat() if self.date_correction else None,
            'date_echeance': self.date_echeance.isoformat() if self.date_echeance else None,
            'statut': self.statut,
            'actions_correctives': self.actions_correctives,
            'priorite': self.priorite,
            'controle_id': self.controle_id
        }


# =============================================
# CONSTANTES
# =============================================

CATEGORIES_RISQUE = {
    'credit': 'Risque de crédit',
    'operationnel': 'Risque opérationnel',
    'marche': 'Risque de marché',
    'juridique': 'Risque juridique',
    'conformite': 'Risque de conformité',
    'strategique': 'Risque stratégique',
    'autre': 'Autre'
}

TYPES_RISQUE = {
    'interne': 'Interne',
    'externe': 'Externe',
    'systemique': 'Systémique',
    'individuel': 'Individuel',
    'collectif': 'Collectif'
}

NIVEAUX_RISQUE_GLOBAL = {
    'faible': 'Faible (1-8)',
    'moyen': 'Moyen (9-15)',
    'eleve': 'Élevé (16-19)',
    'critique': 'Critique (20-25)'
}

STATUTS_RISQUE = {
    'actif': 'Actif',
    'en_cours': 'En cours de traitement',
    'maitrise': 'Maîtrisé',
    'atténue': 'Atténué',
    'termine': 'Terminé',
    'archive': 'Archivé'
}

TYPES_CONTROLE = {
    'financier': 'Contrôle financier',
    'operationnel': 'Contrôle opérationnel',
    'conformite': 'Contrôle de conformité',
    'rh': 'Contrôle RH',
    'it': 'Contrôle IT',
    'qualite': 'Contrôle qualité',
    'autre': 'Autre'
}

STATUTS_CONTROLE = {
    'planifie': 'Planifié',
    'en_cours': 'En cours',
    'effectue': 'Effectué',
    'valide': 'Validé',
    'rejete': 'Rejeté',
    'annule': 'Annulé'
}

TYPES_NON_CONFORMITE = {
    'critique': 'Non-conformité critique',
    'majeure': 'Non-conformité majeure',
    'mineure': 'Non-conformité mineure',
    'observation': 'Observation'
}

GRAVITES_NON_CONFORMITE = {
    'faible': 'Faible',
    'moyenne': 'Moyenne',
    'elevee': 'Élevée',
    'critique': 'Critique'
}

STATUTS_NON_CONFORMITE = {
    'ouverte': 'Ouverte',
    'en_cours': 'En cours de correction',
    'corrigee': 'Corrigée',
    'verifiee': 'Vérifiée',
    'fermee': 'Fermée',
    'ignoree': 'Ignorée'
}


# =============================================
# MODÈLE POUR LES RENDEZ-VOUS
# =============================================

class RendezVous(db.Model):
    """Modèle pour les rendez-vous"""

    __tablename__ = 'rendez_vous'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    secretaire_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # L'agent concerné
    lieu_id = db.Column(db.Integer, db.ForeignKey('lieux.id'), nullable=True)

    # Informations
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    objectif = db.Column(db.Text, nullable=True)

    # Dates et heures
    date_debut = db.Column(db.DateTime, nullable=False)
    date_fin = db.Column(db.DateTime, nullable=True)
    duree = db.Column(db.Integer, default=30)  # Durée en minutes

    # Lieu
    lieu = db.Column(db.String(200), nullable=True)
    adresse = db.Column(db.String(300), nullable=True)
    notes_lieu = db.Column(db.Text, nullable=True)

    # Participants
    participants = db.Column(db.Text, nullable=True)  # JSON ou liste séparée par virgules
    nb_participants = db.Column(db.Integer, default=1)

    # Statut
    statut = db.Column(db.String(20), default='planifie')
    # Options: 'planifie', 'confirme', 'en_cours', 'termine', 'annule', 'reporte'

    # Résultats
    resultat = db.Column(db.Text, nullable=True)
    compte_rendu = db.Column(db.Text, nullable=True)
    notes_suivi = db.Column(db.Text, nullable=True)

    # Métadonnées
    priorite = db.Column(db.String(20), default='normale')
    # Options: 'basse', 'normale', 'haute', 'urgente'

    type_rendez_vous = db.Column(db.String(50), default='physique')
    # Options: 'physique', 'telephonique', 'visioconference', 'terrain'

    # Rappels
    rappel_envoye = db.Column(db.Boolean, default=False)
    date_rappel = db.Column(db.DateTime, nullable=True)
    rappel_commentaire = db.Column(db.Text, nullable=True)

    # Dates système
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations inverses
    client = db.relationship('Client', backref='rendez_vous', lazy=True)
    secretaire = db.relationship('User', foreign_keys=[secretaire_id], backref='rendez_vous_secretaires', lazy=True)
    agent = db.relationship('User', foreign_keys=[agent_id], backref='rendez_vous_agents', lazy=True)
    lieu = db.relationship('Lieu', backref='rendez_vous', lazy=True)

    def __repr__(self):
        return f'<RendezVous {self.id} - {self.client.prenom} {self.client.nom} - {self.date_debut.strftime("%d/%m/%Y %H:%M")}>'

    @staticmethod
    def get_aujourdhui(secretaire_id):
        """Récupère les rendez-vous du jour"""
        today = datetime.utcnow().date()
        return RendezVous.query.filter(
            RendezVous.secretaire_id == secretaire_id,
            func.date(RendezVous.date_debut) == today
        ).order_by(RendezVous.date_debut.asc()).all()

    @staticmethod
    def get_a_venir(secretaire_id, limit=None):
        """Récupère les rendez-vous à venir"""
        query = RendezVous.query.filter(
            RendezVous.secretaire_id == secretaire_id,
            RendezVous.date_debut >= datetime.utcnow(),
            RendezVous.statut.in_(['planifie', 'confirme'])
        ).order_by(RendezVous.date_debut.asc())
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_passes(secretaire_id, limit=None):
        """Récupère les rendez-vous passés"""
        query = RendezVous.query.filter(
            RendezVous.secretaire_id == secretaire_id,
            RendezVous.date_debut < datetime.utcnow(),
            RendezVous.statut.in_(['termine', 'annule', 'reporte'])
        ).order_by(RendezVous.date_debut.desc())
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_par_client(client_id, limit=None):
        """Récupère les rendez-vous d'un client"""
        query = RendezVous.query.filter_by(client_id=client_id).order_by(
            RendezVous.date_debut.desc()
        )
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_statistiques(secretaire_id, date_debut=None, date_fin=None):
        """Statistiques des rendez-vous"""
        query = RendezVous.query.filter_by(secretaire_id=secretaire_id)

        if date_debut:
            query = query.filter(RendezVous.date_debut >= date_debut)
        if date_fin:
            query = query.filter(RendezVous.date_debut <= date_fin)

        rendez_vous = query.all()
        total = len(rendez_vous)

        # Par statut
        planifies = len([r for r in rendez_vous if r.statut == 'planifie'])
        confirmes = len([r for r in rendez_vous if r.statut == 'confirme'])
        en_cours = len([r for r in rendez_vous if r.statut == 'en_cours'])
        termines = len([r for r in rendez_vous if r.statut == 'termine'])
        annules = len([r for r in rendez_vous if r.statut == 'annule'])
        reportes = len([r for r in rendez_vous if r.statut == 'reporte'])

        # Par type
        physiques = len([r for r in rendez_vous if r.type_rendez_vous == 'physique'])
        telephoniques = len([r for r in rendez_vous if r.type_rendez_vous == 'telephonique'])
        visios = len([r for r in rendez_vous if r.type_rendez_vous == 'visioconference'])
        terrains = len([r for r in rendez_vous if r.type_rendez_vous == 'terrain'])

        # Taux de réalisation
        realises = termines
        taux_realisation = round((realises / total * 100), 2) if total > 0 else 0

        # Durée moyenne
        durees = [r.duree for r in rendez_vous if r.duree]
        duree_moyenne = round(sum(durees) / len(durees), 2) if durees else 0

        return {
            'total': total,
            'planifies': planifies,
            'confirmes': confirmes,
            'en_cours': en_cours,
            'termines': termines,
            'annules': annules,
            'reportes': reportes,
            'physiques': physiques,
            'telephoniques': telephoniques,
            'visios': visios,
            'terrains': terrains,
            'taux_realisation': taux_realisation,
            'duree_moyenne': duree_moyenne
        }

    def confirmer(self):
        """Confirme le rendez-vous"""
        self.statut = 'confirme'
        db.session.commit()

    def commencer(self):
        """Démarre le rendez-vous"""
        self.statut = 'en_cours'
        db.session.commit()

    def terminer(self, resultat=None, compte_rendu=None):
        """Termine le rendez-vous"""
        self.statut = 'termine'
        if resultat:
            self.resultat = resultat
        if compte_rendu:
            self.compte_rendu = compte_rendu
        db.session.commit()

    def annuler(self, notes=None):
        """Annule le rendez-vous"""
        self.statut = 'annule'
        if notes:
            self.notes_suivi = notes
        db.session.commit()

    def reporter(self, nouvelle_date, notes=None):
        """Reporte le rendez-vous"""
        self.statut = 'reporte'
        self.date_debut = nouvelle_date
        if notes:
            self.notes_suivi = notes
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'client_nom': f"{self.client.prenom} {self.client.nom}" if self.client else None,
            'client_telephone': self.client.telephone if self.client else None,
            'secretaire_id': self.secretaire_id,
            'agent_id': self.agent_id,
            'agent_nom': f"{self.agent.prenom} {self.agent.nom}" if self.agent else None,
            'titre': self.titre,
            'description': self.description,
            'objectif': self.objectif,
            'date_debut': self.date_debut.isoformat(),
            'date_fin': self.date_fin.isoformat() if self.date_fin else None,
            'duree': self.duree,
            'lieu': self.lieu,
            'adresse': self.adresse,
            'statut': self.statut,
            'type_rendez_vous': self.type_rendez_vous,
            'priorite': self.priorite,
            'resultat': self.resultat,
            'compte_rendu': self.compte_rendu
        }


# =============================================
# MODÈLE POUR LES DOCUMENTS ARCHIVÉS
# =============================================

class DocumentArchive(db.Model):
    """Modèle pour les documents archivés"""

    __tablename__ = 'documents_archives'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    archiviste_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    dossier_id = db.Column(db.Integer, db.ForeignKey('dossiers.id'), nullable=True)

    # Informations
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Catégorie et type
    categorie = db.Column(db.String(50), nullable=False)
    # Options: 'contrat', 'facture', 'identite', 'justificatif', 'comptable', 'rh', 'autre'

    type_document = db.Column(db.String(20), nullable=False)
    # Options: 'pdf', 'word', 'excel', 'image', 'scan', 'autre'

    # Fichier
    nom_fichier = db.Column(db.String(255), nullable=False)
    chemin_fichier = db.Column(db.String(500), nullable=False)
    taille_fichier = db.Column(db.Integer, nullable=True)  # En octets

    # Métadonnées
    mots_cles = db.Column(db.String(500), nullable=True)
    version = db.Column(db.String(20), default='1.0')

    # Dates
    date_creation = db.Column(db.DateTime, nullable=False)
    date_archivage = db.Column(db.DateTime, default=datetime.utcnow)
    date_expiration = db.Column(db.DateTime, nullable=True)
    date_dernier_acces = db.Column(db.DateTime, nullable=True)

    # Statut
    statut = db.Column(db.String(20), default='actif')
    # Options: 'actif', 'archive', 'expire', 'supprime'

    # Métadonnées
    confidentialite = db.Column(db.String(20), default='normal')
    # Options: 'public', 'normal', 'confidentiel', 'tres_confidentiel'

    notes = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(500), nullable=True)

    # Relations inverses
    archiviste = db.relationship('User', foreign_keys=[archiviste_id], backref='documents_archives', lazy=True)
    client = db.relationship('Client', backref='documents_archives', lazy=True)
    dossier = db.relationship('Dossier', backref='documents_archives', lazy=True)

    def __repr__(self):
        return f'<DocumentArchive {self.id} - {self.titre} - {self.categorie}>'

    @staticmethod
    def get_par_categorie(archiviste_id, categorie, limit=None):
        """Récupère les documents par catégorie"""
        query = DocumentArchive.query.filter_by(
            archiviste_id=archiviste_id,
            categorie=categorie,
            statut='actif'
        ).order_by(DocumentArchive.date_archivage.desc())
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_recherche(archiviste_id, query_string):
        """Recherche des documents"""
        return DocumentArchive.query.filter(
            DocumentArchive.archiviste_id == archiviste_id,
            DocumentArchive.statut == 'actif',
            db.or_(
                DocumentArchive.titre.ilike(f'%{query_string}%'),
                DocumentArchive.description.ilike(f'%{query_string}%'),
                DocumentArchive.mots_cles.ilike(f'%{query_string}%'),
                DocumentArchive.tags.ilike(f'%{query_string}%')
            )
        ).order_by(DocumentArchive.date_archivage.desc()).all()

    @staticmethod
    def get_recents(archiviste_id, limit=10):
        """Récupère les documents récemment archivés"""
        return DocumentArchive.query.filter_by(
            archiviste_id=archiviste_id,
            statut='actif'
        ).order_by(DocumentArchive.date_archivage.desc()).limit(limit).all()

    @staticmethod
    def get_statistiques(archiviste_id):
        """Statistiques des documents archivés"""
        total = DocumentArchive.query.filter_by(
            archiviste_id=archiviste_id,
            statut='actif'
        ).count()

        # Par catégorie
        categories = {}
        for cat in ['contrat', 'facture', 'identite', 'justificatif', 'comptable', 'rh', 'autre']:
            count = DocumentArchive.query.filter_by(
                archiviste_id=archiviste_id,
                categorie=cat,
                statut='actif'
            ).count()
            categories[cat] = count

        # Taille totale
        taille_totale = db.session.query(db.func.sum(DocumentArchive.taille_fichier)).filter(
            DocumentArchive.archiviste_id == archiviste_id,
            DocumentArchive.statut == 'actif'
        ).scalar() or 0

        # Par type
        types = {}
        for t in ['pdf', 'word', 'excel', 'image', 'scan', 'autre']:
            count = DocumentArchive.query.filter_by(
                archiviste_id=archiviste_id,
                type_document=t,
                statut='actif'
            ).count()
            types[t] = count

        return {
            'total': total,
            'categories': categories,
            'types': types,
            'taille_totale': taille_totale,
            'taille_totale_mb': round(taille_totale / (1024 * 1024), 2) if taille_totale > 0 else 0
        }

    def enregistrer_acces(self):
        """Enregistre un accès au document"""
        self.date_dernier_acces = datetime.utcnow()
        db.session.commit()

    def archiver(self):
        """Marque le document comme archivé"""
        self.statut = 'archive'
        db.session.commit()

    def supprimer(self):
        """Supprime le document (logique)"""
        self.statut = 'supprime'
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'description': self.description,
            'categorie': self.categorie,
            'type_document': self.type_document,
            'nom_fichier': self.nom_fichier,
            'chemin_fichier': self.chemin_fichier,
            'taille_fichier': self.taille_fichier,
            'mots_cles': self.mots_cles,
            'version': self.version,
            'date_creation': self.date_creation.isoformat(),
            'date_archivage': self.date_archivage.isoformat(),
            'date_expiration': self.date_expiration.isoformat() if self.date_expiration else None,
            'statut': self.statut,
            'confidentialite': self.confidentialite,
            'tags': self.tags
        }


# =============================================
# MODÈLE POUR LES LIEUX (pour les rendez-vous)
# =============================================

class Lieu(db.Model):
    """Modèle pour les lieux"""

    __tablename__ = 'lieux'

    id = db.Column(db.Integer, primary_key=True)

    nom = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(300), nullable=False)
    complement = db.Column(db.String(200), nullable=True)

    # Coordonnées
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # Contact
    telephone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    site_web = db.Column(db.String(200), nullable=True)

    # Capacité
    capacite_max = db.Column(db.Integer, nullable=True)
    nb_salles = db.Column(db.Integer, default=0)

    # Métadonnées
    type_lieu = db.Column(db.String(50), default='bureau')
    # Options: 'bureau', 'agence', 'externe', 'domicile', 'autre'

    description = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    # Statut
    statut = db.Column(db.String(20), default='actif')

    # Dates système
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Lieu {self.id} - {self.nom}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'adresse': self.adresse,
            'complement': self.complement,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'telephone': self.telephone,
            'email': self.email,
            'type_lieu': self.type_lieu,
            'capacite_max': self.capacite_max,
            'description': self.description,
            'statut': self.statut
        }


# =============================================
# CONSTANTES
# =============================================

STATUTS_RENDEZ_VOUS = {
    'planifie': 'Planifié',
    'confirme': 'Confirmé',
    'en_cours': 'En cours',
    'termine': 'Terminé',
    'annule': 'Annulé',
    'reporte': 'Reporté'
}

TYPES_RENDEZ_VOUS = {
    'physique': 'Physique',
    'telephonique': 'Téléphonique',
    'visioconference': 'Visioconférence',
    'terrain': 'Terrain'
}

PRIORITES_RENDEZ_VOUS = {
    'basse': 'Basse',
    'normale': 'Normale',
    'haute': 'Haute',
    'urgente': 'Urgente'
}

CATEGORIES_DOCUMENT = {
    'contrat': 'Contrat',
    'facture': 'Facture',
    'identite': 'Document d\'identité',
    'justificatif': 'Justificatif',
    'comptable': 'Document comptable',
    'rh': 'Document RH',
    'autre': 'Autre'
}

TYPES_DOCUMENT_ARCHIVE = {
    'pdf': 'PDF',
    'word': 'Word',
    'excel': 'Excel',
    'image': 'Image',
    'scan': 'Scan',
    'autre': 'Autre'
}

CONFIDENTIALITE_DOCUMENT = {
    'public': 'Public',
    'normal': 'Normal',
    'confidentiel': 'Confidentiel',
    'tres_confidentiel': 'Très confidentiel'
}

STATUTS_DOCUMENT_ARCHIVE = {
    'actif': 'Actif',
    'archive': 'Archivé',
    'expire': 'Expiré',
    'supprime': 'Supprimé'
}

STATUTS_LIEU = {
    'actif': 'Actif',
    'inactif': 'Inactif',
    'supprime': 'Supprimé'
}

TYPES_LIEU = {
    'bureau': 'Bureau',
    'agence': 'Agence',
    'externe': 'Externe',
    'domicile': 'Domicile',
    'autre': 'Autre'
}


# =============================================
# MODÈLE POUR LA PRÉSENCE (POINTAGE)
# =============================================

class Presence(db.Model):
    """Modèle pour la présence/pointage des employés"""

    __tablename__ = 'presences'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rh_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Chargé RH qui a validé

    # Dates et heures
    date = db.Column(db.DateTime, default=datetime.utcnow)
    date_pointage = db.Column(db.Date, nullable=False)

    heure_arrivee = db.Column(db.DateTime, nullable=True)
    heure_depart = db.Column(db.DateTime, nullable=True)

    # Temps de travail
    duree_travail = db.Column(db.Integer, nullable=True)  # en minutes
    heures_supplementaires = db.Column(db.Integer, default=0)  # en minutes

    # Statut
    statut = db.Column(db.String(200), default='present')
    # Options: 'present', 'absent', 'retard', 'excusé', 'congé', 'formation', 'mission'

    # Retard
    retard_minutes = db.Column(db.Integer, default=0)
    motif_retard = db.Column(db.String(200), nullable=True)

    # Départ anticipé
    depart_anticipe_minutes = db.Column(db.Integer, default=0)
    motif_depart_anticipe = db.Column(db.String(200), nullable=True)

    # Validation
    valide = db.Column(db.Boolean, default=False)
    date_validation = db.Column(db.DateTime, nullable=True)
    commentaires_validation = db.Column(db.Text, nullable=True)

    # Métadonnées
    methode_pointage = db.Column(db.String(50), default='manuel')
    # Options: 'manuel', 'qr_code', 'biometrique', 'mobile'

    notes = db.Column(db.Text, nullable=True)
    lieu_pointage = db.Column(db.String(200), nullable=True)

    # Dates système
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations inverses
    user = db.relationship('User', foreign_keys=[user_id], backref='presences', lazy=True)
    rh = db.relationship('User', foreign_keys=[rh_id], backref='presences_validees', lazy=True)

    def __repr__(self):
        return f'<Presence {self.id} - {self.user.prenom} {self.user.nom} - {self.date_pointage}>'

    @staticmethod
    def get_aujourdhui(user_id):
        """Récupère la présence d'aujourd'hui pour un utilisateur"""
        today = datetime.utcnow().date()
        return Presence.query.filter_by(
            user_id=user_id,
            date_pointage=today
        ).first()

    @staticmethod
    def get_presences_jour(user_id, date=None):
        """Récupère les présences d'un jour spécifique"""
        if date is None:
            date = datetime.utcnow().date()
        return Presence.query.filter_by(
            user_id=user_id,
            date_pointage=date
        ).all()

    @staticmethod
    def get_presences_mois(user_id, annee=None, mois=None):
        """Récupère les présences d'un mois"""
        if annee is None:
            annee = datetime.utcnow().year
        if mois is None:
            mois = datetime.utcnow().month

        start_date = datetime(annee, mois, 1).date()
        if mois == 12:
            end_date = datetime(annee + 1, 1, 1).date()
        else:
            end_date = datetime(annee, mois + 1, 1).date()

        return Presence.query.filter(
            Presence.user_id == user_id,
            Presence.date_pointage >= start_date,
            Presence.date_pointage < end_date
        ).order_by(Presence.date_pointage.asc()).all()

    @staticmethod
    def get_statistiques_mois(user_id, annee=None, mois=None):
        """Statistiques de présence pour un mois"""
        presences = Presence.get_presences_mois(user_id, annee, mois)

        total_jours = len(presences)
        presents = len([p for p in presences if p.statut == 'present'])
        absents = len([p for p in presences if p.statut == 'absent'])
        retards = len([p for p in presences if p.statut == 'retard'])
        excuses = len([p for p in presences if p.statut == 'excusé'])
        conges = len([p for p in presences if p.statut == 'congé'])
        formations = len([p for p in presences if p.statut == 'formation'])
        missions = len([p for p in presences if p.statut == 'mission'])

        # Temps de travail total
        temps_total = sum([p.duree_travail or 0 for p in presences])
        heures_total = temps_total // 60
        minutes_total = temps_total % 60

        # Retards totaux
        retards_total = sum([p.retard_minutes or 0 for p in presences])
        retards_heures = retards_total // 60
        retards_minutes = retards_total % 60

        # Taux de présence
        taux_presence = round((presents / total_jours * 100), 2) if total_jours > 0 else 0

        return {
            'total_jours': total_jours,
            'presents': presents,
            'absents': absents,
            'retards': retards,
            'excuses': excuses,
            'conges': conges,
            'formations': formations,
            'missions': missions,
            'taux_presence': taux_presence,
            'temps_total': temps_total,
            'heures_total': heures_total,
            'minutes_total': minutes_total,
            'retards_total': retards_total,
            'retards_heures': retards_heures,
            'retards_minutes': retards_minutes
        }

    @staticmethod
    def get_absents_aujourdhui(rh_id=None):
        """Récupère les employés absents aujourd'hui"""
        today = datetime.utcnow().date()
        query = Presence.query.filter(
            Presence.date_pointage == today,
            Presence.statut == 'absent'
        )
        if rh_id:
            query = query.join(User).filter(User.rh_id == rh_id)
        return query.all()

    @staticmethod
    def get_retards_aujourdhui(rh_id=None):
        """Récupère les employés en retard aujourd'hui"""
        today = datetime.utcnow().date()
        query = Presence.query.filter(
            Presence.date_pointage == today,
            Presence.statut == 'retard'
        )
        if rh_id:
            query = query.join(User).filter(User.rh_id == rh_id)
        return query.all()

    def pointer_arrivee(self, heure=None, methode='manuel', lieu=None):
        """Enregistre l'heure d'arrivée"""
        if heure is None:
            heure = datetime.utcnow()
        self.heure_arrivee = heure
        self.date_pointage = heure.date()
        self.methode_pointage = methode
        if lieu:
            self.lieu_pointage = lieu

        # Vérifier si c'est un retard (heure d'arrivée > 8h30)
        heure_limite = heure.replace(hour=8, minute=30, second=0, microsecond=0)
        if heure > heure_limite:
            self.statut = 'retard'
            self.retard_minutes = int((heure - heure_limite).total_seconds() / 60)

        db.session.commit()

    def pointer_depart(self, heure=None):
        """Enregistre l'heure de départ"""
        if heure is None:
            heure = datetime.utcnow()
        self.heure_depart = heure

        # Calculer la durée de travail
        if self.heure_arrivee:
            duree = (heure - self.heure_arrivee).total_seconds() / 60
            self.duree_travail = int(duree)

        db.session.commit()

    def valider(self, rh_id, commentaires=None):
        """Valide la présence"""
        self.valide = True
        self.rh_id = rh_id
        self.date_validation = datetime.utcnow()
        if commentaires:
            self.commentaires_validation = commentaires
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_nom': f"{self.user.prenom} {self.user.nom}" if self.user else None,
            'date_pointage': self.date_pointage.isoformat(),
            'heure_arrivee': self.heure_arrivee.isoformat() if self.heure_arrivee else None,
            'heure_depart': self.heure_depart.isoformat() if self.heure_depart else None,
            'duree_travail': self.duree_travail,
            'statut': self.statut,
            'retard_minutes': self.retard_minutes,
            'valide': self.valide,
            'methode_pointage': self.methode_pointage,
            'lieu_pointage': self.lieu_pointage
        }


# =============================================
# MODÈLE POUR LES CONGÉS
# =============================================

class Conge(db.Model):
    """Modèle pour les congés des employés"""

    __tablename__ = 'conges'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rh_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Chargé RH qui a approuvé
    remplacant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Qui remplace

    # Informations
    type_conge = db.Column(db.String(50), nullable=False)
    # Options: 'annuel', 'maladie', 'maternite', 'paternite', 'sans_solde', 'formation', 'exceptionnel'

    motif = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)

    # Dates
    date_debut = db.Column(db.DateTime, nullable=False)
    date_fin = db.Column(db.DateTime, nullable=False)
    date_reprise = db.Column(db.DateTime, nullable=True)

    # Durée
    duree_jours = db.Column(db.Integer, nullable=False)
    duree_ouvrables = db.Column(db.Integer, nullable=True)  # Jours ouvrés

    # Solde
    solde_utilise = db.Column(db.Integer, default=0)  # Jours utilisés
    solde_restant = db.Column(db.Integer, default=0)  # Jours restants

    # Statut
    statut = db.Column(db.String(200), default='en_attente')
    # Options: 'en_attente', 'approuve', 'refuse', 'annule', 'termine'

    # Approbations
    approbateur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    date_approbation = db.Column(db.DateTime, nullable=True)
    commentaires_approbation = db.Column(db.Text, nullable=True)

    # Métadonnées
    urgent = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)
    pieces_jointes = db.Column(db.Text, nullable=True)  # Chemin des fichiers

    # Dates système
    date_demande = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations inverses
    user = db.relationship('User', foreign_keys=[user_id], backref='conges', lazy=True)
    rh = db.relationship('User', foreign_keys=[rh_id], backref='conges_approuves', lazy=True)
    remplacant = db.relationship('User', foreign_keys=[remplacant_id], backref='conges_remplacements', lazy=True)
    approbateur = db.relationship('User', foreign_keys=[approbateur_id], backref='conges_approbations', lazy=True)

    def __repr__(self):
        return f'<Conge {self.id} - {self.user.prenom} {self.user.nom} - {self.type_conge}>'

    @staticmethod
    def get_en_cours(user_id=None):
        """Récupère les congés en cours"""
        today = datetime.utcnow().date()
        query = Conge.query.filter(
            Conge.date_debut <= today,
            Conge.date_fin >= today,
            Conge.statut.in_(['approuve', 'termine'])
        )
        if user_id:
            query = query.filter(Conge.user_id == user_id)
        return query.all()

    @staticmethod
    def get_a_venir(user_id=None, limit=None):
        """Récupère les congés à venir"""
        today = datetime.utcnow().date()
        query = Conge.query.filter(
            Conge.date_debut > today,
            Conge.statut.in_(['en_attente', 'approuve'])
        ).order_by(Conge.date_debut.asc())
        if user_id:
            query = query.filter(Conge.user_id == user_id)
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_en_attente(rh_id=None, limit=None):
        """Récupère les congés en attente d'approbation"""
        query = Conge.query.filter_by(statut='en_attente').order_by(Conge.date_demande.asc())
        if rh_id:
            query = query.join(User).filter(User.rh_id == rh_id)
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_par_employe(user_id, limit=None):
        """Récupère les congés d'un employé"""
        query = Conge.query.filter_by(user_id=user_id).order_by(Conge.date_debut.desc())
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_statistiques(rh_id=None, annee=None):
        """Statistiques des congés"""
        if annee is None:
            annee = datetime.utcnow().year

        start_date = datetime(annee, 1, 1)
        end_date = datetime(annee + 1, 1, 1)

        query = Conge.query.filter(
            Conge.date_debut >= start_date,
            Conge.date_debut < end_date
        )
        if rh_id:
            query = query.join(User).filter(User.rh_id == rh_id)

        conges = query.all()

        total = len(conges)
        en_attente = len([c for c in conges if c.statut == 'en_attente'])
        approuves = len([c for c in conges if c.statut == 'approuve'])
        refuses = len([c for c in conges if c.statut == 'refuse'])
        annules = len([c for c in conges if c.statut == 'annule'])
        termines = len([c for c in conges if c.statut == 'termine'])

        # Par type
        types = {}
        for t in ['annuel', 'maladie', 'maternite', 'paternite', 'sans_solde', 'formation', 'exceptionnel']:
            count = len([c for c in conges if c.type_conge == t])
            types[t] = count

        # Jours de congé totaux
        jours_totaux = sum([c.duree_jours for c in conges if c.statut in ['approuve', 'termine']])

        return {
            'total': total,
            'en_attente': en_attente,
            'approuves': approuves,
            'refuses': refuses,
            'annules': annules,
            'termines': termines,
            'types': types,
            'jours_totaux': jours_totaux
        }

    def approuver(self, rh_id, commentaires=None):
        """Approuve le congé"""
        self.statut = 'approuve'
        self.rh_id = rh_id
        self.approbateur_id = rh_id
        self.date_approbation = datetime.utcnow()
        if commentaires:
            self.commentaires_approbation = commentaires
        db.session.commit()

    def refuser(self, rh_id, commentaires=None):
        """Refuse le congé"""
        self.statut = 'refuse'
        self.rh_id = rh_id
        self.approbateur_id = rh_id
        self.date_approbation = datetime.utcnow()
        if commentaires:
            self.commentaires_approbation = commentaires
        db.session.commit()

    def annuler(self, notes=None):
        """Annule le congé"""
        self.statut = 'annule'
        if notes:
            self.notes = notes
        db.session.commit()

    def terminer(self):
        """Marque le congé comme terminé"""
        self.statut = 'termine'
        self.date_reprise = datetime.utcnow()
        db.session.commit()

    def calculer_duree(self):
        """Calcule la durée en jours"""
        delta = self.date_fin - self.date_debut
        self.duree_jours = delta.days + 1
        return self.duree_jours

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_nom': f"{self.user.prenom} {self.user.nom}" if self.user else None,
            'type_conge': self.type_conge,
            'motif': self.motif,
            'description': self.description,
            'date_debut': self.date_debut.isoformat(),
            'date_fin': self.date_fin.isoformat(),
            'date_reprise': self.date_reprise.isoformat() if self.date_reprise else None,
            'duree_jours': self.duree_jours,
            'solde_utilise': self.solde_utilise,
            'solde_restant': self.solde_restant,
            'statut': self.statut,
            'date_demande': self.date_demande.isoformat(),
            'date_approbation': self.date_approbation.isoformat() if self.date_approbation else None,
            'urgent': self.urgent,
            'notes': self.notes
        }


# =============================================
# MODÈLE POUR LE SOLDE DE CONGÉS
# =============================================

class SoldeConge(db.Model):
    """Modèle pour le solde de congés des employés"""

    __tablename__ = 'soldes_conges'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    # Soldes
    total_annuel = db.Column(db.Integer, default=30)  # Jours de congé par an
    restant_annuel = db.Column(db.Integer, default=30)
    utilise_annuel = db.Column(db.Integer, default=0)

    # Maladie
    total_maladie = db.Column(db.Integer, default=10)
    restant_maladie = db.Column(db.Integer, default=10)
    utilise_maladie = db.Column(db.Integer, default=0)

    # Autres
    total_exceptionnel = db.Column(db.Integer, default=0)
    restant_exceptionnel = db.Column(db.Integer, default=0)
    utilise_exceptionnel = db.Column(db.Integer, default=0)

    # Congés non pris (report)
    report_annee = db.Column(db.Integer, default=0)
    report_jours = db.Column(db.Integer, default=0)

    # Année de référence
    annee_reference = db.Column(db.Integer, default=lambda: datetime.utcnow().year)

    # Dates
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations inverses
    user = db.relationship('User', backref='solde_conges', lazy=True)

    def __repr__(self):
        return f'<SoldeConge {self.id} - {self.user.prenom} {self.user.nom}>'

    def utiliser_jours(self, type_conge, jours):
        """Utilise des jours de congé"""
        if type_conge == 'annuel':
            if self.restant_annuel >= jours:
                self.restant_annuel -= jours
                self.utilise_annuel += jours
                return True, f"{jours} jours de congé annuel utilisés"
        elif type_conge == 'maladie':
            if self.restant_maladie >= jours:
                self.restant_maladie -= jours
                self.utilise_maladie += jours
                return True, f"{jours} jours de congé maladie utilisés"
        elif type_conge == 'exceptionnel':
            if self.restant_exceptionnel >= jours:
                self.restant_exceptionnel -= jours
                self.utilise_exceptionnel += jours
                return True, f"{jours} jours de congé exceptionnel utilisés"
        return False, "Solde insuffisant"

    def ajouter_jours(self, type_conge, jours):
        """Ajoute des jours de congé"""
        if type_conge == 'annuel':
            self.total_annuel += jours
            self.restant_annuel += jours
        elif type_conge == 'maladie':
            self.total_maladie += jours
            self.restant_maladie += jours
        elif type_conge == 'exceptionnel':
            self.total_exceptionnel += jours
            self.restant_exceptionnel += jours
        db.session.commit()

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_nom': f"{self.user.prenom} {self.user.nom}" if self.user else None,
            'annuel': {
                'total': self.total_annuel,
                'utilise': self.utilise_annuel,
                'restant': self.restant_annuel
            },
            'maladie': {
                'total': self.total_maladie,
                'utilise': self.utilise_maladie,
                'restant': self.restant_maladie
            },
            'exceptionnel': {
                'total': self.total_exceptionnel,
                'utilise': self.utilise_exceptionnel,
                'restant': self.restant_exceptionnel
            },
            'report_jours': self.report_jours,
            'annee_reference': self.annee_reference
        }


# =============================================
# CONSTANTES
# =============================================

STATUTS_PRESENCE = {
    'present': 'Présent',
    'absent': 'Absent',
    'retard': 'En retard',
    'excusé': 'Excusé',
    'congé': 'En congé',
    'formation': 'En formation',
    'mission': 'En mission'
}

METHODES_POINTAGE = {
    'manuel': 'Manuel',
    'qr_code': 'QR Code',
    'biometrique': 'Biométrique',
    'mobile': 'Application mobile'
}

TYPES_CONGE = {
    'annuel': 'Congé annuel',
    'maladie': 'Congé maladie',
    'maternite': 'Congé maternité',
    'paternite': 'Congé paternité',
    'sans_solde': 'Congé sans solde',
    'formation': 'Congé formation',
    'exceptionnel': 'Congé exceptionnel'
}

STATUTS_CONGE = {
    'en_attente': 'En attente',
    'approuve': 'Approuvé',
    'refuse': 'Refusé',
    'annule': 'Annulé',
    'termine': 'Terminé'
}


# =============================================
# MODÈLE POUR LES TICKETS DE SUPPORT
# =============================================

class TicketSupport(db.Model):
    """Modèle pour les tickets de support informatique"""

    __tablename__ = 'tickets_support'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    demandeur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    informaticien_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    equipement_id = db.Column(db.Integer, db.ForeignKey('equipements.id'), nullable=True)

    # Informations
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    etapes = db.Column(db.Text, nullable=True)  # Étapes de résolution

    # Catégorie
    categorie = db.Column(db.String(50), nullable=False)
    # Options: 'materiel', 'logiciel', 'reseau', 'securite', 'telephonie', 'acces', 'autre'

    # Sous-catégorie
    sous_categorie = db.Column(db.String(50), nullable=True)

    # Priorité
    priorite = db.Column(db.String(20), default='moyenne')
    # Options: 'basse', 'moyenne', 'haute', 'critique'

    # Urgence
    urgence = db.Column(db.Boolean, default=False)

    # Statut
    statut = db.Column(db.String(20), default='nouveau')
    # Options: 'nouveau', 'en_cours', 'en_attente', 'resolu', 'ferme', 'annule'

    # Dates
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_attribution = db.Column(db.DateTime, nullable=True)
    date_debut_traitement = db.Column(db.DateTime, nullable=True)
    date_resolution = db.Column(db.DateTime, nullable=True)
    date_fermeture = db.Column(db.DateTime, nullable=True)
    date_echeance = db.Column(db.DateTime, nullable=True)

    # Résolution
    solution = db.Column(db.Text, nullable=True)
    commentaires = db.Column(db.Text, nullable=True)

    # Satisfaction
    satisfaction = db.Column(db.Integer, nullable=True)  # 1-5
    commentaire_satisfaction = db.Column(db.Text, nullable=True)

    # Temps
    temps_estime = db.Column(db.Integer, nullable=True)  # en minutes
    temps_reel = db.Column(db.Integer, nullable=True)  # en minutes

    # Métadonnées
    pieces_jointes = db.Column(db.Text, nullable=True)  # Chemins des fichiers
    version_os = db.Column(db.String(50), nullable=True)
    navigateur = db.Column(db.String(50), nullable=True)
    capture_ecran = db.Column(db.Text, nullable=True)

    # Relations inverses
    demandeur = db.relationship('User', foreign_keys=[demandeur_id], backref='tickets_demandes', lazy=True)
    informaticien = db.relationship('User', foreign_keys=[informaticien_id], backref='tickets_assignes', lazy=True)
    equipement = db.relationship('Equipement', backref='tickets', lazy=True)

    def __repr__(self):
        return f'<TicketSupport {self.id} - {self.titre} - {self.statut}>'

    @staticmethod
    def get_nouveaux(informaticien_id=None, limit=None):
        """Récupère les tickets nouveaux"""
        query = TicketSupport.query.filter_by(statut='nouveau').order_by(
            TicketSupport.priorite.desc(),
            TicketSupport.date_creation.asc()
        )
        if informaticien_id:
            query = query.filter_by(informaticien_id=informaticien_id)
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_en_cours(informaticien_id=None, limit=None):
        """Récupère les tickets en cours"""
        query = TicketSupport.query.filter(
            TicketSupport.statut.in_(['en_cours', 'en_attente'])
        ).order_by(TicketSupport.priorite.desc(), TicketSupport.date_modification.desc())
        if informaticien_id:
            query = query.filter_by(informaticien_id=informaticien_id)
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_urgents(informaticien_id=None):
        """Récupère les tickets urgents"""
        query = TicketSupport.query.filter(
            TicketSupport.priorite.in_(['haute', 'critique']),
            TicketSupport.statut.in_(['nouveau', 'en_cours', 'en_attente'])
        ).order_by(TicketSupport.priorite.desc(), TicketSupport.date_creation.asc())
        if informaticien_id:
            query = query.filter_by(informaticien_id=informaticien_id)
        return query.all()

    @staticmethod
    def get_par_demandeur(demandeur_id, limit=None):
        """Récupère les tickets d'un demandeur"""
        query = TicketSupport.query.filter_by(demandeur_id=demandeur_id).order_by(
            TicketSupport.date_creation.desc()
        )
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_statistiques(informaticien_id=None):
        """Statistiques des tickets"""
        query = TicketSupport.query
        if informaticien_id:
            query = query.filter_by(informaticien_id=informaticien_id)

        total = query.count()
        nouveaux = query.filter_by(statut='nouveau').count()
        en_cours = query.filter_by(statut='en_cours').count()
        en_attente = query.filter_by(statut='en_attente').count()
        resolus = query.filter_by(statut='resolu').count()
        fermes = query.filter_by(statut='ferme').count()
        annules = query.filter_by(statut='annule').count()

        # Par priorité
        critiques = query.filter_by(priorite='critique').count()
        hautes = query.filter_by(priorite='haute').count()
        moyennes = query.filter_by(priorite='moyenne').count()
        basses = query.filter_by(priorite='basse').count()

        # Par catégorie
        categories = {}
        for cat in ['materiel', 'logiciel', 'reseau', 'securite', 'telephonie', 'acces', 'autre']:
            count = query.filter_by(categorie=cat).count()
            categories[cat] = count

        # Temps moyen de résolution
        temps_total = db.session.query(db.func.sum(TicketSupport.temps_reel)).filter(
            TicketSupport.statut.in_(['resolu', 'ferme'])
        )
        if informaticien_id:
            temps_total = temps_total.filter_by(informaticien_id=informaticien_id)
        temps_total = temps_total.scalar() or 0

        nb_resolus = resolus + fermes
        temps_moyen = round(temps_total / nb_resolus, 2) if nb_resolus > 0 else 0

        # Taux de résolution
        taux_resolution = round(((resolus + fermes) / total * 100), 2) if total > 0 else 0

        # Satisfaction moyenne
        satisfaction = query.filter(TicketSupport.satisfaction.isnot(None))
        satisfaction_moyenne = db.session.query(db.func.avg(TicketSupport.satisfaction)).filter(
            TicketSupport.statut.in_(['resolu', 'ferme'])
        )
        if informaticien_id:
            satisfaction_moyenne = satisfaction_moyenne.filter_by(informaticien_id=informaticien_id)
        satisfaction_moyenne = satisfaction_moyenne.scalar() or 0

        return {
            'total': total,
            'nouveaux': nouveaux,
            'en_cours': en_cours,
            'en_attente': en_attente,
            'resolus': resolus,
            'fermes': fermes,
            'annules': annules,
            'critiques': critiques,
            'hautes': hautes,
            'moyennes': moyennes,
            'basses': basses,
            'categories': categories,
            'temps_moyen': temps_moyen,
            'taux_resolution': taux_resolution,
            'satisfaction_moyenne': round(satisfaction_moyenne, 2)
        }

    def attribuer(self, informaticien_id):
        """Attribue le ticket à un informaticien"""
        self.informaticien_id = informaticien_id
        self.statut = 'en_cours'
        self.date_attribution = datetime.utcnow()
        self.date_debut_traitement = datetime.utcnow()
        db.session.commit()

    def resoudre(self, solution=None, temps=None):
        """Résout le ticket"""
        self.statut = 'resolu'
        self.date_resolution = datetime.utcnow()
        if solution:
            self.solution = solution
        if temps:
            self.temps_reel = temps
        db.session.commit()

    def fermer(self, commentaires=None):
        """Ferme le ticket"""
        self.statut = 'ferme'
        self.date_fermeture = datetime.utcnow()
        if commentaires:
            self.commentaires = commentaires
        db.session.commit()

    def annuler(self, motif=None):
        """Annule le ticket"""
        self.statut = 'annule'
        if motif:
            self.commentaires = motif
        db.session.commit()

    def mettre_en_attente(self, motif=None):
        """Met le ticket en attente"""
        self.statut = 'en_attente'
        if motif:
            self.commentaires = motif
        db.session.commit()

    def noter_satisfaction(self, note, commentaire=None):
        """Note la satisfaction"""
        self.satisfaction = note
        if commentaire:
            self.commentaire_satisfaction = commentaire
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'description': self.description,
            'categorie': self.categorie,
            'priorite': self.priorite,
            'statut': self.statut,
            'demandeur_id': self.demandeur_id,
            'demandeur_nom': f"{self.demandeur.prenom} {self.demandeur.nom}" if self.demandeur else None,
            'informaticien_id': self.informaticien_id,
            'informaticien_nom': f"{self.informaticien.prenom} {self.informaticien.nom}" if self.informaticien else None,
            'date_creation': self.date_creation.isoformat(),
            'date_resolution': self.date_resolution.isoformat() if self.date_resolution else None,
            'solution': self.solution,
            'satisfaction': self.satisfaction,
            'temps_estime': self.temps_estime,
            'temps_reel': self.temps_reel
        }


# =============================================
# MODÈLE POUR LES ÉQUIPEMENTS
# =============================================

class Equipement(db.Model):
    """Modèle pour les équipements informatiques"""

    __tablename__ = 'equipements'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    informaticien_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Utilisateur assigné

    # Informations générales
    nom = db.Column(db.String(100), nullable=False)
    marque = db.Column(db.String(50), nullable=True)
    modele = db.Column(db.String(50), nullable=True)

    # Type d'équipement
    type_equipement = db.Column(db.String(50), nullable=False)
    # Options: 'pc', 'serveur', 'imprimante', 'reseau', 'telephonie', 'accessoire', 'autre'

    # Identification
    numero_serie = db.Column(db.String(100), unique=True, nullable=True)
    code_inventaire = db.Column(db.String(50), unique=True, nullable=True)
    mac_adresse = db.Column(db.String(50), nullable=True)
    ip_adresse = db.Column(db.String(50), nullable=True)

    # Caractéristiques
    processeur = db.Column(db.String(100), nullable=True)
    ram = db.Column(db.String(20), nullable=True)  # ex: "8 Go"
    stockage = db.Column(db.String(50), nullable=True)  # ex: "256 Go SSD"
    systeme_exploitation = db.Column(db.String(50), nullable=True)

    # Localisation
    localisation = db.Column(db.String(200), nullable=True)
    batiment = db.Column(db.String(50), nullable=True)
    bureau = db.Column(db.String(50), nullable=True)

    # Statut
    statut = db.Column(db.String(20), default='operationnel')
    # Options: 'operationnel', 'maintenance', 'panne', 'reforme', 'reserve'

    # Dates
    date_acquisition = db.Column(db.DateTime, nullable=True)
    date_mise_en_service = db.Column(db.DateTime, nullable=True)
    date_derniere_maintenance = db.Column(db.DateTime, nullable=True)
    date_prochaine_maintenance = db.Column(db.DateTime, nullable=True)
    date_garantie_fin = db.Column(db.DateTime, nullable=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Métadonnées
    fournisseur = db.Column(db.String(100), nullable=True)
    prix_achat = db.Column(db.Float, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    # Relations inverses
    informaticien = db.relationship('User', foreign_keys=[informaticien_id], backref='equipements_gere', lazy=True)
    utilisateur = db.relationship('User', foreign_keys=[utilisateur_id], backref='equipements_assignes', lazy=True)

    def __repr__(self):
        return f'<Equipement {self.id} - {self.nom} - {self.type_equipement}>'

    @staticmethod
    def get_operationnels(informaticien_id=None, limit=None):
        """Récupère les équipements opérationnels"""
        query = Equipement.query.filter_by(statut='operationnel')
        if informaticien_id:
            query = query.filter_by(informaticien_id=informaticien_id)
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_en_maintenance(informaticien_id=None):
        """Récupère les équipements en maintenance"""
        query = Equipement.query.filter_by(statut='maintenance')
        if informaticien_id:
            query = query.filter_by(informaticien_id=informaticien_id)
        return query.all()

    @staticmethod
    def get_par_type(informaticien_id=None, type_equipement=None):
        """Récupère les équipements par type"""
        query = Equipement.query
        if informaticien_id:
            query = query.filter_by(informaticien_id=informaticien_id)
        if type_equipement:
            query = query.filter_by(type_equipement=type_equipement)
        return query.all()

    @staticmethod
    def get_par_utilisateur(utilisateur_id):
        """Récupère les équipements assignés à un utilisateur"""
        return Equipement.query.filter_by(utilisateur_id=utilisateur_id).all()

    @staticmethod
    def get_statistiques(informaticien_id=None):
        """Statistiques des équipements"""
        query = Equipement.query
        if informaticien_id:
            query = query.filter_by(informaticien_id=informaticien_id)

        total = query.count()
        operationnels = query.filter_by(statut='operationnel').count()
        maintenance = query.filter_by(statut='maintenance').count()
        panne = query.filter_by(statut='panne').count()
        reforme = query.filter_by(statut='reforme').count()
        reserve = query.filter_by(statut='reserve').count()

        # Par type
        types = {}
        for t in ['pc', 'serveur', 'imprimante', 'reseau', 'telephonie', 'accessoire', 'autre']:
            count = query.filter_by(type_equipement=t).count()
            types[t] = count

        # Par localisation
        localisations = {}
        for equip in query.all():
            if equip.localisation:
                localisations[equip.localisation] = localisations.get(equip.localisation, 0) + 1

        # Âge moyen
        ages = []
        for equip in query.filter(Equipement.date_acquisition.isnot(None)).all():
            age = (datetime.utcnow() - equip.date_acquisition).days
            ages.append(age)
        age_moyen = round(sum(ages) / len(ages), 2) if ages else 0

        return {
            'total': total,
            'operationnels': operationnels,
            'maintenance': maintenance,
            'panne': panne,
            'reforme': reforme,
            'reserve': reserve,
            'types': types,
            'localisations': localisations,
            'age_moyen_jours': age_moyen,
            'age_moyen_ans': round(age_moyen / 365, 2) if age_moyen > 0 else 0
        }

    def assigner(self, utilisateur_id):
        """Assigne l'équipement à un utilisateur"""
        self.utilisateur_id = utilisateur_id
        db.session.commit()

    def liberer(self):
        """Libère l'équipement"""
        self.utilisateur_id = None
        db.session.commit()

    def changer_statut(self, statut, notes=None):
        """Change le statut de l'équipement"""
        self.statut = statut
        if notes:
            self.notes = notes
        db.session.commit()

    def planifier_maintenance(self, date_maintenance):
        """Planifie une maintenance"""
        self.date_prochaine_maintenance = date_maintenance
        if self.statut == 'operationnel':
            self.statut = 'maintenance'
        db.session.commit()

    def effectuer_maintenance(self):
        """Effectue la maintenance"""
        self.date_derniere_maintenance = datetime.utcnow()
        self.date_prochaine_maintenance = None
        if self.statut == 'maintenance':
            self.statut = 'operationnel'
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'marque': self.marque,
            'modele': self.modele,
            'type_equipement': self.type_equipement,
            'numero_serie': self.numero_serie,
            'code_inventaire': self.code_inventaire,
            'mac_adresse': self.mac_adresse,
            'ip_adresse': self.ip_adresse,
            'processeur': self.processeur,
            'ram': self.ram,
            'stockage': self.stockage,
            'systeme_exploitation': self.systeme_exploitation,
            'localisation': self.localisation,
            'statut': self.statut,
            'date_acquisition': self.date_acquisition.isoformat() if self.date_acquisition else None,
            'date_mise_en_service': self.date_mise_en_service.isoformat() if self.date_mise_en_service else None,
            'date_garantie_fin': self.date_garantie_fin.isoformat() if self.date_garantie_fin else None,
            'fournisseur': self.fournisseur,
            'prix_achat': self.prix_achat,
            'utilisateur_id': self.utilisateur_id,
            'utilisateur_nom': f"{self.utilisateur.prenom} {self.utilisateur.nom}" if self.utilisateur else None
        }


# =============================================
# MODÈLE POUR L'HISTORIQUE DES TICKETS
# =============================================

class HistoriqueTicket(db.Model):
    """Modèle pour l'historique des tickets de support"""

    __tablename__ = 'historique_tickets'

    id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets_support.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    action = db.Column(db.String(50), nullable=False)
    # Options: 'creation', 'attribution', 'debut_traitement', 'mise_en_attente', 'resolution', 'fermeture', 'annulation', 'commentaire'

    ancien_statut = db.Column(db.String(20), nullable=True)
    nouveau_statut = db.Column(db.String(20), nullable=True)

    commentaire = db.Column(db.Text, nullable=True)

    date_action = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    ticket = db.relationship('TicketSupport', backref='historique', lazy=True)
    user = db.relationship('User', backref='historique_tickets', lazy=True)

    def __repr__(self):
        return f'<HistoriqueTicket {self.id} - Ticket {self.ticket_id} - {self.action}>'

    def to_dict(self):
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'user_id': self.user_id,
            'user_nom': f"{self.user.prenom} {self.user.nom}" if self.user else None,
            'action': self.action,
            'ancien_statut': self.ancien_statut,
            'nouveau_statut': self.nouveau_statut,
            'commentaire': self.commentaire,
            'date_action': self.date_action.isoformat()
        }


# =============================================
# CONSTANTES
# =============================================

CATEGORIES_TICKET = {
    'materiel': 'Matériel',
    'logiciel': 'Logiciel',
    'reseau': 'Réseau',
    'securite': 'Sécurité',
    'telephonie': 'Téléphonie',
    'acces': 'Accès',
    'autre': 'Autre'
}

PRIORITES_TICKET = {
    'basse': 'Basse',
    'moyenne': 'Moyenne',
    'haute': 'Haute',
    'critique': 'Critique'
}

STATUTS_TICKET = {
    'nouveau': 'Nouveau',
    'en_cours': 'En cours',
    'en_attente': 'En attente',
    'resolu': 'Résolu',
    'ferme': 'Fermé',
    'annule': 'Annulé'
}

TYPES_EQUIPEMENT = {
    'pc': 'Poste de travail',
    'serveur': 'Serveur',
    'imprimante': 'Imprimante',
    'reseau': 'Équipement réseau',
    'telephonie': 'Téléphonie',
    'accessoire': 'Accessoire',
    'autre': 'Autre'
}

STATUTS_EQUIPEMENT = {
    'operationnel': 'Opérationnel',
    'maintenance': 'En maintenance',
    'panne': 'En panne',
    'reforme': 'Réformé',
    'reserve': 'En réserve'
}

ACTIONS_HISTORIQUE_TICKET = {
    'creation': 'Création',
    'attribution': 'Attribution',
    'debut_traitement': 'Début traitement',
    'mise_en_attente': 'Mise en attente',
    'resolution': 'Résolution',
    'fermeture': 'Fermeture',
    'annulation': 'Annulation',
    'commentaire': 'Commentaire'
}

class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    categorie = db.Column(db.String(50), nullable=True)  # Ex: 'client', 'credit', 'paiement', 'employe'

    # 👇 AJOUTEZ CETTE LIGNE (décommentez ou ajoutez-la)
    users = db.relationship('User', secondary='user_permissions', back_populates='permissions')

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Permission {self.nom}>'

    @classmethod
    def init_default_permissions(cls):
        """Initialise les permissions par défaut dans la base de données"""

        permissions_data = [
            # 👥 CLIENTS
            ('voir_clients', 'Voir la liste des clients', 'clients'),
            ('creer_client', 'Créer un nouveau client', 'clients'),
            ('modifier_client', 'Modifier les informations client', 'clients'),
            ('supprimer_client', 'Supprimer un client', 'clients'),
            ('exporter_clients', 'Exporter la liste des clients', 'clients'),

            # 💰 CRÉDITS
            ('voir_credits', 'Voir la liste des crédits', 'credits'),
            ('creer_credit', 'Créer une demande de crédit', 'credits'),
            ('modifier_credit', 'Modifier un crédit', 'credits'),
            ('approuver_credit', 'Approuver les crédits', 'credits'),
            ('rejeter_credit', 'Rejeter les crédits', 'credits'),
            ('annuler_credit', 'Annuler un crédit', 'credits'),
            ('voir_analyse_credit', 'Voir les analyses de crédit', 'credits'),
            ('simuler_credit', 'Simuler un crédit', 'credits'),

            # 💵 PAIEMENTS
            ('voir_paiements', 'Voir l\'historique des paiements', 'paiements'),
            ('enregistrer_paiement', 'Enregistrer un paiement', 'paiements'),
            ('modifier_paiement', 'Modifier un paiement', 'paiements'),
            ('annuler_paiement', 'Annuler un paiement', 'paiements'),
            ('exporter_paiements', 'Exporter les paiements', 'paiements'),
            ('voir_echeances', 'Voir les échéances', 'paiements'),

            # 📊 RAPPORTS
            ('voir_rapports', 'Voir les rapports', 'rapports'),
            ('exporter_rapports', 'Exporter les rapports', 'rapports'),
            ('creer_rapport_personnalise', 'Créer des rapports personnalisés', 'rapports'),
            ('voir_tableau_bord', 'Voir le tableau de bord', 'rapports'),

            # 👔 EMPLOYÉS (pour superviseurs)
            ('voir_employes', 'Voir la liste des employés', 'employes'),
            ('creer_employe', 'Créer un nouvel employé', 'employes'),
            ('modifier_employe', 'Modifier un employé', 'employes'),
            ('suspendre_employe', 'Suspendre un employé', 'employes'),
            ('reactiver_employe', 'Réactiver un employé', 'employes'),
            ('supprimer_employe', 'Supprimer un employé', 'employes'),
            ('gerer_permissions', 'Gérer les permissions des employés', 'employes'),

            # 🏦 SUCCURSALES
            ('voir_succursales', 'Voir les succursales', 'succursales'),
            ('creer_succursale', 'Créer une succursale', 'succursales'),
            ('modifier_succursale', 'Modifier une succursale', 'succursales'),

            # 🏧 CAISSE (pour caissiers)
            ('gerer_caisse', 'Gérer la caisse', 'caisse'),
            ('ouvrir_caisse', 'Ouvrir la caisse', 'caisse'),
            ('fermer_caisse', 'Fermer la caisse', 'caisse'),
            ('voir_mouvements_caisse', 'Voir les mouvements de caisse', 'caisse'),
            ('faire_depot_caisse', 'Faire un dépôt en caisse', 'caisse'),
            ('faire_retrait_caisse', 'Faire un retrait de caisse', 'caisse'),
            ('cloturer_caisse', 'Clôturer la caisse en fin de journée', 'caisse'),

            # 📈 ANALYSE (pour analystes crédit)
            ('analyser_credit', 'Analyser les demandes de crédit', 'analyse'),
            ('voir_scoring', 'Voir le scoring des clients', 'analyse'),
            ('proposer_credit', 'Proposer des crédits', 'analyse'),
            ('voir_historique_client', 'Voir l\'historique complet du client', 'analyse'),

            # 🎯 GROUPES (pour gestionnaires de groupes)
            ('creer_groupe', 'Créer un groupe de clients', 'groupes'),
            ('gerer_groupe', 'Gérer les groupes de clients', 'groupes'),
            ('voir_groupes', 'Voir les groupes', 'groupes'),
            ('animer_groupe', 'Animer les réunions de groupe', 'groupes'),

            # 🚗 TERRAIN (pour agents terrain)
            ('planifier_visite', 'Planifier des visites terrain', 'terrain'),
            ('enregistrer_visite', 'Enregistrer une visite', 'terrain'),
            ('voir_tournee', 'Voir sa tournée', 'terrain'),
            ('collecter_paiement', 'Collecter des paiements sur le terrain', 'terrain'),

            # 🔐 ADMINISTRATION
            ('gerer_utilisateurs', 'Gérer les utilisateurs', 'admin'),
            ('voir_logs', 'Voir les logs système', 'admin'),
            ('configurer_systeme', 'Configurer le système', 'admin'),
            ('sauvegarder_donnees', 'Sauvegarder les données', 'admin'),
            ('restaurer_donnees', 'Restaurer les données', 'admin'),

            # 📋 CONFORMITÉ (pour agents conformité)
            ('verifier_kyc', 'Vérifier les documents KYC', 'conformite'),
            ('voir_alertes_conformite', 'Voir les alertes de conformité', 'conformite'),
            ('traiter_alerte', 'Traiter une alerte de conformité', 'conformite'),
            ('exporter_rapports_conformite', 'Exporter les rapports de conformité', 'conformite'),

            # 📚 FORMATION
            ('voir_formations', 'Voir les formations disponibles', 'formation'),
            ('participer_formation', 'Participer à une formation', 'formation'),
            ('creer_formation', 'Créer une formation', 'formation'),
            ('evaluer_formation', 'Évaluer une formation', 'formation'),
        ]

        for nom, description, categorie in permissions_data:
            permission = cls.query.filter_by(nom=nom).first()
            if not permission:
                permission = cls(
                    nom=nom,
                    description=description,
                    categorie=categorie
                )
                db.session.add(permission)

        db.session.commit()
        print(f"✅ {len(permissions_data)} permissions initialisées")




class Journal(db.Model):
    __tablename__ = 'journal'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    # === INFORMATIONS DE L'ACTION ===
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)  # 'CREATION_PRET', 'APPROBATION', etc.
    details = db.Column(db.Text, nullable=True)

    # === MÉTADONNÉES ===
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 peut aller jusqu'à 45 caractères
    user_agent = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # === LIENS VERS LES OBJETS CONCERNÉS ===
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    pret_id = db.Column(db.Integer, db.ForeignKey('prets.id'), nullable=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=True)

    # === RELATIONS ===
    user = db.relationship('User', foreign_keys=[employe_id], backref='actions_journal')
    client = db.relationship('Client', foreign_keys=[client_id], backref='actions_journal')
    pret = db.relationship('Pret', foreign_keys=[pret_id], backref='actions_journal')
    document = db.relationship('Document', foreign_keys=[document_id], backref='actions_journal')
    date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Journal {self.id}: {self.action} - {self.timestamp.strftime("%d/%m/%Y %H:%M")}>'

    @classmethod
    def ajouter(cls, employe_id, action, details=None, ip_address=None, user_agent=None,
                client_id=None, pret_id=None, document_id=None):
        """Ajoute une entrée dans le journal"""
        entry = cls(
            employe_id=employe_id,
            action=action,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            client_id=client_id,
            pret_id=pret_id,
            document_id=document_id
        )
        db.session.add(entry)
        db.session.commit()
        return entry

    @classmethod
    def get_by_user(cls, employe_id, limit=50):
        """Récupère les actions d'un utilisateur"""
        return cls.query.filter_by(employe_id=employe_id).order_by(cls.timestamp.desc()).limit(limit).all()

    @classmethod
    def get_by_client(cls, client_id, limit=50):
        """Récupère les actions concernant un client"""
        return cls.query.filter_by(client_id=client_id).order_by(cls.timestamp.desc()).limit(limit).all()

    @classmethod
    def get_by_pret(cls, pret_id, limit=50):
        """Récupère les actions concernant un prêt"""
        return cls.query.filter_by(pret_id=pret_id).order_by(cls.timestamp.desc()).limit(limit).all()

    @classmethod
    def get_recent(cls, limit=100):
        """Récupère les actions récentes"""
        return cls.query.order_by(cls.timestamp.desc()).limit(limit).all()





class Client(db.Model):
    __tablename__ = 'clients'
    __table_args__ = {'extend_existing': True}

    cree_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    id = db.Column(db.Integer, primary_key=True)
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    id_client = db.Column(db.String(200), unique=True)
    nom = db.Column(db.String(500))
    prenom = db.Column(db.String(500))
    nom_complet = db.Column(db.String(500))
    sexe = db.Column(db.String(100), nullable=True)
    telephone = db.Column(db.String(200))
    email = db.Column(db.String(200))
    adresse = db.Column(db.Text)
    cin = db.Column(db.String(500))
    date_naissance = db.Column(db.DateTime)
    profession = db.Column(db.String(1000))
    revenu_mensuel = db.Column(db.Float)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)

    statut = db.Column(db.String(200), default='actif')
    mot_de_passe_hash = db.Column(db.String(2550))
    groupe_id = db.Column(db.Integer)
    terms_accepted = db.Column(db.Boolean, default=False)
    terms_accepted_at = db.Column(db.DateTime, nullable=True)
    compte_actif = db.Column(db.Boolean, default=True)

    user = db.relationship('User', backref='client_profile', foreign_keys=[employe_id])

    terms_signature_ip = db.Column(db.String(450))
    terms_signature_user_agent = db.Column(db.Text)
    terms_signature_hash = db.Column(db.String(256))

    # ------------------- Champs pour vérification faciale annuelle -------------------
    selfie_reference = db.Column(db.Text)  # Selfie principal de référence
    photo_face_left = db.Column(db.Text) # Face côté gauche
    photo_face_right = db.Column(db.Text) # Face côté droit
    photo_id_verified = db.Column(db.Boolean, default=False)  # ID vérifié
    photo_id= db.Column(db.Boolean, default=False)  # ID vérifié
    photo_face = db.Column(db.Text)  # Photo recto
    photo_dos = db.Column(db.Text)  # Photo verso
    photo_selfie = db.Column(db.Text)
    verification_next_due = db.Column(db.DateTime)  # Date prochaine vérification annuelle
    selfie_last_verification = db.Column(db.DateTime)  # Date dernière vérification
    blocked_until_verification = db.Column(db.Boolean, default=False)  # Bloquer transactions
    notification_sent = db.Column(db.Boolean, default=False)  # Notification annuelle envoyée

    role = db.Column(db.String(20), default='client')  # client, employe, admin, superviseur

    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=False)

    # Relation
    succursale = db.relationship('Succursale', foreign_keys=[succursale_id], backref='clients')

    # Nouveaux champs à ajouter
    email_confirme = db.Column(db.Boolean, default=False)
    date_confirmation_email = db.Column(db.DateTime, nullable=True)
    a_un_pret_actif = db.Column(db.Boolean, default=False)
    compte_suspendu = db.Column(db.Boolean, default=False)
    raison_suspension = db.Column(db.String(200), nullable=True)
    date_suspension = db.Column(db.DateTime, nullable=True)

    # ✅ CHAMPS AJOUTÉS (nécessaires pour votre formulaire)
    # Informations personnelles complémentaires
    lieu_naissance = db.Column(db.String(1000), nullable=True)
    nationalite = db.Column(db.String(500), default='Haïtienne')
    autre_nationalite = db.Column(db.String(500), nullable=True)
    cin_nif = db.Column(db.String(500), unique=True, nullable=True)  # Alternative à cin

    # Adresse détaillée
    commune = db.Column(db.String(1000), nullable=True)
    departement = db.Column(db.String(500), nullable=True)
    duree_adresse = db.Column(db.Integer, nullable=True)  # en années

    # Situation familiale
    etat_civil = db.Column(db.String(200), nullable=True)  # celibataire, marie, union_libre, divorce
    nom_conjoint = db.Column(db.String(100), nullable=True)
    nb_enfants = db.Column(db.Integer, default=0)

    # Informations professionnelles
    entreprise = db.Column(db.String(100), nullable=True)
    adresse_travail = db.Column(db.String(200), nullable=True)
    tel_travail = db.Column(db.String(200), nullable=True)
    autres_revenus = db.Column(db.Text, nullable=True)

    # Informations financières
    depenses_mensuelles = db.Column(db.Float, default=0)
    capacite_remboursement = db.Column(db.Float, default=0)

    # Gestion des tokens
    token_signature = db.Column(db.Text, nullable=True)
    date_expiration_token = db.Column(db.DateTime, nullable=True)

    # ✅ Ajoute ces champs si nécessaire
    verification_faciale = db.Column(db.Boolean, default=False)
    score_verification = db.Column(db.Float, default=0)
    date_envoi_terms = db.Column(db.DateTime, nullable=True)
    solde = db.Column(db.Float, default=0.0)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    numero_compte = db.Column(db.String(500), unique=True)

    date_signature_terms = db.Column(db.DateTime, nullable=True)

    ville = db.Column(db.String(1000), nullable=True)  # ✅ Le champ doit exister
    code_postal = db.Column(db.String(1000), nullable=True)  # ✅ Le champ doit exister
    # Dans votre modèle Client

    @property
    def statut_affichage(self):

        prets_impayes = Pret.query.filter(
            Pret.client_id == self.id,
            Pret.balance > 0
        ).count()

        if prets_impayes > 0:
            return "Suspendu"

        return "Actif"





    # Relations

    def __repr__(self):
        return f'<Client {self.id}: {self.nom} {self.prenom}>'

    def verifier_peut_demander_pret(self):
        """Vérifie si le client peut demander un nouveau prêt"""
        if self.statut != 'actif':
            return False, "Votre compte n'est pas actif. Veuillez contacter votre agence."

        if not self.email_confirme:
            return False, "Veuillez confirmer votre adresse email avant de demander un prêt."

        if not self.terms_accepted:
            return False, "Vous devez accepter les conditions d'utilisation."

        if self.compte_suspendu:
            return False, f"Votre compte est suspendu. Raison : {self.raison_suspension or 'Non spécifiée'}"

        if self.a_un_pret_actif:
            return False, "Vous avez déjà un prêt en cours. Vous ne pouvez faire que des dépôts jusqu'au remboursement complet."

        return True, "OK"



    def verifier_peut_demander_pret(self):
        """Vérifie si le client peut demander un nouveau prêt"""
        if self.statut != 'actif':
            return False, "Votre compte n'est pas actif. Veuillez contacter votre agence."

        if not self.email_confirme:
            return False, "Veuillez confirmer votre adresse email avant de demander un prêt."

        if not self.terms_accepted:
            return False, "Vous devez accepter les conditions d'utilisation."

        if self.compte_suspendu:
            return False, f"Votre compte est suspendu. Raison : {self.raison_suspension or 'Non spécifiée'}"

        if self.a_un_pret_actif:
            return False, "Vous avez déjà un prêt en cours. Vous ne pouvez faire que des dépôts jusqu'au remboursement complet."

        return True, "OK"

    def suspendre_compte_pret(self):
        """Suspend le compte après l'octroi d'un prêt"""
        self.a_un_pret_actif = True
        self.compte_suspendu = False
        self.raison_suspension = "Prêt en cours - Opérations limitées aux dépôts uniquement"
        self.date_suspension = datetime.utcnow()
        self.statut = 'suspendu'


    def definir_mot_de_passe(self, mot_de_passe):
        self.mot_de_passe_hash = generate_password_hash(mot_de_passe)

    def verifier_mot_de_passe(self, mot_de_passe):
        return check_password_hash(self.mot_de_passe_hash, mot_de_passe)

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.statut == 'actif'

    @property
    def is_anonymous(self):
        return False


class Groupe(db.Model):
    __tablename__ = 'groupes'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    code_groupe = db.Column(db.String(20), unique=True)
    zone = db.Column(db.String(100))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.String(20), default='actif')
    responsable_id = db.Column(db.Integer)

    succursale_id = db.Column(
        db.Integer,
        db.ForeignKey('succursale.id'),
        nullable=True
    )

    succursale = db.relationship(
        'Succursale',
        backref='groupes'
    )

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.statut == 'actif'

    @property
    def is_anonymous(self):
        return False


class Pret(db.Model):
    __tablename__ = 'prets'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    groupe_id = db.Column(db.Integer)
    montant = db.Column(db.Float, default=0)
    taux_interet = db.Column(db.Float)
    duree_mois = db.Column(db.Integer)
    date_demande = db.Column(db.DateTime, default=datetime.utcnow)
    date_approbation = db.Column(db.DateTime)
    statut = db.Column(db.String(200), default='en_attente')
    motif = db.Column(db.String(100))
    montant_interet = db.Column(db.Float)
    montant_total = db.Column(db.Float)
    montant_rembourse = db.Column(db.Float, default=0)
    penalite = db.Column(db.Float, default=0)
    mensualite = db.Column(db.Float)
    actif = db.Column(db.Boolean, default=True)
    type_pret = db.Column(db.String(50), default='classique')
    autre_type_pret = db.Column(db.String(50), default='classique')
    garantie = db.Column(db.String(200), nullable=True)
    info_garant = db.Column(db.String(200), nullable=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # ← avec un 's'
    solde_restant = db.Column(db.Float, default=0)

    reference1 = db.Column(db.String(255), nullable=True)
    reference2 = db.Column(db.String(255), nullable=True)
    telephone_reference1 = db.Column(db.String(50), nullable=True)
    telephone_reference2 = db.Column(db.String(50), nullable=True)
    signature = db.Column(db.Text, nullable=True)

    numero_dossier = db.Column(db.VARCHAR(250), unique=True)

    derniere_activite = db.Column(db.DateTime, nullable=True)

    # ===== AJOUTEZ CES COLONNES =====
    date_reception = db.Column(db.DateTime, nullable=True)
    date_debut = db.Column(db.DateTime, nullable=True)
    date_creation = db.Column(db.DateTime, nullable=True)
    decision = db.Column(db.String(50), nullable=True)  # approuve, refuse, en_attente
    montant_demande = db.Column(db.Float, nullable=True)
    montant_accorde = db.Column(db.Float, nullable=True)
    signature_responsable = db.Column(db.String(25500), nullable=True)
    motif_refus = db.Column(db.Text, nullable=True)
    numero_pret = db.Column(db.VARCHAR(50), unique=True)  # ou db.VARCHAR(50)
    date_echeance = db.Column(db.DateTime)  # ← Ajouter cette ligne
    date_decaissement = db.Column(db.DateTime, nullable=True)  # ← ADD THIS LINE

    conditions_acceptees = db.Column(db.Boolean, default=False, nullable=False)
    date_signature = db.Column(db.DateTime, nullable=True)
    signature_client = db.Column(db.Text, nullable=True)
    ip_signature = db.Column(db.String(250), nullable=True)
    prochaine_echeance = db.Column(db.Date, nullable=True)


    client = db.relationship('Client', foreign_keys=[client_id], backref='prets_contractes')

    agent = db.relationship('User', foreign_keys=[agent_id], backref='prets_geres')



    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=False)

    succursale = db.relationship('Succursale', foreign_keys=[succursale_id],
                                 backref='prets_list', overlaps='succursale_rel')

    # succursale = db.relationship("Succursale", back_populates="prets")

    code_pret = db.Column(db.String(20))  # BR001-PR001



    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def generate_echeancier(self):
        """Generate payment schedule for the loan"""
        from datetime import timedelta
        from dateutil.relativedelta import relativedelta

        # Delete existing schedule
        Echeancier.query.filter_by(pret_id=self.id).delete()

        monthly_payment = self.mensualite
        current_date = datetime.now().date() + relativedelta(months=1)

        for i in range(1, self.duree_mois + 1):
            echeance = Echeancier(
                pret_id=self.id,
                numero_echeance=i,
                date_echeance=current_date,
                montant=monthly_payment
            )
            db.session.add(echeance)
            current_date += relativedelta(months=1)

        db.session.commit()

    def get_payment_status(self):
        """Get overall payment status"""
        echeanciers = Echeancier.query.filter_by(pret_id=self.id).all()

        if not echeanciers:
            return {
                'total': 0,
                'paid': 0,
                'pending': 0,
                'overdue': 0,
                'total_paid': 0,
                'remaining': self.montant_total,
                'progress': 0
            }

        total = len(echeanciers)
        paid = sum(1 for e in echeanciers if e.statut == 'paye')
        pending = sum(1 for e in echeanciers if e.statut == 'en_attente')
        overdue = sum(1 for e in echeanciers if e.statut == 'impaye')
        total_paid = sum(e.montant_paye for e in echeanciers)

        return {
            'total': total,
            'paid': paid,
            'pending': pending,
            'overdue': overdue,
            'total_paid': total_paid,
            'remaining': self.montant_total - total_paid,
            'progress': (total_paid / self.montant_total * 100) if self.montant_total > 0 else 0
        }

    def check_overdue_payments(self):
        """Check and update overdue payments"""
        today = date.today()
        echeanciers = Echeancier.query.filter(
            Echeancier.pret_id == self.id,
            Echeancier.statut.in_(['en_attente', 'partiel']),
            Echeancier.date_echeance < today
        ).all()

        for echeance in echeanciers:
            echeance.statut = 'impaye'
            echeance.calculate_penalty(today)

        if echeanciers:
            db.session.commit()

        return len(echeanciers)

    @property
    def solde_restant(self):
        """Calcule le solde restant du prêt"""
        from sqlalchemy import func
        total_rembourse = db.session.query(func.sum(Remboursement.montant)).filter_by(
            pret_id=self.id, statut='effectue'
        ).scalar() or 0
        return self.montant - total_rembourse  # Utilisez montant au lieu de montant_total



class ReferenceClient(db.Model):
    __tablename__ = "references_clients"

    id = db.Column(db.Integer, primary_key=True)

    pret_id = db.Column(
        db.Integer,
        db.ForeignKey("prets.id"),
        nullable=False
    )

    nom_complet = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(50), nullable=False)
    adresse = db.Column(db.String(255), nullable=True)
    profession = db.Column(db.String(150), nullable=True)
    relation = db.Column(db.String(100), nullable=True)

    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    pret = db.relationship(
        "Pret",
        backref=db.backref("references", lazy=True, cascade="all, delete-orphan")
    )


class Paiement(db.Model):
    __tablename__ = 'paiements'

    id = db.Column(db.Integer, primary_key=True)
    credit_id = db.Column(db.Integer, db.ForeignKey('credits.id'), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    date_paiement = db.Column(db.DateTime, default=datetime.utcnow)
    mode_paiement = db.Column(db.String(50))  # 'especes', 'virement', 'mobile_money'
    reference = db.Column(db.String(100))
    statut = db.Column(db.String(20), default='valide')  # 'valide', 'annule', 'en_attente'
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    interet = db.Column(db.Float, default=0)

    # Relations
    credit = db.relationship('Credit', backref='paiements', lazy=True,)
    utilisateur = db.relationship('User', backref='paiements_effectues', lazy=True,)

    def __repr__(self):
        return f'<Paiement {self.id}: {self.montant} HTG>'

class Remboursement(db.Model):
    __tablename__ = 'remboursements'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    pret_id = db.Column(db.Integer, db.ForeignKey('prets.id'), nullable=False)
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    montant = db.Column(db.Float)
    date_remboursement = db.Column(db.DateTime, default=datetime.utcnow)
    date_echeance = db.Column(db.DateTime)
    statut = db.Column(db.String(200), default='en_attente')
    type_paiement = db.Column(db.String(20))
    methode =  db.Column(db.String(20))
    reference = db.Column(db.String(20))
    date = db.Column(db.DateTime)

    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=False)

    # ✅ Ajoute les relations
    pret = db.relationship('Pret', backref='remboursements')
    client = db.relationship('User', foreign_keys=[client_id], backref='remboursements_effectues')
    succursale = db.relationship('Succursale', back_populates='remboursements')
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=False)




class Employe(db.Model):
    __tablename__ = 'employes'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    # matricule = db.Column(db.String(20), unique=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    email = db.Column(db.String(120))
    telephone = db.Column(db.String(20))
    poste = db.Column(db.String(100))
    date_embauche = db.Column(db.DateTime)
    statut = db.Column(db.String(200), default='en_attente')  # ← Modifier 'actif' en 'en_attente'
    mot_de_passe_hash = db.Column(db.String(255))
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=False)
    entreprise_id = db.Column(db.Integer, db.ForeignKey("entreprises.id"))
    actif = db.Column(db.Boolean, default=False)

    # AJOUTER CES CHAMPS MANQUANTS :
    role = db.Column(db.String(50))  # ← AJOUTER
    niveau_habilitation = db.Column(db.Integer, default=1)  # ← AJOUTER
    derniere_activite = db.Column(db.DateTime)  # ← AJOUTER
    verifications_completes = db.Column(db.Boolean, default=False)  # ← AJOUTER
    formation_aml_cft = db.Column(db.Boolean, default=False)  # ← AJOUTER




    def definir_mot_de_passe(self, mot_de_passe):
        self.mot_de_passe_hash = generate_password_hash(mot_de_passe)

    def verifier_mot_de_passe(self, mot_de_passe):
        return check_password_hash(self.mot_de_passe_hash, mot_de_passe)

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.statut == 'actif'

    @property
    def is_anonymous(self):
        return False

        # AJOUTER CETTE PROPRIÉTÉ POUR nom_complet :

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"





class LoanRecommendationController:
    """Contrôleur pour les recommandations de prêt"""

    def __init__(self, page, api_base_url=None, token=None):
        self.page = page
        self.api_base_url = api_base_url or "https://api.gmes.com/v1"
        self.token = token

        def show_loan_recommendation(self, e=None):
            """Recommandations de prêt personnalisées"""
            try:
                headers = {"Authorization": f"Bearer {self.token}"}
                response = requests.get(f"{self.api_base_url}/recommandations-pret", headers=headers)

                if response.status_code == 200:
                    data = response.json()

                    view = ft.Column([
                        ft.Row([
                            ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: self.show_dashboard()),
                            ft.Text("Recommandations", size=20, weight=ft.FontWeight.BOLD)
                        ]),

                        # Score de crédit
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Text("🎯 Score de Crédit", size=18, weight=ft.FontWeight.BOLD),
                                        ft.Container(
                                            content=ft.Text(
                                                f"{data['score']}/850",
                                                color=ft.colors.WHITE,
                                                weight=ft.FontWeight.BOLD
                                            ),
                                            bgcolor=self.get_score_color(data['score']),
                                            padding=10,
                                            border_radius=20
                                        )
                                    ]),
                                    ft.Text(f"Catégorie: {data['categorie']}"),

                                    # Facteurs d'influence
                                    ft.Text("Facteurs influençant votre score:", size=14, weight=ft.FontWeight.BOLD),
                                    *[ft.Text(f"• {factor}") for factor in data['facteurs']]
                                ]),
                                padding=20
                            )
                        ),

                        # Prêts recommandés
                        ft.Text("Prêts Recommandés", size=16, weight=ft.FontWeight.BOLD),
                        *[self.create_loan_recommendation_card(pret) for pret in data['prets_recommandes']],

                        # Améliorer son score
                        ft.ExpansionTile(
                            title=ft.Text("💡 Comment améliorer votre score?"),
                            controls=[
                                ft.ListTile(title=ft.Text("• Effectuez vos remboursements à temps")),
                                ft.ListTile(title=ft.Text("• Maintenez une activité régulière")),
                                ft.ListTile(title=ft.Text("• Évitez les retards de paiement")),
                                ft.ListTile(title=ft.Text("• Diversifiez vos sources de revenus")),
                            ]
                        )
                    ])

                    self.page.clean()
                    self.page.add(view)

            except Exception as e:
                self.show_error(f"Erreur: {str(e)}")


        def get_score_color(self, score):
            """Couleur selon le score"""
            if score >= 750:
                return ft.colors.GREEN
            elif score >= 650:
                return ft.colors.BLUE
            elif score >= 550:
                return ft.colors.ORANGE
            else:
                return ft.colors.RED


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    employe_id = db.Column(db.Integer)
    pret_id = db.Column(db.Integer)


    montant = db.Column(db.Float)
    gateway = db.Column(db.String(20))  # moncash, natcash, etc.
    transaction_id = db.Column(db.String(100))  # ID de la transaction du gateway
    statut = db.Column(db.String(200), default='en_attente')  # en_attente, paye, echoue
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_confirmation = db.Column(db.DateTime)
    metadata_info = db.Column(db.Text)  # Données supplémentaires au format JSON
    date = db.Column(db.DateTime)
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'))


class Retrait(db.Model):
    __tablename__ = 'retraits'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    compte_epargne_id = db.Column(db.Integer, db.ForeignKey('epargnes.id'), nullable=False)
    montant = db.Column(db.Numeric(15, 2), nullable=False)
    mode_retrait = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    signature_data = db.Column(db.Text)  # Stockage de la signature en base64
    date_retrait = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.String(50), default='effectue')
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'))

    # Relations
    client = db.relationship('Client', backref='retraits')
    compte = db.relationship('Epargne', backref='retraits')
    transaction = db.relationship('Transaction', backref='retrait_associe')

class Credit(db.Model):
    __tablename__ = 'credits'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approuve_par = db.Column(db.Integer, db.ForeignKey('users.id'))

    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'))

    succursale = db.relationship('Succursale', backref='credits', foreign_keys=[succursale_id])

    # ➕ AJOUTEZ CETTE LIGNE (la clé étrangère manquante)
    produit_id = db.Column(db.Integer, db.ForeignKey('produits.id'), nullable=True)

    # Informations financières
    montant = db.Column(db.Float, nullable=False)
    taux_interet = db.Column(db.Float, nullable=False, default=0)
    duree_mois = db.Column(db.Integer, nullable=False)
    montant_restant = db.Column(db.Float, default=0)
    montant_total_du = db.Column(db.Float)

    # Dates
    date_demande = db.Column(db.DateTime, default=datetime.utcnow)
    date_approbation = db.Column(db.DateTime)
    date_debut = db.Column(db.DateTime)
    date_fin = db.Column(db.DateTime)

    # Statut
    statut = db.Column(db.String(200), default='en_attente')

    # Autres champs
    objet = db.Column(db.String(200))
    garantie = db.Column(db.String(200))
    notes = db.Column(db.Text)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relations - CORRECTION ICI : utiliser 'paiements' au lieu de 'paiements'
    client = db.relationship('Client', backref=db.backref('credits_client', lazy='dynamic'))
    agent = db.relationship('User', foreign_keys=[agent_id], backref='credits_agent')
    approbateur = db.relationship('User', foreign_keys=[approuve_par], backref='credits_approuves')

    # La relation avec Paiement - on utilise un nom différent
    # Ne pas utiliser 'paiements' car c'est déjà utilisé ailleurs
    # credit_paiements = db.relationship('Paiement', backref='credit_rel', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        super(Credit, self).__init__(*args, **kwargs)
        if self.montant and self.taux_interet and self.duree_mois:
            self.calculer_montant_total()
            self.montant_restant = self.montant_total_du

    def calculer_montant_total(self):
        interets = self.montant * (self.taux_interet / 100) * (self.duree_mois / 12)
        self.montant_total_du = self.montant + interets
        return self.montant_total_du

    @property
    def montant_rembourse(self):
        """Calcule le montant total déjà remboursé"""
        total = db.session.query(db.func.sum(Paiement.montant)).filter_by(credit_id=self.id).scalar()
        return total or 0

    @property
    def progression(self):
        if self.montant_total_du > 0:
            return (self.montant_rembourse / self.montant_total_du) * 100
        return 0

    @property
    def nombre_paiements(self):
        """Retourne le nombre de paiements effectués"""
        return Paiement.query.filter_by(credit_id=self.id).count()

    def __repr__(self):
        return f'<Credit {self.id}: {self.montant} HTG - {self.statut}>'
# models.py - Ajoutez cette fonction AVANT la classe User (ligne ~10)

def generate_carte_numero():
    """Génère un numéro de carte unique"""
    import random
    import string
    # Format: GMES-XXXX-XXXX
    return f"GMES-{''.join(random.choices(string.ascii_uppercase + string.digits, k=4))}-{''.join(random.choices(string.digits, k=4))}"




class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Qui a fait l'action
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_name = db.Column(db.String(200))
    user_role = db.Column(db.String(50))

    # Où l'action a été faite
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'))
    succursale_nom = db.Column(db.String(100))

    # Quoi a été fait
    action = db.Column(db.String(100))  # 'create', 'update', 'delete', 'login', etc.
    module = db.Column(db.String(100))  # 'employe', 'pret', 'client', 'succursale'
    details = db.Column(db.Text)  # Détails JSON de l'action

    # IP et user agent pour sécurité
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.Text)

    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AuditLog {self.user_name} - {self.action} - {self.timestamp}>'

class AuditOperation(db.Model):
    __tablename__ = "audit_operations"

    id = db.Column(db.Integer, primary_key=True)

    utilisateur_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    type_operation = db.Column(db.String(50))

    reference = db.Column(db.String(100))

    montant = db.Column(db.Float)

    ancien_solde = db.Column(db.Float)

    nouveau_solde = db.Column(db.Float)

    adresse_ip = db.Column(db.String(100))

    appareil = db.Column(db.String(255))

    date_operation = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    resultat = db.Column(
        db.String(20),
        default="SUCCES"
    )


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # ← AJOUT foreign key
    acteur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Qui a déclenché
    titre = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type_notification = db.Column(db.String(50))  # ← Gardez celui-ci
    type = db.Column(db.String(20), default='info')  # success, danger, warning, info
    # SUPPRIMEZ la ligne "type" en double
    lue = db.Column(db.Boolean, default=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    lien = db.Column(db.String(500))
    date_envoi = db.Column(db.DateTime, default=datetime.now)
    date_lecture = db.Column(db.DateTime)
    action_id = db.Column(db.Integer, db.ForeignKey('actions.id'), nullable=False)
    destinataire_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    level = db.Column(db.String(20), default='error')  # error, warning, info, success
    url = db.Column(db.String(500))  # Lien pour voir les détails
    read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    error_id = db.Column(db.Integer)  # Pour lier à l'erreur originale

    # ========== COLONNES AJOUTÉES (SANS CASSER L'EXISTANT) ==========
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)  # Ajout client
    pret_id = db.Column(db.Integer, db.ForeignKey('prets.id'), nullable=True)  # Ajout prêt
    requires_action = db.Column(db.Boolean, default=False)  # Notification nécessite une action
    is_read = db.Column(db.Boolean, default=False)  # Alternative à 'lue' (vos méthodes existent déjà)
    read_at = db.Column(db.DateTime, nullable=True)  # Alternative à 'date_lecture'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Alternative à 'date_creation'

    niveau = db.Column(db.String(20), default='info')  # info, success, warning, danger
    # ================================================================

    # Relations
    user = db.relationship('User', foreign_keys=[employe_id], backref='notifications_envoyees')
    action = db.relationship('Action', backref='notifications')
    # ✅ Utilisez plutôt ceci (SANS backref)
    destinataire = db.relationship('User', foreign_keys=[destinataire_id])
    acteur = db.relationship('User', foreign_keys=[acteur_id])

    # ========== RELATIONS AJOUTÉES ==========
    client = db.relationship('Client', foreign_keys=[client_id],
                             backref='notifications')  # Déjà présent mais client_id manquait
    pret = db.relationship('Pret', foreign_keys=[pret_id],
                           backref='notifications')  # Déjà présent mais pret_id manquait

    # =======================================

    def __repr__(self):
        return f'<Notification {self.id}: {self.titre}>'

    def marquer_lue(self):
        """Marque la notification comme lue"""
        self.lue = True
        self.date_lecture = datetime.now()
        db.session.commit()

    # ========== MÉTHODES AJOUTÉES (OPTIONNELLES, SANS CASSER) ==========
    def mark_as_read(self):
        """Méthode alternative pour marquer comme lu"""
        if not self.lue:
            self.marquer_lue()
        # Met aussi à jour les nouveaux champs si présents
        if hasattr(self, 'is_read'):
            self.is_read = True
        if hasattr(self, 'read_at'):
            self.read_at = datetime.now()
        db.session.commit()

    @property
    def est_lue(self):
        """Getter unifié pour l'état de lecture"""
        return self.lue or (hasattr(self, 'is_read') and self.is_read)
    # ================================================================

class CreerGroupeForm(FlaskForm):
    nom = StringField('Nom du groupe', validators=[DataRequired(), Length(min=2, max=100)])
    type_groupe = SelectField('Type de groupe', choices=[
        ('solidaire', 'Groupe Solidaire'),
        ('rotatif', 'Tontine Rotative'),
        ('epargne', 'Groupe d\'Épargne'),
        ('credit', 'Groupe de Crédit'),
        ('mixte', 'Groupe Mixte')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    nombre_membres = IntegerField('Nombre de membres', validators=[DataRequired()])
    montant_cotisation = DecimalField('Montant de cotisation', validators=[DataRequired()])
    frequence_cotisation = SelectField('Fréquence de cotisation', choices=[
        ('quotidienne', 'Quotidienne'),
        ('hebdomadaire', 'Hebdomadaire'),
        ('mensuelle', 'Mensuelle'),
        ('trimestrielle', 'Trimestrielle'),
        ('annuelle', 'Annuelle')
    ], validators=[DataRequired()])
    date_creation = DateField('Date de création', validators=[DataRequired()])
    responsable_id = SelectField('Responsable', coerce=int, validators=[DataRequired()])
    objectif = TextAreaField('Objectif', validators=[Optional(), Length(max=300)])
    reglement_interieur = TextAreaField('Règlement intérieur', validators=[Optional(), Length(max=1000)])
    adresse = StringField('Adresse', validators=[Optional(), Length(max=200)])
    ville = StringField('Ville', validators=[Optional(), Length(max=50)])
    est_actif = BooleanField('Groupe actif', default=True)


class Succursale(db.Model):
    __tablename__ = 'succursale'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)  # BR001, BR002, ...
    nom = db.Column(db.String(100), nullable=False)
    ville = db.Column(db.String(100))
    adresse = db.Column(db.Text)
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    directeur_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.String(20), default='active')
    active = db.Column(db.Boolean, default=True)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    rayon = db.Column(db.Integer)  # en mètres (ex: 100m)

    entreprise_id = db.Column(db.Integer, db.ForeignKey("entreprises.id"))

    # Relations
    directeur = db.relationship('User', foreign_keys=[directeur_id])

    # ✅ RELATION UNIQUE pour tous les utilisateurs de la succursale
    # users = db.relationship('User',
    #                         foreign_keys='User.succursale_id',
    #                         back_populates='succursale',
    #                         primaryjoin="Succursale.id == User.succursale_id")

    # ✅ RELATION vers User
    users = db.relationship('User',
                            foreign_keys='User.succursale_id',
                            back_populates='succursale')

    # ✅ Relation pour les employés (filtre par rôle)
    employes = db.relationship('User',
                               foreign_keys='User.succursale_id',
                               primaryjoin="and_(Succursale.id == User.succursale_id, User.role.in_(['employe', 'superviseur']))",
                               viewonly=True,
                               overlaps='users')


    prets = db.relationship('Pret', back_populates='succursale',
                            foreign_keys='Pret.succursale_id', overlaps='prets_list')

    remboursements = db.relationship('Remboursement',
                                     back_populates='succursale',
                                     foreign_keys='Remboursement.succursale_id')



class HistoriqueEmploye(db.Model):
    __tablename__ = 'historique_employes'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    modifie_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    employe_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    # Type d'action
    action = db.Column(db.String(50),
                       nullable=False)  # 'creation', 'modification', 'promotion', 'suspension', 'reactivation', 'depart'

    # Anciennes et nouvelles valeurs (stockées en JSON)
    anciennes_valeurs = db.Column(db.JSON, nullable=True)
    nouvelles_valeurs = db.Column(db.JSON, nullable=True)

    # Métadonnées
    date_action = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 peut faire 45 caractères
    description = db.Column(db.String(255), nullable=True)

    # Relations
    # ✅ Relation employé (à garder comme ça)
    employe = db.relationship(
        "User",
        foreign_keys=[employe_id],
        backref="historique_employes"
    )


    modifie_par = db.relationship("User",foreign_keys=[modifie_par_id],back_populates="modifications_effectuees")

    def __repr__(self):
        return f'<HistoriqueEmploye {self.id}: {self.action} - {self.date_action}>'

    @classmethod
    def enregistrer_creation(cls, employe,employe_id, modifie_par, ip_address=None):
        """Enregistre la création d'un employé"""
        historique = cls(
            employe_id=employe_id,
            modifie_par_id=modifie_par.id,
            action='creation',
            nouvelles_valeurs={
                'username': employe.username,
                'email': employe.email,
                'nom': employe.nom,
                'prenom': employe.prenom,
                'telephone': employe.telephone,
                'role': employe.role,
                'succursale_id': employe.succursale_id,
                'statut': employe.statut
            },
            ip_address=ip_address,
            description=f"Création de l'employé {employe.prenom} {employe.nom}"
        )
        db.session.add(historique)
        return historique

    @classmethod
    def enregistrer_modification(cls, employe,employe_id, modifie_par, anciennes_valeurs, nouvelles_valeurs, ip_address=None):
        """Enregistre une modification d'un employé"""
        # Ne garder que les champs qui ont changé
        changements = {}
        for key, new_value in nouvelles_valeurs.items():
            if key in anciennes_valeurs and anciennes_valeurs[key] != new_value:
                changements[key] = {
                    'ancien': anciennes_valeurs[key],
                    'nouveau': new_value
                }

        if changements:
            historique = cls(
                employe_id=employe_id,
                modifie_par_id=modifie_par.id,
                action='modification',
                anciennes_valeurs=anciennes_valeurs,
                nouvelles_valeurs=nouvelles_valeurs,
                ip_address=ip_address,
                description=f"Modification de l'employé {employe.prenom} {employe.nom}: {', '.join(changements.keys())}"
            )
            db.session.add(historique)
            return historique
        return None

    @classmethod
    def enregistrer_changement_statut(cls, employe, modifie_par, ancien_statut, nouveau_statut, ip_address=None):
        """Enregistre un changement de statut"""
        historique = cls(
            employe_id=employe.id,
            modifie_par_id=modifie_par.id,
            action=f'changement_statut_{nouveau_statut}',
            anciennes_valeurs={'statut': ancien_statut},
            nouvelles_valeurs={'statut': nouveau_statut},
            ip_address=ip_address,
            description=f"Changement de statut de {employe.prenom} {employe.nom}: {ancien_statut} → {nouveau_statut}"
        )
        db.session.add(historique)
        return historique

    @classmethod
    def enregistrer_promotion(cls, employe, modifie_par, ancien_role, nouveau_role, ancienne_fonction,
                              nouvelle_fonction, ip_address=None):
        """Enregistre une promotion ou changement de rôle"""
        historique = cls(
            employe_id=employe.id,
            modifie_par_id=modifie_par.id,
            action='promotion',
            anciennes_valeurs={'role': ancien_role, 'fonction': ancienne_fonction},
            nouvelles_valeurs={'role': nouveau_role, 'fonction': nouvelle_fonction},
            ip_address=ip_address,
            description=f"Promotion de {employe.prenom} {employe.nom}: {ancien_role} → {nouveau_role}"
        )
        db.session.add(historique)
        return historique

    @classmethod
    def enregistrer_depart(cls, employe, modifie_par, date_depart, motif, ip_address=None):
        """Enregistre le départ d'un employé"""
        historique = cls(
            employe_id=employe.id,
            modifie_par_id=modifie_par.id,
            action='depart',
            nouvelles_valeurs={
                'date_depart': date_depart.isoformat() if date_depart else None,
                'motif': motif,
                'statut': 'inactif'
            },
            ip_address=ip_address,
            description=f"Départ de l'employé {employe.prenom} {employe.nom}: {motif}"
        )
        db.session.add(historique)
        return historique


class Pointage(db.Model):
    __tablename__ = 'pointages'

    id = db.Column(db.Integer, primary_key=True)

    # Relations

    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=False)

    # Date
    date = db.Column(db.Date, nullable=False, default=datetime.now().date)

    # Horaires
    heure_arrivee = db.Column(db.DateTime, nullable=True)
    heure_depart = db.Column(db.DateTime, nullable=True)

    # Statut
    present = db.Column(db.Boolean, default=False)
    retard = db.Column(db.Boolean, default=False)
    absence_justifiee = db.Column(db.Boolean, default=False)

    # Type de journée
    type_journee = db.Column(db.String(20), default='normale')  # 'normale', 'teletravail', 'formation', 'mission'

    # Justification
    motif_absence = db.Column(db.String(200), nullable=True)
    justificatif_url = db.Column(db.String(500), nullable=True)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relations
    employe = db.relationship('User', backref='pointages')
    succursale = db.relationship('Succursale', backref='pointages')


    __table_args__ = (
        db.UniqueConstraint('employe_id', 'date', name='unique_pointage_jour'),
    )

    def __repr__(self):
        return f'<Pointage {self.employe_id} - {self.date}>'

    def pointer_arrivee(self):
        """Enregistre l'heure d'arrivée"""
        maintenant = datetime.now()
        self.heure_arrivee = maintenant
        self.date = maintenant.date()

        # Vérifier le retard (après 8h30)
        heure_limite = maintenant.replace(hour=8, minute=30, second=0)
        if maintenant > heure_limite:
            self.retard = True

        self.present = True
        db.session.commit()

    def pointer_depart(self):
        """Enregistre l'heure de départ"""
        self.heure_depart = datetime.now()
        db.session.commit()

    @property
    def heures_travaillees(self):
        """Calcule le nombre d'heures travaillées"""
        if self.heure_arrivee and self.heure_depart:
            duree = self.heure_depart - self.heure_arrivee
            return round(duree.total_seconds() / 3600, 2)
        return 0

    @property
    def minutes_retard(self):
        """Calcule les minutes de retard"""
        if self.heure_arrivee and self.retard:
            heure_limite = self.heure_arrivee.replace(hour=8, minute=30, second=0)
            if self.heure_arrivee > heure_limite:
                retard = self.heure_arrivee - heure_limite
                return int(retard.total_seconds() / 60)
        return 0


class Recrutement(db.Model):
    __tablename__ = 'recrutements'

    id = db.Column(db.Integer, primary_key=True)

    # Informations du poste
    titre = db.Column(db.String(200), nullable=False)
    poste = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    responsabilites = db.Column(db.Text, nullable=True)
    profil_recherche = db.Column(db.Text, nullable=True)

    # Localisation
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=True)

    # Type de contrat
    type_contrat = db.Column(db.String(50))  # 'CDI', 'CDD', 'stage', 'consultant'
    duree_mois = db.Column(db.Integer, nullable=True)  # Pour les CDD

    # Dates
    date_publication = db.Column(db.DateTime, default=datetime.utcnow)
    date_limite = db.Column(db.Date, nullable=False)
    date_debut_souhaitee = db.Column(db.Date, nullable=True)

    # Statut
    statut = db.Column(db.String(20), default='publie')  # 'brouillon', 'publie', 'cloture', 'annule'

    # Rémunération
    salaire_min = db.Column(db.Float, nullable=True)
    salaire_max = db.Column(db.Float, nullable=True)

    # Métadonnées
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    candidatures = db.relationship('Candidature', backref='recrutement', lazy='dynamic')
    succursale = db.relationship('Succursale', backref='recrutements')

    def __repr__(self):
        return f'<Recrutement {self.id}: {self.poste}>'

    @property
    def nb_candidatures(self):
        """Nombre total de candidatures"""
        return self.candidatures.count()

    @property
    def nb_candidatures_nouvelles(self):
        """Nombre de nouvelles candidatures"""
        return self.candidatures.filter_by(statut='nouvelle').count()

    @property
    def jours_restants(self):
        """Jours restants avant la date limite"""
        if self.date_limite:
            delta = (self.date_limite - datetime.now().date()).days
            return max(0, delta)
        return 0

    @property
    def est_urgent(self):
        """Vérifie si le recrutement est urgent"""
        return self.jours_restants <= 7 and self.jours_restants > 0


class Formation(db.Model):
    __tablename__ = 'formations'

    id = db.Column(db.Integer, primary_key=True)

    # Informations de base
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    objectifs = db.Column(db.Text, nullable=True)

    # Type de formation
    type_formation = db.Column(db.String(50), nullable=False)  # 'interne', 'externe', 'en_ligne'
    categorie = db.Column(db.String(50))  # 'technique', 'commercial', 'conformite', 'management'

    # Dates
    date_debut = db.Column(db.DateTime, nullable=False)
    date_fin = db.Column(db.DateTime, nullable=False)
    date_limite_inscription = db.Column(db.DateTime, nullable=True)

    # Lieu
    lieu = db.Column(db.String(200), nullable=True)
    formateur = db.Column(db.String(100), nullable=True)  # Gardez ce champ pour l'affichage

    # Capacité
    capacite_max = db.Column(db.Integer, default=20)
    places_disponibles = db.Column(db.Integer, default=20)

    # Coût
    cout = db.Column(db.Float, default=0)

    # Statut
    statut = db.Column(db.String(20), default='planifiee')  # 'planifiee', 'en_cours', 'terminee', 'annulee'

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # ⚠️ AJOUTEZ D'ABORD CETTE COLONNE ICI ⚠️
    formateur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # <-- À AJOUTER

    # Relations
    participants = db.relationship('FormationParticipant', backref='formation', lazy='dynamic')

    # ENSUITE, ajoutez les relations (après avoir défini toutes les colonnes)
    formateur_user = db.relationship('User', foreign_keys=[formateur_id], backref='formations_enseignees')
    created_by_user = db.relationship('User', foreign_keys=[created_by], backref='formations_crees')

    def __repr__(self):
        return f'<Formation {self.id}: {self.titre}>'

    @property
    def nb_participants(self):
        """Nombre de participants inscrits"""
        return self.participants.count()

    @property
    def progression(self):
        """Calcule la progression de la formation"""
        maintenant = datetime.now()
        if maintenant < self.date_debut:
            return 0
        elif maintenant > self.date_fin:
            return 100
        else:
            total = (self.date_fin - self.date_debut).total_seconds()
            ecoule = (maintenant - self.date_debut).total_seconds()
            return int((ecoule / total) * 100)

    @property
    def est_complet(self):
        """Vérifie si la formation est complète"""
        return self.nb_participants >= self.capacite_max

    def inscrire_participant(self, employe_id):
        """Inscrit un participant à la formation"""
        if not self.est_complet:
            participant = FormationParticipant(
                formation_id=self.id,
                employe_id=employe_id,
                statut='inscrit'
            )
            db.session.add(participant)
            self.places_disponibles -= 1
            db.session.commit()
            return True
        return False

class Produit(db.Model):
    __tablename__ = 'produits'

    id = db.Column(db.Integer, primary_key=True)

    # Informations de base
    code = db.Column(db.String(20), unique=True, nullable=False)  # PRD-001, CRD-CLASSIC, etc.
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # ➕ CLÉ ÉTRANGÈRE AJOUTÉE
    categorie_id = db.Column(db.Integer, db.ForeignKey('categories_produits.id'), nullable=True)

    # Type de produit
    type_produit = db.Column(db.String(50), nullable=False)  # 'credit', 'epargne', 'assurance', 'service'
    # categorie = db.Column(db.String(50), nullable=True)  # 'classique', 'jeune', 'femme', 'agricole', 'PME'

    # Caractéristiques financières
    taux_interet_min = db.Column(db.Float, default=0)  # Taux minimum (%)
    taux_interet_max = db.Column(db.Float, default=0)  # Taux maximum (%)
    montant_min = db.Column(db.Float, default=0)
    montant_max = db.Column(db.Float, default=0)
    duree_min_mois = db.Column(db.Integer, default=1)
    duree_max_mois = db.Column(db.Integer, default=12)

    # Frais et commissions
    frais_dossier = db.Column(db.Float, default=0)  # Montant fixe ou pourcentage
    frais_dossier_type = db.Column(db.String(20), default='fixe')  # 'fixe', 'pourcentage'
    frais_penalite = db.Column(db.Float, default=0)  # Pénalité de retard (%)

    # Conditions d'éligibilité
    age_min = db.Column(db.Integer, default=18)
    age_max = db.Column(db.Integer, default=65)
    revenu_min = db.Column(db.Float, default=0)
    anciennete_min_mois = db.Column(db.Integer, default=0)  # Ancienneté minimum en mois

    # Garanties requises
    garantie_requise = db.Column(db.Boolean, default=False)
    type_garantie = db.Column(db.String(100), nullable=True)  # 'caution', 'hypotheque', 'nantissement'
    taux_garantie = db.Column(db.Float, default=0)  # Pourcentage de couverture

    # Statut et visibilité
    est_actif = db.Column(db.Boolean, default=True)
    est_promotion = db.Column(db.Boolean, default=False)
    date_debut_promotion = db.Column(db.DateTime, nullable=True)
    date_fin_promotion = db.Column(db.DateTime, nullable=True)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relations
    credits = db.relationship('Credit', backref='produit', lazy='dynamic')

    def __repr__(self):
        return f'<Produit {self.code}: {self.nom}>'

    @property
    def nb_souscriptions(self):
        """Nombre de souscriptions à ce produit"""
        return self.credits.count()

    @property
    def montant_total_octroye(self):
        """Montant total octroyé pour ce produit"""
        from sqlalchemy import func
        return db.session.query(func.sum(Credit.montant)).filter(
            Credit.produit_id == self.id
        ).scalar() or 0

    @property
    def en_promotion(self):
        """Vérifie si le produit est en promotion"""
        maintenant = datetime.now()
        if self.est_promotion and self.date_debut_promotion and self.date_fin_promotion:
            return self.date_debut_promotion <= maintenant <= self.date_fin_promotion
        return self.est_promotion

    @property
    def taux_promotionnel(self):
        """Taux promotionnel si applicable"""
        if self.en_promotion:
            return self.taux_interet_min * 0.8  # 20% de réduction
        return self.taux_interet_min

    def est_eligible(self, client):
        """Vérifie si un client est éligible à ce produit"""
        from datetime import date

        # Vérifier l'âge
        if client.date_naissance:
            age = date.today().year - client.date_naissance.year
            if age < self.age_min or age > self.age_max:
                return False, "Âge non éligible"

        # Vérifier le revenu
        if client.revenu_mensuel and client.revenu_mensuel < self.revenu_min:
            return False, "Revenu insuffisant"

        # Vérifier l'ancienneté
        if client.date_inscription:
            anciennete = (date.today() - client.date_inscription.date()).days / 30
            if anciennete < self.anciennete_min_mois:
                return False, "Ancienneté insuffisante"

        return True, "Éligible"

    def calculer_mensualite(self, montant, duree_mois):
        """Calcule la mensualité pour un montant et une durée donnés"""
        if montant < self.montant_min or montant > self.montant_max:
            return None, "Montant hors limites"

        if duree_mois < self.duree_min_mois or duree_mois > self.duree_max_mois:
            return None, "Durée hors limites"

        # Calcul des intérêts
        taux_mensuel = (self.taux_interet_min / 100) / 12
        mensualite = (montant * taux_mensuel * (1 + taux_mensuel) ** duree_mois) / \
                     ((1 + taux_mensuel) ** duree_mois - 1) if taux_mensuel > 0 else montant / duree_mois

        return round(mensualite, 2), None

    def calculer_frais_dossier(self, montant):
        """Calcule les frais de dossier"""
        if self.frais_dossier_type == 'fixe':
            return self.frais_dossier
        else:  # pourcentage
            return montant * (self.frais_dossier / 100)


class ProduitSimulation(db.Model):
    __tablename__ = 'produit_simulations'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    produit_id = db.Column(db.Integer, db.ForeignKey('produits.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Agent qui a fait la simulation

    # Paramètres de simulation
    montant_demande = db.Column(db.Float, nullable=False)
    duree_demande = db.Column(db.Integer, nullable=False)  # en mois

    # Résultats
    mensualite_calculee = db.Column(db.Float, nullable=False)
    taux_applique = db.Column(db.Float, nullable=False)
    frais_dossier = db.Column(db.Float, default=0)
    montant_total = db.Column(db.Float, nullable=False)  # Capital + intérêts

    # Date
    date_simulation = db.Column(db.DateTime, default=datetime.utcnow)

    # Éligibilité
    est_eligible = db.Column(db.Boolean, default=False)
    motif_ineligibilite = db.Column(db.String(200), nullable=True)

    # Relations
    produit = db.relationship('Produit', backref='simulations')

    def __repr__(self):
        return f'<Simulation {self.id}: {self.produit.nom} - {self.montant_demande} HTG>'


class CategorieProduit(db.Model):
    __tablename__ = 'categories_produits'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Hiérarchie
    parent_id = db.Column(db.Integer, db.ForeignKey('categories_produits.id'), nullable=True)

    # Métadonnées
    est_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    sous_categories = db.relationship('CategorieProduit', backref=db.backref('parent', remote_side=[id]))
    produits = db.relationship('Produit', backref='categorie_obj', lazy='dynamic')

    def __repr__(self):
        return f'<Categorie {self.code}: {self.nom}>'

    @property
    def nb_produits(self):
        """Nombre de produits dans cette catégorie"""
        return self.produits.count()

    @property
    def chemin_complet(self):
        """Chemin complet de la catégorie (ex: Crédits > Particuliers > Jeunes)"""
        if self.parent:
            return f"{self.parent.chemin_complet} > {self.nom}"
        return self.nom


class PromotionProduit(db.Model):
    __tablename__ = 'promotions_produits'

    id = db.Column(db.Integer, primary_key=True)
    produit_id = db.Column(db.Integer, db.ForeignKey('produits.id'), nullable=False)

    # Informations de la promotion
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Réduction
    type_reduction = db.Column(db.String(20), default='pourcentage')  # 'pourcentage', 'montant_fixe'
    valeur_reduction = db.Column(db.Float, nullable=False)  # 10 pour 10% ou 50000 pour montant fixe

    # Conditions
    montant_min = db.Column(db.Float, default=0)
    montant_max = db.Column(db.Float, default=0)
    duree_min_mois = db.Column(db.Integer, default=0)
    duree_max_mois = db.Column(db.Integer, default=0)

    # Période
    date_debut = db.Column(db.DateTime, nullable=False)
    date_fin = db.Column(db.DateTime, nullable=False)

    # Statut
    est_active = db.Column(db.Boolean, default=True)
    code_promotion = db.Column(db.String(20), unique=True, nullable=True)  # Ex: "JEUNE2024"

    # Limites d'utilisation
    utilisation_max = db.Column(db.Integer, default=0)  # 0 = illimité
    utilisation_actuelle = db.Column(db.Integer, default=0)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relations
    produit = db.relationship('Produit', backref='promotions')

    def __repr__(self):
        return f'<Promotion {self.code_promotion}: {self.nom}>'

    @property
    def est_valide(self):
        """Vérifie si la promotion est valide"""
        maintenant = datetime.now()
        return (self.est_active and
                self.date_debut <= maintenant <= self.date_fin and
                (self.utilisation_max == 0 or self.utilisation_actuelle < self.utilisation_max))

    @property
    def jours_restants(self):
        """Jours restants avant la fin de la promotion"""
        if self.est_valide:
            delta = (self.date_fin - datetime.now()).days
            return max(0, delta)
        return 0

    def appliquer_reduction(self, montant_initial):
        """Applique la réduction à un montant"""
        if self.type_reduction == 'pourcentage':
            return montant_initial * (1 - self.valeur_reduction / 100)
        else:  # montant_fixe
            return max(0, montant_initial - self.valeur_reduction)

    def utiliser(self):
        """Incrémente le compteur d'utilisation"""
        if self.est_valide:
            self.utilisation_actuelle += 1
            db.session.commit()
            return True
        return False


class AlerteAML(db.Model):
    __tablename__ = 'alertes_aml'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=True)
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Agent concerné
    traitee_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Conformité qui traite

    # Informations de l'alerte
    type_alerte = db.Column(db.String(50),
                            nullable=False)  # 'transaction_suspecte', 'kyc_incomplet', 'document_expire', 'volume_anormal', 'ppe', 'pays_risque'
    niveau_risque = db.Column(db.String(20), default='moyen')  # 'faible', 'moyen', 'eleve', 'critique'
    score_risque = db.Column(db.Integer, default=0)  # Score sur 100

    # Description
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Montant concerné (pour transactions)
    montant = db.Column(db.Float, default=0)
    devise = db.Column(db.String(10), default='HTG')

    # Dates
    date_detection = db.Column(db.DateTime, default=datetime.utcnow)
    date_traitement = db.Column(db.DateTime, nullable=True)
    date_escalade = db.Column(db.DateTime, nullable=True)

    # Statut
    statut = db.Column(db.String(20),
                       default='nouvelle')  # 'nouvelle', 'en_cours', 'traitee', 'escaladee', 'fausse_alerte'

    # Résolution
    action_prise = db.Column(db.Text, nullable=True)
    commentaire_traitement = db.Column(db.Text, nullable=True)

    # Escalade
    escalade_a = db.Column(db.String(100), nullable=True)  # 'superieur', 'brh', 'cellule_renseignement'
    motif_escalade = db.Column(db.Text, nullable=True)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relations
    client = db.relationship('Client', backref='alertes_aml', foreign_keys=[client_id])
    transaction = db.relationship('Transaction', backref='alertes_aml', foreign_keys=[transaction_id])
    user = db.relationship('User', foreign_keys=[employe_id], backref='alertes_generees')
    traitee_par = db.relationship('User', foreign_keys=[traitee_par_id], backref='alertes_traitees')

    def __repr__(self):
        return f'<AlerteAML {self.id}: {self.type_alerte} - {self.niveau_risque}>'

    @property
    def jours_ouverture(self):
        """Nombre de jours depuis la détection"""
        delta = datetime.now() - self.date_detection
        return delta.days

    @property
    def delai_traitement(self):
        """Délai de traitement en heures"""
        if self.date_traitement:
            delta = self.date_traitement - self.date_detection
            return round(delta.total_seconds() / 3600, 1)
        return None

    @property
    def couleur_risque(self):
        """Couleur pour l'affichage du risque"""
        couleurs = {
            'faible': 'success',
            'moyen': 'warning',
            'eleve': 'danger',
            'critique': 'dark'
        }
        return couleurs.get(self.niveau_risque, 'secondary')

    @property
    def priorite(self):
        """Priorité basée sur le risque et le délai"""
        if self.niveau_risque == 'critique':
            return 1
        elif self.niveau_risque == 'eleve' and self.jours_ouverture > 2:
            return 2
        elif self.niveau_risque == 'moyen' and self.jours_ouverture > 5:
            return 3
        elif self.niveau_risque == 'faible' and self.jours_ouverture > 10:
            return 4
        return 5

    def traiter(self, employe_id, action, commentaire):
        """Marque l'alerte comme traitée"""
        self.statut = 'traitee'
        self.traitee_par_id = employe_id
        self.date_traitement = datetime.now()
        self.action_prise = action
        self.commentaire_traitement = commentaire
        db.session.commit()

    def escalader(self, employe_id, destinataire, motif):
        """Escalade l'alerte à une autorité supérieure"""
        self.statut = 'escaladee'
        self.traitee_par_id = employe_id
        self.date_escalade = datetime.now()
        self.escalade_a = destinataire
        self.motif_escalade = motif
        db.session.commit()

    def marquer_fausse(self, employe_id, commentaire):
        """Marque comme fausse alerte"""
        self.statut = 'fausse_alerte'
        self.traitee_par_id = employe_id
        self.date_traitement = datetime.now()
        self.commentaire_traitement = commentaire
        db.session.commit()

    @classmethod
    def creer_depuis_transaction(cls, transaction, motif, niveau_risque='moyen'):
        """Crée une alerte à partir d'une transaction suspecte"""
        alerte = cls(
            client_id=transaction.client_id,
            transaction_id=transaction.id,
            employe_id=transaction.employe_id,
            type_alerte='transaction_suspecte',
            niveau_risque=niveau_risque,
            titre=f"Transaction suspecte - {transaction.type}",
            description=motif,
            montant=transaction.montant
        )
        db.session.add(alerte)
        db.session.commit()
        return alerte

class Document(db.Model):
    __tablename__ = 'documents'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    # === CLÉS ÉTRANGÈRES ===
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # === INFORMATIONS DU DOCUMENT ===
    type_document = db.Column(db.String(50), nullable=False)  # 'cin', 'passeport', 'permis', 'attestation'
    categorie = db.Column(db.String(20), default='identite')  # 'identite', 'domicile', 'professionnel', 'financier'
    nom = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # === INFORMATIONS DU FICHIER ===
    filename = db.Column(db.String(500), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, default=0)  # en bytes
    mime_type = db.Column(db.String(100), nullable=True)

    # === MÉTADONNÉES DU DOCUMENT ===
    numero = db.Column(db.String(100), nullable=True)
    pays_emission = db.Column(db.String(50), default='HTI')
    date_emission = db.Column(db.Date, nullable=True)
    date_expiration = db.Column(db.Date, nullable=True)

    # === VÉRIFICATION ===
    est_verifie = db.Column(db.Boolean, default=False)
    date_verification = db.Column(db.DateTime, nullable=True)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commentaire_verification = db.Column(db.Text, nullable=True)
    score_authenticite = db.Column(db.Integer, default=0)  # Score 0-100

    # === OCR ===
    ocr_texte = db.Column(db.Text, nullable=True)
    ocr_confiance = db.Column(db.Float, default=0)
    ocr_donnees = db.Column(db.JSON, nullable=True)

    # === DATES ===
    date_upload = db.Column(db.DateTime, default=datetime.utcnow)
    date_expiration_notification = db.Column(db.DateTime, nullable=True)

    # === RELATIONS (AVEC foreign_keys SPÉCIFIÉES) ===
    user = db.relationship('User', foreign_keys=[employe_id], backref='documents')
    client = db.relationship('Client', foreign_keys=[client_id], backref='documents')
    verificateur = db.relationship('User', foreign_keys=[verified_by], backref='documents_verifies')

    def __repr__(self):
        return f'<Document {self.id}: {self.type_document} - {self.nom}>'

    @property
    def extension(self):
        """Retourne l'extension du fichier"""
        if '.' in self.filename:
            return self.filename.rsplit('.', 1)[1].lower()
        return ''

    @property
    def est_image(self):
        """Vérifie si le document est une image"""
        return self.mime_type and self.mime_type.startswith('image/')

    @property
    def est_pdf(self):
        """Vérifie si le document est un PDF"""
        return self.mime_type == 'application/pdf' or self.extension == 'pdf'

    @property
    def icone(self):
        """Retourne l'icône Font Awesome selon le type de fichier"""
        if self.est_image:
            return 'fa-file-image'
        elif self.est_pdf:
            return 'fa-file-pdf'
        elif self.extension in ['doc', 'docx']:
            return 'fa-file-word'
        elif self.extension in ['xls', 'xlsx']:
            return 'fa-file-excel'
        elif self.extension in ['txt']:
            return 'fa-file-alt'
        else:
            return 'fa-file'

    @property
    def taille_formattee(self):
        """Retourne la taille formatée (Ko, Mo)"""
        size = self.file_size
        if not size:
            return 'Inconnue'

        for unit in ['o', 'Ko', 'Mo', 'Go']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} To"

    @property
    def est_expire(self):
        """Vérifie si le document est expiré"""
        if self.date_expiration:
            return datetime.now().date() > self.date_expiration
        return False

    @property
    def jours_avant_expiration(self):
        """Jours avant expiration (négatif si expiré)"""
        if self.date_expiration:
            delta = self.date_expiration - datetime.now().date()
            return delta.days
        return None

    @property
    def statut_expiration(self):
        """Statut d'expiration pour affichage"""
        if not self.date_expiration:
            return {'couleur': 'secondary', 'texte': 'Non défini'}

        jours = self.jours_avant_expiration
        if jours < 0:
            return {'couleur': 'danger', 'texte': f'Expiré depuis {-jours}j'}
        elif jours <= 30:
            return {'couleur': 'warning', 'texte': f'Expire dans {jours}j'}
        elif jours <= 90:
            return {'couleur': 'info', 'texte': f'Expire dans {jours}j'}
        else:
            return {'couleur': 'success', 'texte': f'Valide ({jours}j)'}

    @classmethod
    def get_by_user(cls, employe_id, categorie=None):
        """Récupère les documents d'un utilisateur"""
        query = cls.query.filter_by(employe_id=employe_id)
        if categorie:
            query = query.filter_by(categorie=categorie)
        return query.order_by(cls.date_upload.desc()).all()

    @classmethod
    def get_by_client(cls, client_id, categorie=None):
        """Récupère les documents d'un client"""
        query = cls.query.filter_by(client_id=client_id)
        if categorie:
            query = query.filter_by(categorie=categorie)
        return query.order_by(cls.date_upload.desc()).all()

    @classmethod
    def get_en_attente(cls):
        """Récupère les documents en attente de vérification"""
        return cls.query.filter_by(est_verifie=False).order_by(cls.date_upload).all()

    def verifier(self, verificateur_id, valide, commentaire=None):
        """Vérifie le document (valide/rejette)"""
        self.est_verifie = True
        self.verified_by = verificateur_id
        self.date_verification = datetime.now()
        self.commentaire_verification = commentaire
        self.statut = 'valide' if valide else 'rejete'
        db.session.commit()

    def notifier_expiration(self):
        """Marque que la notification d'expiration a été envoyée"""
        self.date_expiration_notification = datetime.now()
        db.session.commit()


class VerificationAnnuelle(db.Model):
    __tablename__ = 'verifications_annuelles'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    effectuee_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Dates
    date_derniere_verification = db.Column(db.DateTime, nullable=False)
    date_prochaine_verification = db.Column(db.DateTime, nullable=False)
    date_effectuee = db.Column(db.DateTime, nullable=True)

    # Statut
    statut = db.Column(db.String(20), default='a_faire')  # 'a_faire', 'en_cours', 'effectuee', 'retard'

    # Résultats
    resultat = db.Column(db.String(20), nullable=True)  # 'conforme', 'non_conforme', 'partiel'
    commentaire = db.Column(db.Text, nullable=True)

    # Documents vérifiés
    documents_verifies = db.Column(db.JSON, nullable=True)  # Liste des IDs de documents vérifiés

    # KYC
    kyc_valide = db.Column(db.Boolean, default=False)
    screening_aml_valide = db.Column(db.Boolean, default=False)
    verification_faciale_valide = db.Column(db.Boolean, default=False)

    # Score global
    score_conformite = db.Column(db.Integer, default=0)  # Score sur 100

    # Notifications
    notification_envoyee = db.Column(db.Boolean, default=False)
    date_notification = db.Column(db.DateTime, nullable=True)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relations
    client = db.relationship('Client', backref='verifications_annuelles')
    effectuee_par = db.relationship('User', backref='verifications_effectuees')


    # ✅ NOUVELLE COLONNE
    annee = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint(
            'client_id',
            'annee',
            name='unique_verification_par_an'
        ),
    )

    def __repr__(self):
        return f'<VerificationAnnuelle {self.id}: {self.client.nom} - {self.date_prochaine_verification.strftime("%Y")}>'

    @property
    def jours_restants(self):
        """Jours avant la prochaine échéance"""
        delta = self.date_prochaine_verification - datetime.now()
        return delta.days

    @property
    def est_en_retard(self):
        """Vérifie si la vérification est en retard"""
        return datetime.now() > self.date_prochaine_verification and self.statut != 'effectuee'

    @property
    def couleur_statut(self):
        """Couleur pour l'affichage du statut"""
        if self.statut == 'effectuee':
            return 'success'
        elif self.est_en_retard:
            return 'danger'
        elif self.jours_restants <= 30:
            return 'warning'
        else:
            return 'info'

    @property
    def priorite(self):
        """Priorité de la vérification"""
        if self.est_en_retard:
            return 1
        elif self.jours_restants <= 15:
            return 2
        elif self.jours_restants <= 30:
            return 3
        elif self.jours_restants <= 60:
            return 4
        else:
            return 5

    def effectuer(self, employe_id, documents_verifies, kyc_valide, screening_valide, faciale_valide, commentaire=None):
        """Effectue la vérification annuelle"""
        self.statut = 'effectuee'
        self.effectuee_par_id = employe_id
        self.date_effectuee = datetime.now()
        self.documents_verifies = documents_verifies
        self.kyc_valide = kyc_valide
        self.screening_aml_valide = screening_valide
        self.verification_faciale_valide = faciale_valide
        self.commentaire = commentaire

        # Calculer le score
        score = 0
        if kyc_valide:
            score += 40
        if screening_valide:
            score += 30
        if faciale_valide:
            score += 30
        self.score_conformite = score

        # Déterminer le résultat
        if score >= 80:
            self.resultat = 'conforme'
        elif score >= 50:
            self.resultat = 'partiel'
        else:
            self.resultat = 'non_conforme'

        # Planifier la prochaine vérification
        self.date_prochaine_verification = self.date_prochaine_verification.replace(
            year=self.date_prochaine_verification.year + 1)

        db.session.commit()

    def notifier_retard(self):
        """Marque que la notification de retard a été envoyée"""
        self.notification_envoyee = True
        self.date_notification = datetime.now()
        db.session.commit()

    @classmethod
    def planifier_pour_client(cls, client_id, date_derniere_verif=None):
        """Planifie une nouvelle vérification annuelle pour un client"""
        if not date_derniere_verif:
            date_derniere_verif = datetime.now()

        prochaine_verif = date_derniere_verif.replace(year=date_derniere_verif.year + 1)

        verification = cls(
            client_id=client_id,
            date_derniere_verification=date_derniere_verif,
            date_prochaine_verification=prochaine_verif,
            statut='a_faire'
        )
        db.session.add(verification)
        db.session.commit()
        return verification

    @classmethod
    def get_verifications_a_faire(cls, limite_jours=30):
        """Récupère les vérifications à faire dans les X jours"""
        date_limite = datetime.now() + timedelta(days=limite_jours)
        return cls.query.filter(
            cls.statut.in_(['a_faire', 'en_cours']),
            cls.date_prochaine_verification <= date_limite
        ).order_by(cls.date_prochaine_verification).all()


class ScreeningListe(db.Model):
    __tablename__ = 'screening_listes'

    id = db.Column(db.Integer, primary_key=True)

    # Type de liste
    type_liste = db.Column(db.String(50), nullable=False)  # 'pep', 'sanction', 'terrorisme', 'criminalite'
    source = db.Column(db.String(100), nullable=True)  # 'ONU', 'UE', 'OFAC', 'BRH', 'Interne'

    # Entité
    nom = db.Column(db.String(200), nullable=False)
    alias = db.Column(db.Text, nullable=True)  # Noms alternatifs en JSON
    type_entite = db.Column(db.String(20))  # 'personne', 'organisation', 'pays'

    # Identifiants
    numero_document = db.Column(db.String(100), nullable=True)
    pays = db.Column(db.String(50), nullable=True)
    date_naissance = db.Column(db.Date, nullable=True)
    lieu_naissance = db.Column(db.String(200), nullable=True)

    # Informations
    motif = db.Column(db.Text, nullable=True)
    reference_officielle = db.Column(db.String(100), nullable=True)
    date_inscription = db.Column(db.Date, nullable=True)

    # Niveau de risque
    niveau_risque = db.Column(db.String(20), default='eleve')

    # Statut
    actif = db.Column(db.Boolean, default=True)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ScreeningListe {self.id}: {self.nom} - {self.type_liste}>'

    @classmethod
    def screener_client(cls, client):
        """Screen un client contre toutes les listes"""
        resultats = []
        query = cls.query.filter_by(actif=True)

        for liste in query.all():
            # Vérification par nom
            if liste.nom.lower() in f"{client.nom} {client.prenom}".lower():
                resultats.append({
                    'liste': liste,
                    'match': 'nom',
                    'score': 90
                })
                continue

            # Vérification par document
            if liste.numero_document and client.cin == liste.numero_document:
                resultats.append({
                    'liste': liste,
                    'match': 'document',
                    'score': 100
                })
                continue

            # Vérification par date de naissance
            if liste.date_naissance and client.date_naissance:
                if liste.date_naissance == client.date_naissance.date():
                    resultats.append({
                        'liste': liste,
                        'match': 'date_naissance',
                        'score': 95
                    })

        return resultats


class FormationAML(db.Model):
    __tablename__ = 'formations_aml'

    id = db.Column(db.Integer, primary_key=True)

    # Informations formation
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type_formation = db.Column(db.String(50))  # 'initiale', 'continue', 'specialisee'

    # Dates
    date_formation = db.Column(db.DateTime, nullable=False)
    duree_heures = db.Column(db.Integer, default=4)

    # Formateur
    formateur = db.Column(db.String(100), nullable=True)

    # Participants
    participants = db.Column(db.JSON, default=list)  # Liste des IDs des participants
    participants_presents = db.Column(db.JSON, default=list)

    # Évaluation
    note_minimum = db.Column(db.Integer, default=70)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<FormationAML {self.id}: {self.titre}>'

    @property
    def nb_participants(self):
        return len(self.participants) if self.participants else 0

    @property
    def nb_presents(self):
        return len(self.participants_presents) if self.participants_presents else 0

    @property
    def taux_presence(self):
        if self.nb_participants > 0:
            return round((self.nb_presents / self.nb_participants) * 100, 1)
        return 0


class CertificatFormation(db.Model):
    __tablename__ = 'certificats_formation'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    formation_id = db.Column(db.Integer, db.ForeignKey('formations_aml.id'), nullable=False)

    # Informations
    date_obtention = db.Column(db.DateTime, default=datetime.utcnow)
    date_expiration = db.Column(db.DateTime, nullable=False)  # Généralement +1 an

    # Résultats
    note = db.Column(db.Integer, nullable=True)
    reussi = db.Column(db.Boolean, default=False)

    # Certificat
    certificat_url = db.Column(db.String(500), nullable=True)
    certificat_valide = db.Column(db.Boolean, default=True)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    employe = db.relationship('User', backref='certificats_aml')
    formation = db.relationship('FormationAML', backref='certificats')

    __table_args__ = (
        db.UniqueConstraint('employe_id', 'formation_id', name='unique_certificat_employe'),
    )

    def __repr__(self):
        return f'<CertificatFormation {self.id}: {self.employe.nom} - {self.formation.titre}>'

    @property
    def est_valide(self):
        """Vérifie si le certificat est encore valide"""
        return self.certificat_valide and datetime.now() < self.date_expiration

    @property
    def jours_restants(self):
        """Jours avant expiration"""
        if self.date_expiration:
            delta = self.date_expiration - datetime.now()
            return delta.days
        return None


class Echeance(db.Model):
    __tablename__ = 'echeances'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    credit_id = db.Column(db.Integer, db.ForeignKey('credits.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Agent responsable

    # Informations de l'échéance
    numero_echeance = db.Column(db.Integer, nullable=False)  # Numéro de l'échéance (1, 2, 3...)
    montant_capital = db.Column(db.Float, nullable=False)  # Part du capital
    montant_interet = db.Column(db.Float, nullable=False)  # Intérêts
    montant_total = db.Column(db.Float, nullable=False)  # Capital + Intérêts
    montant_penalite = db.Column(db.Float, default=0)  # Pénalités éventuelles

    # Dates
    date_echeance = db.Column(db.Date, nullable=False)
    date_limite = db.Column(db.Date, nullable=False)  # Date limite avec période de grâce
    date_paiement = db.Column(db.DateTime, nullable=True)

    # Statut
    statut = db.Column(db.String(200), default='en_attente')  # 'en_attente', 'payee', 'retard', 'impayee', 'renégociée'

    # Paiement
    paiement_id = db.Column(db.Integer, db.ForeignKey('paiements.id'), nullable=True)
    mode_paiement = db.Column(db.String(50), nullable=True)
    reference_paiement = db.Column(db.String(100), nullable=True)

    # Recouvrement
    tentative_recouvrement = db.Column(db.Integer, default=0)
    date_derniere_relance = db.Column(db.DateTime, nullable=True)
    commentaire_recouvrement = db.Column(db.Text, nullable=True)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relations
    credit = db.relationship('Credit', backref='echeances')
    client = db.relationship('Client', backref='echeances')
    agent = db.relationship('User', backref='echeances_suivies')
    paiement = db.relationship('Paiement', backref='echeance_concernee')

    __table_args__ = (
        db.UniqueConstraint('credit_id', 'numero_echeance', name='unique_echeance_credit'),
    )

    def __repr__(self):
        return f'<Echeance {self.id}: Crédit {self.credit_id} - Échéance {self.numero_echeance}>'

    @property
    def jours_retard(self):
        """Calcule le nombre de jours de retard"""
        if self.statut == 'payee' and self.date_paiement:
            if self.date_paiement.date() > self.date_limite:
                return (self.date_paiement.date() - self.date_limite).days
            return 0
        elif self.statut in ['retard', 'impayee']:
            aujourd_hui = datetime.now().date()
            if aujourd_hui > self.date_limite:
                return (aujourd_hui - self.date_limite).days
        return 0

    @property
    def jours_avant_echeance(self):
        """Jours avant l'échéance"""
        aujourd_hui = datetime.now().date()
        if aujourd_hui <= self.date_echeance:
            return (self.date_echeance - aujourd_hui).days
        return -self.jours_retard

    @property
    def est_payee(self):
        """Vérifie si l'échéance est payée"""
        return self.statut == 'payee'

    @property
    def est_en_retard(self):
        """Vérifie si l'échéance est en retard"""
        aujourd_hui = datetime.now().date()
        return (self.statut != 'payee' and aujourd_hui > self.date_limite)

    @property
    def couleur_statut(self):
        """Couleur pour l'affichage du statut"""
        if self.statut == 'payee':
            return 'success'
        elif self.est_en_retard:
            if self.jours_retard <= 7:
                return 'warning'
            elif self.jours_retard <= 30:
                return 'danger'
            else:
                return 'dark'
        elif self.jours_avant_echeance <= 3:
            return 'info'
        else:
            return 'secondary'

    @property
    def libelle_statut(self):
        """Libellé du statut avec retard"""
        if self.statut == 'payee':
            return 'Payée'
        elif self.est_en_retard:
            return f'Retard {self.jours_retard}j'
        elif self.jours_avant_echeance <= 3:
            return f'Échéance J-{self.jours_avant_echeance}'
        else:
            return 'À venir'

    def payer(self, paiement_id, mode_paiement, reference=None):
        """Marque l'échéance comme payée"""
        self.statut = 'payee'
        self.paiement_id = paiement_id
        self.mode_paiement = mode_paiement
        self.reference_paiement = reference
        self.date_paiement = datetime.now()
        db.session.commit()

    def signaler_retard(self, commentaire=None):
        """Signale un retard de paiement"""
        self.statut = 'retard'
        self.tentative_recouvrement += 1
        self.date_derniere_relance = datetime.now()
        self.commentaire_recouvrement = commentaire
        db.session.commit()

    def renégocier(self, nouvelle_date, commentaire=None):
        """Renégocie la date d'échéance"""
        ancienne_date = self.date_limite
        self.date_limite = nouvelle_date
        self.statut = 'renégociée'
        self.commentaire_recouvrement = f"Renégociée: {ancienne_date} -> {nouvelle_date}. {commentaire or ''}"
        db.session.commit()

    @classmethod
    def get_echeances_a_venir(cls, jours=30):
        """Récupère les échéances à venir dans X jours"""
        date_limite = datetime.now().date() + timedelta(days=jours)
        return cls.query.filter(
            cls.statut == 'en_attente',
            cls.date_echeance <= date_limite
        ).order_by(cls.date_echeance).all()

    @classmethod
    def get_echeances_en_retard(cls):
        """Récupère toutes les échéances en retard"""
        aujourd_hui = datetime.now().date()
        return cls.query.filter(
            cls.statut.in_(['en_attente', 'retard']),
            cls.date_limite < aujourd_hui
        ).order_by(cls.date_limite).all()


class DecisionCredit(db.Model):
    __tablename__ = 'decisions_credit'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    credit_id = db.Column(db.Integer, db.ForeignKey('credits.id'), nullable=False)
    decideur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Type de décision
    type_decision = db.Column(db.String(20), nullable=False)  # 'approbation', 'rejet', 'renégociation', 'annulation'

    # Décision
    decision = db.Column(db.String(20), nullable=False)  # 'approuve', 'rejete', 'renégocie', 'annule'

    # Montants (pour renégociation)
    montant_original = db.Column(db.Float, nullable=True)
    montant_nouveau = db.Column(db.Float, nullable=True)
    taux_original = db.Column(db.Float, nullable=True)
    taux_nouveau = db.Column(db.Float, nullable=True)
    duree_originale = db.Column(db.Integer, nullable=True)
    duree_nouvelle = db.Column(db.Integer, nullable=True)

    # Commentaires et motifs
    motif = db.Column(db.String(200), nullable=False)
    commentaire = db.Column(db.Text, nullable=True)

    # Documents associés
    document_approbation = db.Column(db.String(500), nullable=True)

    # Dates
    date_decision = db.Column(db.DateTime, default=datetime.utcnow)
    date_effet = db.Column(db.DateTime, nullable=True)  # Date à laquelle la décision prend effet

    # Niveau de décision
    niveau_decision = db.Column(db.String(20), default='chef_credit')  # 'agent', 'chef_credit', 'comite', 'direction'

    # Validation hiérarchique
    valide_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    date_validation = db.Column(db.DateTime, nullable=True)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    credit = db.relationship('Credit', backref='decisions')
    decideur = db.relationship('User', foreign_keys=[decideur_id], backref='decisions_prises')
    valide_par = db.relationship('User', foreign_keys=[valide_par_id], backref='decisions_validees')

    def __repr__(self):
        return f'<DecisionCredit {self.id}: {self.decision} - Crédit {self.credit_id}>'

    @property
    def est_approuvee(self):
        return self.decision == 'approuve' and self.valide_par_id is not None

    @property
    def couleur_decision(self):
        """Couleur pour l'affichage de la décision"""
        couleurs = {
            'approuve': 'success',
            'rejete': 'danger',
            'renégocie': 'warning',
            'annule': 'secondary'
        }
        return couleurs.get(self.decision, 'info')

    @property
    def icone_decision(self):
        """Icône pour la décision"""
        icones = {
            'approuve': 'check-circle',
            'rejete': 'times-circle',
            'renégocie': 'sync-alt',
            'annule': 'ban'
        }
        return icones.get(self.decision, 'question-circle')

    def appliquer(self):
        """Applique la décision au crédit"""
        credit = self.credit

        if self.decision == 'approuve':
            credit.statut = 'actif'
            credit.date_approbation = self.date_decision
            credit.approuve_par = self.decideur_id

        elif self.decision == 'rejete':
            credit.statut = 'rejete'

        elif self.decision == 'renégocie':
            if self.montant_nouveau:
                credit.montant = self.montant_nouveau
            if self.taux_nouveau:
                credit.taux_interet = self.taux_nouveau
            if self.duree_nouvelle:
                credit.duree_mois = self.duree_nouvelle
            credit.statut = 'en_attente'
            credit.notes = f"Renégociation: {self.motif}"

        elif self.decision == 'annule':
            credit.statut = 'annule'

        self.date_effet = datetime.now()
        db.session.commit()

    def valider(self, valideur_id):
        """Validation hiérarchique de la décision"""
        self.valide_par_id = valideur_id
        self.date_validation = datetime.now()
        db.session.commit()

        # Si validée, appliquer la décision
        if self.valide_par_id:
            self.appliquer()

    @classmethod
    def get_decisions_recentes(cls, limite=20):
        """Récupère les décisions récentes"""
        return cls.query.order_by(
            cls.date_decision.desc()
        ).limit(limite).all()

    @classmethod
    def get_decisions_en_attente_validation(cls):
        """Récupère les décisions en attente de validation"""
        return cls.query.filter(
            cls.valide_par_id.is_(None),
            cls.date_decision.isnot(None)
        ).order_by(cls.date_decision).all()


class RenegociationCredit(db.Model):
    __tablename__ = 'renegociations_credit'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    credit_id = db.Column(db.Integer, db.ForeignKey('credits.id'), nullable=False)
    demande_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approuve_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Type de renégociation
    type_renegociation = db.Column(db.String(50))  # 'taux', 'duree', 'montant', 'report', 'restructuration'

    # Anciennes valeurs
    ancien_montant = db.Column(db.Float)
    ancien_taux = db.Column(db.Float)
    ancienne_duree = db.Column(db.Integer)
    ancienne_mensualite = db.Column(db.Float)

    # Nouvelles valeurs proposées
    nouveau_montant = db.Column(db.Float)
    nouveau_taux = db.Column(db.Float)
    nouvelle_duree = db.Column(db.Integer)
    nouvelle_mensualite = db.Column(db.Float)

    # Report d'échéance
    mois_report = db.Column(db.Integer, default=0)  # Nombre de mois de report
    date_nouvelle_echeance = db.Column(db.Date, nullable=True)

    # Motifs
    motif_demande = db.Column(db.Text)
    motif_client = db.Column(db.Text)  # Motif invoqué par le client

    # Documents justificatifs
    justificatifs = db.Column(db.JSON, default=list)  # URLs des documents

    # Statut
    statut = db.Column(db.String(200), default='en_attente')  # 'en_attente', 'approuvee', 'rejetee', 'en_cours'

    # Dates
    date_demande = db.Column(db.DateTime, default=datetime.utcnow)
    date_traitement = db.Column(db.DateTime, nullable=True)

    # Commentaires
    commentaire_approbation = db.Column(db.Text, nullable=True)

    # Relations
    credit = db.relationship('Credit', backref='renegociations')
    demandeur = db.relationship('User', foreign_keys=[demande_par_id], backref='renegociations_demandees')
    approbateur = db.relationship('User', foreign_keys=[approuve_par_id], backref='renegociations_approuvees')

    def __repr__(self):
        return f'<RenegociationCredit {self.id}: Crédit {self.credit_id} - {self.type_renegociation}>'

    def approuver(self, approbateur_id, commentaire=None):
        """Approuve la renégociation"""
        self.statut = 'approuvee'
        self.approuve_par_id = approbateur_id
        self.date_traitement = datetime.now()
        self.commentaire_approbation = commentaire

        # Mettre à jour le crédit
        credit = self.credit
        if self.nouveau_montant:
            credit.montant = self.nouveau_montant
        if self.nouveau_taux:
            credit.taux_interet = self.nouveau_taux
        if self.nouvelle_duree:
            credit.duree_mois = self.nouvelle_duree

        credit.notes = f"Renégociation approuvée le {datetime.now().strftime('%d/%m/%Y')}"

        db.session.commit()

    def rejeter(self, approbateur_id, commentaire):
        """Rejette la renégociation"""
        self.statut = 'rejetee'
        self.approuve_par_id = approbateur_id
        self.date_traitement = datetime.now()
        self.commentaire_approbation = commentaire
        db.session.commit()


class ScoringCredit(db.Model):
    __tablename__ = 'scoring_credit'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    credit_id = db.Column(db.Integer, db.ForeignKey('credits.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    # Score global
    score_global = db.Column(db.Integer, default=0)  # Score sur 1000

    # Critères de scoring
    criteres = db.Column(db.JSON, default=dict)  # Détail des scores par critère

    # Catégories
    categorie_risque = db.Column(db.String(20))  # 'A', 'B', 'C', 'D', 'E'
    probabilite_defaut = db.Column(db.Float, default=0)  # Probabilité de défaut en %

    # Décision automatique
    decision_automatique = db.Column(db.String(20))  # 'accepte', 'refuse', 'a_analyser'
    montant_maximum = db.Column(db.Float, nullable=True)  # Montant maximum recommandé

    # Métadonnées
    date_calcul = db.Column(db.DateTime, default=datetime.utcnow)
    version_algo = db.Column(db.String(20), default='1.0')

    # Relations
    credit = db.relationship('Credit', backref='scoring')
    client = db.relationship('Client', backref='scorings')

    def __repr__(self):
        return f'<ScoringCredit {self.id}: Score {self.score_global} - {self.categorie_risque}>'

    @property
    def niveau_risque(self):
        """Niveau de risque basé sur la catégorie"""
        niveaux = {
            'A': 'Très faible',
            'B': 'Faible',
            'C': 'Moyen',
            'D': 'Élevé',
            'E': 'Très élevé'
        }
        return niveaux.get(self.categorie_risque, 'Indéterminé')

    @property
    def couleur_risque(self):
        """Couleur pour l'affichage du risque"""
        couleurs = {
            'A': 'success',
            'B': 'info',
            'C': 'warning',
            'D': 'danger',
            'E': 'dark'
        }
        return couleurs.get(self.categorie_risque, 'secondary')

    @classmethod
    def calculer_score(cls, credit, client):
        """Calcule le score de crédit pour une demande"""

        # === VALIDATION DES DONNÉES ===
        if not client or not credit:
            return {
                'score': 0,
                'categorie': 'E',
                'decision': 'refuse',
                'proba_defaut': 100,
                'criteres': {},
                'erreur': 'Client ou crédit manquant'
            }

        score = 0
        criteres = {}

        # === 1. REVENU MENSUEL ===
        revenu = client.revenu_mensuel or 0
        if revenu >= 100000:
            score += 200
            criteres['revenu'] = 200
        elif revenu >= 50000:
            score += 150
            criteres['revenu'] = 150
        elif revenu >= 25000:
            score += 100
            criteres['revenu'] = 100
        else:
            score += 50
            criteres['revenu'] = 50

        # === 2. CAPACITÉ DE REMBOURSEMENT ===
        capacite = client.capacite_remboursement or 0
        if capacite > 0:
            montant_credit = credit.montant or 0
            ratio = montant_credit / capacite
            if ratio <= 3:
                score += 200
                criteres['capacite'] = 200
            elif ratio <= 5:
                score += 150
                criteres['capacite'] = 150
            elif ratio <= 10:
                score += 100
                criteres['capacite'] = 100
            else:
                score += 50
                criteres['capacite'] = 50
        else:
            criteres['capacite'] = 0

        # === 3. HISTORIQUE DE CRÉDIT ===
        credits_precedents = Credit.query.filter_by(client_id=client.id).count()
        if credits_precedents == 0:
            score += 100
            criteres['historique'] = 100
        elif credits_precedents <= 3:
            score += 150
            criteres['historique'] = 150
        else:
            score += 200
            criteres['historique'] = 200

        # === 4. GARANTIE ===
        if credit.garantie:
            score += 150
            criteres['garantie'] = 150
        else:
            score += 50
            criteres['garantie'] = 50

        # === 5. PROFESSION ===
        professions_risque_faible = ['fonctionnaire', 'cadre', 'profession_libérale']
        professions_risque_moyen = ['commerçant', 'indépendant']

        if client.profession in professions_risque_faible:
            score += 150
            criteres['profession'] = 150
        elif client.profession in professions_risque_moyen:
            score += 100
            criteres['profession'] = 100
        else:
            score += 50
            criteres['profession'] = 50

        # === 6. ANCIENNETÉ DU CLIENT ===
        anciennete_jours = (datetime.utcnow() - client.date_creation).days
        if anciennete_jours >= 730:  # 2 ans
            score += 100
            criteres['anciennete'] = 100
        elif anciennete_jours >= 365:  # 1 an
            score += 75
            criteres['anciennete'] = 75
        else:
            score += 25
            criteres['anciennete'] = 25

        # === 7. ÉPARGNE MOYENNE ===
        solde = client.solde or 0
        if solde >= 50000:
            score += 150
            criteres['epargne'] = 150
        elif solde >= 20000:
            score += 100
            criteres['epargne'] = 100
        else:
            score += 30
            criteres['epargne'] = 30

        # === 8. RETARDS PASSÉS (basé sur jours de retard, pas le count) ===
        # IMPORTANT: Utiliser la même métrique que verifier_retards()
        total_jours_retard = db.session.query(
            db.func.sum(RetardPaiement.jours_retard)
        ).filter(
            RetardPaiement.client_id == client.id
        ).scalar() or 0

        nombre_retards = RetardPaiement.query.filter_by(
            client_id=client.id
        ).count()

        if total_jours_retard == 0:
            score += 150
            criteres['retards'] = 150
        elif total_jours_retard <= 30:
            score += 100
            criteres['retards'] = 100
        elif total_jours_retard <= 90:
            score += 50
            criteres['retards'] = 50
        else:
            score += 0
            criteres['retards'] = 0

        # Pénalité pour retards répétés
        if nombre_retards >= 3:
            score -= 25
            criteres['penalite_retards_repetes'] = -25

        # === 9. RATIO DETTE/REVENU (corrigé) ===
        total_dettes = db.session.query(
            db.func.sum(Pret.solde_restant)
        ).filter(
            Pret.client_id == client.id
        ).scalar() or 0

        # Éviter la division par zéro
        if revenu > 0:
            ratio_dette = total_dettes / revenu
            if ratio_dette <= 0.3:
                score += 150
                criteres['ratio_dette_revenu'] = 150
            elif ratio_dette <= 0.5:
                score += 100
                criteres['ratio_dette_revenu'] = 100
            else:
                score += 20
                criteres['ratio_dette_revenu'] = 20
        else:
            criteres['ratio_dette_revenu'] = 0

        # === BONUS : FIDÉLITÉ (optionnel) ===
        prets_rembourses = Pret.query.filter(
            Pret.client_id == client.id,
            Pret.statut == 'rembourse'
        ).count()
        if prets_rembourses >= 2:
            score += 25
            criteres['fidelite'] = 25

        # === DÉCISION FINALE (basée sur score COMPLET) ===
        if score >= 800:
            categorie = 'A'
            proba_defaut = 1
            decision = 'accepte'
        elif score >= 650:
            categorie = 'B'
            proba_defaut = 3
            decision = 'accepte'
        elif score >= 500:
            categorie = 'C'
            proba_defaut = 7
            decision = 'a_analyser'
        elif score >= 350:
            categorie = 'D'
            proba_defaut = 15
            decision = 'a_analyser'
        else:
            categorie = 'E'
            proba_defaut = 30
            decision = 'refuse'

        # === RETOUR COMPLET ===
        # Montant maximum recommandé
        montant_max = client.capacite_remboursement * 12 if client.capacite_remboursement else credit.montant

        return {
            'score_global': score,
            'credit_id':credit.id,
            'client_id':client.id,
            'categorie_risque': categorie,
            'decision_automatique': decision,
            'proba_defaut': proba_defaut,
            'criteres': criteres,
            'details': {
                'revenu': revenu,
                'capacite_remboursement': capacite,
                'anciennete_jours': anciennete_jours,
                'solde': solde,
                'total_dettes': total_dettes,
                'nombre_retards': nombre_retards,
                'total_jours_retard': total_jours_retard,
                'montant_maximum': montant_max
            }
        }





class Caisse(db.Model):
    __tablename__ = 'caisses'

    id = db.Column(db.Integer, primary_key=True)

    # Informations de la caisse
    numero = db.Column(db.String(20), nullable=False)  # C001, C002, etc.
    nom = db.Column(db.String(100), nullable=True)
    type_caisse = db.Column(db.String(20), default='principale')  # 'principale', 'secondaire', 'mobile'

    # Relations
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Agent assigné

    # État de la caisse
    est_ouverte = db.Column(db.Boolean, default=False)
    date_ouverture = db.Column(db.DateTime, nullable=True)
    date_fermeture = db.Column(db.DateTime, nullable=True)

    # Soldes
    solde_initial = db.Column(db.Float, default=0)
    solde_actuel = db.Column(db.Float, default=0)
    solde_minimum = db.Column(db.Float, default=0)  # Seuil minimum d'alerte
    solde_maximum = db.Column(db.Float, default=1000000)  # Plafond maximum

    # Comptage
    dernier_comptage = db.Column(db.DateTime, nullable=True)
    ecart_comptage = db.Column(db.Float, default=0)  # Différence entre solde théorique et réel

    # Statistiques
    total_transactions_jour = db.Column(db.Integer, default=0)
    total_entrees_jour = db.Column(db.Float, default=0)
    total_sorties_jour = db.Column(db.Float, default=0)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relations
    succursale = db.relationship('Succursale', backref='caisses')
    agent = db.relationship('User', backref='caisse_assignee')
    transactions = db.relationship('TransactionCaisse', backref='caisse', lazy='dynamic')
    mouvements = db.relationship('MouvementCaisse', backref='caisse', lazy='dynamic')

    # Ajoutez ces nouveaux champs :
    dernier_jour_reinit = db.Column(db.Date, nullable=True)  # Dernier jour de réinitialisation
    dernier_mois_reinit = db.Column(db.Date, nullable=True)  # Dernier mois de réinitialisation

    # Statistiques mensuelles
    total_transactions_mois = db.Column(db.Integer, default=0)
    total_entrees_mois = db.Column(db.Float, default=0)
    total_sorties_mois = db.Column(db.Float, default=0)

    def __repr__(self):
        return f'<Caisse {self.numero}: {self.solde_actuel} FG>'

    @property
    def peut_ouvrir(self):
        """Vérifie si la caisse peut être ouverte"""
        return not self.est_ouverte and self.agent_id is not None

    @property
    def peut_fermer(self):
        """Vérifie si la caisse peut être fermée"""
        return self.est_ouverte

    @property
    def alerte_solde(self):
        """Vérifie si le solde est en alerte"""
        if self.solde_actuel < self.solde_minimum:
            return {'couleur': 'danger', 'message': 'Solde trop bas'}
        elif self.solde_actuel > self.solde_maximum:
            return {'couleur': 'warning', 'message': 'Solde trop élevé'}
        return {'couleur': 'success', 'message': 'Solde normal'}

    def ouvrir(self, agent_id, solde_initial):
        """Ouvre la caisse"""
        self.est_ouverte = True
        self.agent_id = agent_id
        self.solde_initial = solde_initial
        self.solde_actuel = solde_initial
        self.date_ouverture = datetime.now()

        # Enregistrer le mouvement
        mouvement = MouvementCaisse(
            caisse_id=self.id,
            type_mouvement='ouverture',
            montant=solde_initial,
            solde_apres=solde_initial,
            description=f"Ouverture de caisse - Solde initial: {solde_initial} HTG"
        )
        db.session.add(mouvement)
        db.session.commit()

    def fermer(self, solde_reel, commentaire=None):
        """Ferme la caisse avec comptage"""
        self.est_ouverte = False
        self.date_fermeture = datetime.now()
        self.dernier_comptage = datetime.now()
        self.ecart_comptage = solde_reel - self.solde_actuel

        # Enregistrer le mouvement
        mouvement = MouvementCaisse(
            caisse_id=self.id,
            type_mouvement='fermeture',
            montant=solde_reel,
            solde_apres=solde_reel,
            description=f"Fermeture de caisse - Écart: {self.ecart_comptage} FG. {commentaire or ''}"
        )
        db.session.add(mouvement)
        db.session.commit()

        return self.ecart_comptage

    def ajouter_transaction(self, montant, type_transaction, description):
        """Ajoute une transaction à la caisse"""
        from datetime import date

        # Vérifier et réinitialiser les compteurs quotidiens si nécessaire
        aujourd_hui = date.today()
        if self.dernier_jour_reinit != aujourd_hui:
            self.reinitialiser_quotidien()
            self.dernier_jour_reinit = aujourd_hui

        # Vérifier et réinitialiser les compteurs mensuels si nécessaire
        premier_jour_mois = date.today().replace(day=1)
        if self.dernier_mois_reinit != premier_jour_mois:
            self.reinitialiser_mensuel()
            self.dernier_mois_reinit = premier_jour_mois

        # Mettre à jour le solde
        if type_transaction == 'entree':
            self.solde_actuel += montant
            self.total_entrees_jour += montant
            self.total_entrees_mois += montant
        else:  # sortie
            self.solde_actuel -= montant
            self.total_sorties_jour += montant
            self.total_sorties_mois += montant

        self.total_transactions_jour += 1
        self.total_transactions_mois += 1

        # Enregistrer la transaction
        transaction = TransactionCaisse(
            caisse_id=self.id,
            type_transaction=type_transaction,
            montant=montant,
            solde_apres=self.solde_actuel,
            description=description,
            date_transaction=datetime.now()  # Assurez-vous que ce champ existe
        )
        db.session.add(transaction)
        db.session.commit()

        return transaction

    def reinitialiser_quotidien(self):
        """Réinitialise les compteurs quotidiens"""
        self.total_transactions_jour = 0
        self.total_entrees_jour = 0
        self.total_sorties_jour = 0
        db.session.commit()

    def reinitialiser_mensuel(self):
        """Réinitialise les compteurs mensuels"""
        self.total_transactions_mois = 0
        self.total_entrees_mois = 0
        self.total_sorties_mois = 0
        db.session.commit()


class TransactionCaisse(db.Model):
    __tablename__ = 'transactions_caisse'

    id = db.Column(db.Integer, primary_key=True)
    caisse_id = db.Column(db.Integer, db.ForeignKey('caisses.id'), nullable=False)

    # Type de transaction
    type_transaction = db.Column(db.String(20))  # 'entree', 'sortie', 'virement'
    categorie = db.Column(db.String(50))  # 'depot', 'retrait', 'remboursement', 'credit'

    # Montant
    montant = db.Column(db.Float, nullable=False)
    solde_avant = db.Column(db.Float)
    solde_apres = db.Column(db.Float)

    # Références
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Description
    description = db.Column(db.Text, nullable=True)

    # Date
    date_transaction = db.Column(db.DateTime, default=datetime.utcnow)

    compte_caisse_id = db.Column(db.Integer, db.ForeignKey('comptes_caisse.id'), nullable=False)

    def __repr__(self):
        return f'<TransactionCaisse {self.id}: {self.type_transaction} {self.montant} HTG>'


class MouvementCaisse(db.Model):
    __tablename__ = 'mouvements_caisse'

    id = db.Column(db.Integer, primary_key=True)
    caisse_id = db.Column(db.Integer, db.ForeignKey('caisses.id'), nullable=False)

    type_mouvement = db.Column(db.String(50))  # 'ouverture', 'fermeture', 'approvisionnement', 'retrait'
    montant = db.Column(db.Float, nullable=False)
    solde_apres = db.Column(db.Float)

    description = db.Column(db.Text, nullable=True)
    date_mouvement = db.Column(db.DateTime, default=datetime.utcnow)

    # Approbation
    approuve_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    date_approbation = db.Column(db.DateTime, nullable=True)


## 🎟️ **Classe FileAttente**

class FileAttente(db.Model):
    __tablename__ = 'file_attente'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=False)
    caisse_id = db.Column(db.Integer, db.ForeignKey('caisses.id'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)

    # Ticket
    numero_ticket = db.Column(db.String(20), nullable=False)  # Format: A001, B002, etc.
    prefixe = db.Column(db.String(5), default='A')  # A: Comptes, B: Crédits, C: Caisse

    # Service demandé
    service = db.Column(db.String(50))  # 'depot', 'retrait', 'credit', 'info', 'paiement'

    # Dates
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_appel = db.Column(db.DateTime, nullable=True)
    date_debut_service = db.Column(db.DateTime, nullable=True)
    date_fin_service = db.Column(db.DateTime, nullable=True)

    # Statut
    statut = db.Column(db.String(200), default='en_attente')  # 'en_attente', 'appele', 'en_cours', 'termine', 'annule'

    # Temps d'attente
    temps_estime = db.Column(db.Integer, default=0)  # en minutes
    position_initiale = db.Column(db.Integer)  # Position dans la file

    # Satisfaction
    satisfaction = db.Column(db.Integer, nullable=True)  # Note 1-5
    commentaire = db.Column(db.Text, nullable=True)

    # Métadonnées
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relations
    succursale = db.relationship('Succursale', backref='file_attente')
    caisse = db.relationship('Caisse', backref='clients_servis')
    client = db.relationship('Client', backref='passages_file')
    agent = db.relationship('User', foreign_keys=[created_by], backref='tickets_emis')

    def __repr__(self):
        return f'<FileAttente {self.numero_ticket}: {self.statut}>'

    @property
    def temps_attente_reel(self):
        """Calcule le temps d'attente réel en minutes"""
        if self.date_appel and self.date_creation:
            delta = self.date_appel - self.date_creation
            return round(delta.total_seconds() / 60, 1)
        return None

    @property
    def duree_service(self):
        """Calcule la durée du service en minutes"""
        if self.date_fin_service and self.date_debut_service:
            delta = self.date_fin_service - self.date_debut_service
            return round(delta.total_seconds() / 60, 1)
        return None

    @property
    def couleur_statut(self):
        """Couleur pour l'affichage du statut"""
        couleurs = {
            'en_attente': 'warning',
            'appele': 'info',
            'en_cours': 'primary',
            'termine': 'success',
            'annule': 'secondary'
        }
        return couleurs.get(self.statut, 'secondary')

    def appeler(self, caisse_id):
        """Appelle le client à une caisse"""
        self.statut = 'appele'
        self.caisse_id = caisse_id
        self.date_appel = datetime.now()
        db.session.commit()

    def commencer_service(self):
        """Débute le service"""
        self.statut = 'en_cours'
        self.date_debut_service = datetime.now()
        db.session.commit()

    def terminer(self, satisfaction=None, commentaire=None):
        """Termine le service"""
        self.statut = 'termine'
        self.date_fin_service = datetime.now()
        self.satisfaction = satisfaction
        self.commentaire = commentaire
        db.session.commit()

    def annuler(self, motif=None):
        """Annule le ticket"""
        self.statut = 'annule'
        self.commentaire = motif
        db.session.commit()

    @classmethod
    def generer_ticket(cls, succursale_id, service, prefixe='A'):
        """Génère un nouveau numéro de ticket"""
        aujourd_hui = datetime.now().date()

        # Compter les tickets du jour
        nb_tickets = cls.query.filter(
            cls.succursale_id == succursale_id,
            func.date(cls.date_creation) == aujourd_hui,
            cls.prefixe == prefixe
        ).count()

        numero = f"{prefixe}{nb_tickets + 1:03d}"

        return numero

    @classmethod
    def prochain_client(cls, succursale_id):
        """Récupère le prochain client dans la file"""
        return cls.query.filter_by(
            succursale_id=succursale_id,
            statut='en_attente'
        ).order_by(cls.date_creation).first()


## ⚠️ **Classe Anomalie**

class Anomalie(db.Model):
    __tablename__ = 'anomalies'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=False)
    signaler_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    traitee_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Type d'anomalie
    type_anomalie = db.Column(db.String(50))  # 'technique', 'caisse', 'transaction', 'securite', 'client'
    priorite = db.Column(db.String(20), default='moyenne')  # 'basse', 'moyenne', 'haute', 'critique'

    # Description
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Éléments associés
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=True)
    caisse_id = db.Column(db.Integer, db.ForeignKey('caisses.id'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)

    # Pièces jointes
    pieces_jointes = db.Column(db.JSON, default=list)  # URLs des photos/documents

    # Dates
    date_signalement = db.Column(db.DateTime, default=datetime.utcnow)
    date_traitement = db.Column(db.DateTime, nullable=True)
    date_resolution = db.Column(db.DateTime, nullable=True)

    # Traitement
    statut = db.Column(db.String(20), default='nouvelle')  # 'nouvelle', 'en_cours', 'traitee', 'cloturee'
    action_entreprise = db.Column(db.Text, nullable=True)
    commentaire_resolution = db.Column(db.Text, nullable=True)

    # Escalade
    necessite_escalade = db.Column(db.Boolean, default=False)
    escalade_a = db.Column(db.String(100), nullable=True)  # 'superviseur', 'direction', 'it'
    date_escalade = db.Column(db.DateTime, nullable=True)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relations
    succursale = db.relationship('Succursale', backref='anomalies')
    signaleur = db.relationship('User', foreign_keys=[signaler_par_id], backref='anomalies_signalees')
    traitant = db.relationship('User', foreign_keys=[traitee_par_id], backref='anomalies_traitees')

    def __repr__(self):
        return f'<Anomalie {self.id}: {self.type_anomalie} - {self.statut}>'

    @property
    def delai_traitement(self):
        """Délai de traitement en heures"""
        if self.date_traitement and self.date_signalement:
            delta = self.date_traitement - self.date_signalement
            return round(delta.total_seconds() / 3600, 1)
        return None

    @property
    def couleur_priorite(self):
        """Couleur pour l'affichage de la priorité"""
        couleurs = {
            'basse': 'info',
            'moyenne': 'warning',
            'haute': 'danger',
            'critique': 'dark'
        }
        return couleurs.get(self.priorite, 'secondary')

    @property
    def icone_type(self):
        """Icône selon le type d'anomalie"""
        icones = {
            'technique': 'fa-cogs',
            'caisse': 'fa-cash-register',
            'transaction': 'fa-exchange-alt',
            'securite': 'fa-shield-alt',
            'client': 'fa-user'
        }
        return icones.get(self.type_anomalie, 'fa-exclamation-triangle')

    def prendre_en_charge(self, employe_id):
        """Prend l'anomalie en charge"""
        self.statut = 'en_cours'
        self.traitee_par_id = employe_id
        self.date_traitement = datetime.now()
        db.session.commit()

    def resoudre(self, employe_id, action, commentaire=None):
        """Résout l'anomalie"""
        self.statut = 'traitee'
        self.traitee_par_id = employe_id
        self.date_resolution = datetime.now()
        self.action_entreprise = action
        self.commentaire_resolution = commentaire
        db.session.commit()

    def escalader(self, employe_id, destinataire, motif):
        """Escalade l'anomalie"""
        self.necessite_escalade = True
        self.escalade_a = destinataire
        self.date_escalade = datetime.now()
        self.commentaire_resolution = f"Escalade à {destinataire}: {motif}"
        db.session.commit()

    def fermer(self, employe_id, commentaire=None):
        """Ferme l'anomalie"""
        self.statut = 'cloturee'
        self.commentaire_resolution = commentaire
        db.session.commit()


## ☕ **Classe Pause**

class Pause(db.Model):
    __tablename__ = 'pauses'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approuve_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Type de pause
    type_pause = db.Column(db.String(20), default='pause')  # 'pause', 'dejeuner', 'formation', 'reunion'

    # Dates
    debut = db.Column(db.DateTime, nullable=False)
    fin = db.Column(db.DateTime, nullable=True)
    fin_prevue = db.Column(db.DateTime, nullable=True)

    # Statut
    statut = db.Column(db.String(20), default='en_cours')  # 'en_cours', 'terminee', 'depassee'

    # Durée
    duree_planifiee = db.Column(db.Integer, default=15)  # en minutes
    duree_reelle = db.Column(db.Integer, nullable=True)  # en minutes

    # Justification
    motif = db.Column(db.String(200), nullable=True)

    # Approbation
    est_approuvee = db.Column(db.Boolean, default=False)
    date_approbation = db.Column(db.DateTime, nullable=True)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    employe = db.relationship('User', foreign_keys=[employe_id], backref='pauses')
    approuve_par = db.relationship('User', foreign_keys=[approuve_par_id], backref='pauses_approuvees')

    def __repr__(self):
        return f'<Pause {self.id}: {self.employe.nom} - {self.debut.strftime("%H:%M")}>'

    @property
    def duree_actuelle(self):
        """Durée actuelle de la pause"""
        if self.fin:
            delta = self.fin - self.debut
            return int(delta.total_seconds() / 60)
        elif self.debut:
            delta = datetime.now() - self.debut
            return int(delta.total_seconds() / 60)
        return 0

    @property
    def est_depassee(self):
        """Vérifie si la pause dépasse la durée planifiée"""
        if not self.fin and self.debut:
            return self.duree_actuelle > self.duree_planifiee
        return False

    @property
    def temps_depassement(self):
        """Temps de dépassement en minutes"""
        if self.est_depassee:
            return self.duree_actuelle - self.duree_planifiee
        return 0

    @property
    def couleur_statut(self):
        """Couleur pour l'affichage"""
        if self.est_depassee:
            return 'danger'
        elif self.statut == 'terminee':
            return 'success'
        else:
            return 'warning'

    def terminer(self):
        """Termine la pause"""
        self.fin = datetime.now()
        self.duree_reelle = self.duree_actuelle

        if self.duree_reelle > self.duree_planifiee:
            self.statut = 'depassee'
        else:
            self.statut = 'terminee'

        db.session.commit()

    def approuver(self, approbateur_id):
        """Approuve la pause"""
        self.est_approuvee = True
        self.approuve_par_id = approbateur_id
        self.date_approbation = datetime.now()
        db.session.commit()

    @classmethod
    def get_pauses_en_cours(cls, succursale_id=None):
        """Récupère toutes les pauses en cours"""
        query = cls.query.filter_by(statut='en_cours')

        if succursale_id:
            query = query.join(User).filter(User.succursale_id == succursale_id)

        return query.all()


class Epargne(db.Model):
    __tablename__ = 'epargnes'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    produit_epargne_id = db.Column(db.Integer, db.ForeignKey('produits_epargne.id'), nullable=False)
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Agent qui a ouvert le compte
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=False)

    bloque = db.Column(db.Boolean, default=False)

    # Informations du compte
    numero_compte = db.Column(db.String(20), unique=True, nullable=False)
    intitule_compte = db.Column(db.String(200), nullable=True)

    # Solde et transactions
    solde = db.Column(db.Float, default=0)
    solde_bloque = db.Column(db.Float, default=0)  # Montant bloqué (garanties, etc.)
    solde_disponible = db.Column(db.Float, default=0)

    # Plafonds
    plafond_depot_journalier = db.Column(db.Float, default=1000000)
    plafond_retrait_journalier = db.Column(db.Float, default=500000)
    plafond_operation = db.Column(db.Float, default=200000)

    # Totaux journaliers
    total_depot_jour = db.Column(db.Float, default=0)
    total_retrait_jour = db.Column(db.Float, default=0)
    date_derniere_maj_totaux = db.Column(db.Date, default=datetime.now().date)

    # Dates
    date_ouverture = db.Column(db.DateTime, default=datetime.utcnow)
    date_derniere_transaction = db.Column(db.DateTime, nullable=True)
    date_cloture = db.Column(db.DateTime, nullable=True)

    # Statut
    statut = db.Column(db.String(20), default='actif')  # 'actif', 'inactif', 'cloture', 'bloque'
    motif_cloture = db.Column(db.String(200), nullable=True)

    # Intérêts
    taux_interet = db.Column(db.Float, default=0)  # Taux annuel en %
    interets_courus = db.Column(db.Float, default=0)
    date_dernier_calcul_interets = db.Column(db.Date, nullable=True)

    # Options
    avec_carnet = db.Column(db.Boolean, default=False)
    numero_carnet = db.Column(db.String(50), nullable=True)
    avec_carte = db.Column(db.Boolean, default=False)
    numero_carte = db.Column(db.String(50), nullable=True)

    # Garanties
    est_garantie_pret = db.Column(db.Boolean, default=False)
    pret_garanti_id = db.Column(db.Integer, db.ForeignKey('credits.id'), nullable=True)
    montant_garanti = db.Column(db.Float, default=0)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relations
    client = db.relationship('Client', backref='comptes_epargne')
    produit = db.relationship('ProduitEpargne', backref='comptes')
    employe = db.relationship('User', foreign_keys=[employe_id], backref='comptes_ouverts')
    succursale = db.relationship('Succursale', backref='epargnes')

    # Après (corrigé - utilise compte_id)
    transactions = db.relationship('TransactionEpargne',
                                   foreign_keys='TransactionEpargne.compte_id',
                                   backref='compte',
                                   lazy='dynamic')

    pret_garanti = db.relationship('Credit', foreign_keys=[pret_garanti_id], backref='epargne_garantie')

    # Transferts où ce compte est la source
    transferts_sortants = db.relationship('TransactionEpargne',
                                          foreign_keys='TransactionEpargne.transfert_source_id',
                                          backref='source_epargne',
                                          lazy='dynamic')

    # Transferts où ce compte est la destination
    transferts_entrants = db.relationship('TransactionEpargne',
                                          foreign_keys='TransactionEpargne.transfert_destination_id',
                                          backref='dest_epargne',
                                          lazy='dynamic')

    def __repr__(self):
        return f'<Epargne {self.numero_compte}: {self.solde} HTG>'

    @property
    def solde_net(self):
        """Solde net après déduction des montants bloqués"""
        return self.solde - self.solde_bloque

    # @property
    def peut_retirer(self, montant):
        """Vérifie si un retrait est possible"""
        if self.statut != 'actif':
            return False, "Compte inactif"

        if self.bloque:
            return False, "Compte bloqué"

        if montant > self.solde_disponible:
            return False, "Solde insuffisant"

        if montant > self.plafond_retrait_journalier - self.total_retrait_jour:
            return False, "Plafond de retrait journalier atteint"

        return True, "Retrait possible"


    def peut_deposer(self, montant):
        """Vérifie si un dépôt est possible"""
        # uniquement refusé si clôturé
        if self.statut == 'cloture':
            return False, "Compte clôturé"

        if montant > self.plafond_depot_journalier - self.total_depot_jour:
            return False, "Plafond de dépôt journalier atteint"

        return True, "Dépôt possible"

    def deposer(self, montant, description=None, transaction_ref=None):
        """Effectue un dépôt sur le compte"""
        peut, message = self.peut_deposer(montant)
        if not peut:
            raise ValueError(message)

        # Mettre à jour le solde
        ancien_solde = self.solde
        self.solde += montant
        self.solde_disponible = self.solde - self.solde_bloque
        self.total_depot_jour += montant
        self.date_derniere_transaction = datetime.now()

        # Réinitialiser les totaux si nouveau jour
        self._reinitialiser_totaux_journaliers()

        # Créer la transaction
        transaction = TransactionEpargne(
            compte_id=self.id,
            type_transaction='depot',
            montant=montant,
            solde_avant=ancien_solde,
            solde_apres=self.solde,
            description=description,
            transaction_externe_ref=transaction_ref
        )
        db.session.add(transaction)
        db.session.commit()

        return transaction

    def retirer(self, montant, description=None, transaction_ref=None):
        """Effectue un retrait du compte"""
        peut, message = self.peut_retirer(montant)
        if not peut:
            raise ValueError(message)

        # Mettre à jour le solde
        ancien_solde = self.solde
        self.solde -= montant
        self.solde_disponible = self.solde - self.solde_bloque
        self.total_retrait_jour += montant
        self.date_derniere_transaction = datetime.now()

        # Réinitialiser les totaux si nouveau jour
        self._reinitialiser_totaux_journaliers()

        # Créer la transaction
        transaction = TransactionEpargne(
            compte_id=self.id,
            type_transaction='retrait',
            montant=montant,
            solde_avant=ancien_solde,
            solde_apres=self.solde,
            description=description,
            transaction_externe_ref=transaction_ref
        )
        db.session.add(transaction)
        db.session.commit()

        return transaction

    def bloquer_montant(self, montant, motif, pret_id=None):
        """Bloque un montant sur le compte (pour garantie)"""
        if montant > self.solde_disponible:
            raise ValueError("Montant à bloquer supérieur au solde disponible")

        self.solde_bloque += montant
        self.solde_disponible = self.solde - self.solde_bloque
        self.est_garantie_pret = True
        self.pret_garanti_id = pret_id
        self.montant_garanti = montant

        # Créer une transaction de blocage
        transaction = TransactionEpargne(
            compte_id=self.id,
            type_transaction='blocage',
            montant=montant,
            solde_avant=self.solde + montant,  # Solde avant blocage
            solde_apres=self.solde,
            description=f"Blocage pour garantie: {motif}"
        )
        db.session.add(transaction)
        db.session.commit()

    def debloquer_montant(self, montant=None, motif=None):
        """Débloque un montant sur le compte"""
        if montant is None:
            montant = self.solde_bloque

        if montant > self.solde_bloque:
            raise ValueError("Montant à débloquer supérieur au montant bloqué")

        self.solde_bloque -= montant
        self.solde_disponible = self.solde - self.solde_bloque

        if self.solde_bloque == 0:
            self.est_garantie_pret = False
            self.pret_garanti_id = None
            self.montant_garanti = 0

        # Créer une transaction de déblocage
        transaction = TransactionEpargne(
            compte_id=self.id,
            type_transaction='deblocage',
            montant=montant,
            solde_avant=self.solde + montant,
            solde_apres=self.solde,
            description=f"Déblocage de garantie: {motif}"
        )
        db.session.add(transaction)
        db.session.commit()

    def calculer_interets(self):
        """Calcule les intérêts courus"""
        from datetime import date

        aujourd_hui = date.today()

        if self.date_dernier_calcul_interets:
            jours = (aujourd_hui - self.date_dernier_calcul_interets).days
        else:
            jours = (aujourd_hui - self.date_ouverture.date()).days

        if jours > 0:
            interets = self.solde * (self.taux_interet / 100) * (jours / 365)
            self.interets_courus += interets
            self.date_dernier_calcul_interets = aujourd_hui
            db.session.commit()

            return interets
        return 0

    def capitaliser_interets(self):
        """Capitalise les intérêts (les ajoute au solde)"""
        if self.interets_courus > 0:
            self.solde += self.interets_courus
            self.solde_disponible = self.solde - self.solde_bloque

            # Créer une transaction d'intérêts
            transaction = TransactionEpargne(
                compte_id=self.id,
                type_transaction='interets',
                montant=self.interets_courus,
                solde_avant=self.solde - self.interets_courus,
                solde_apres=self.solde,
                description="Capitalisation des intérêts"
            )
            db.session.add(transaction)

            self.interets_courus = 0
            db.session.commit()

    def cloturer(self, motif, agent_id):
        """Clôture le compte d'épargne"""
        if self.solde > 0:
            raise ValueError("Le compte a un solde positif. Veuillez d'abord vider le compte.")

        self.statut = 'cloture'
        self.date_cloture = datetime.now()
        self.motif_cloture = motif
        self.employe_id = agent_id  # ✅ CORRECT
        db.session.commit()

    def _reinitialiser_totaux_journaliers(self):
        """Réinitialise les totaux journaliers si nouveau jour"""
        aujourd_hui = datetime.now().date()
        if self.date_derniere_maj_totaux != aujourd_hui:
            self.total_depot_jour = 0
            self.total_retrait_jour = 0
            self.date_derniere_maj_totaux = aujourd_hui

    @classmethod
    def generer_numero_compte(cls, succursale_code, produit_code):
        """Génère un numéro de compte unique"""
        import random
        import string

        # Format: SCC-AAAA-XXXXX (S=Succursale, P=Produit)
        annees = datetime.now().strftime('%y')
        mois = datetime.now().strftime('%m')
        sequence = ''.join(random.choices(string.digits, k=5))

        numero = f"{succursale_code}-{produit_code}-{annees}{mois}-{sequence}"

        # Vérifier l'unicité
        while cls.query.filter_by(numero_compte=numero).first():
            sequence = ''.join(random.choices(string.digits, k=5))
            numero = f"{succursale_code}-{produit_code}-{annees}{mois}-{sequence}"

        return numero


from datetime import datetime

class Configuration(db.Model):
    __tablename__ = "configurations"

    id = db.Column(db.Integer, primary_key=True)

    # ================= FINANCE =================
    taux_interet = db.Column(db.Float, default=5.0)  # % mensuel
    frais_dossier = db.Column(db.Float, default=2.0)
    penalite_retard = db.Column(db.Float, default=3.0)
    commission_transfert = db.Column(db.Float, default=1.0)

    # ================= LIMITES =================
    max_pret = db.Column(db.Float, default=500000)
    min_pret = db.Column(db.Float, default=1000)
    duree_max = db.Column(db.Integer, default=24)
    solde_min = db.Column(db.Float, default=100)

    # ================= SYSTEME =================
    devise = db.Column(db.String(10), default="HTG")
    actif = db.Column(db.Boolean, default=True)

    # ================= AUDIT (IMPORTANT BANQUE) =================
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    commentaire = db.Column(db.Text)

    # ================= SCOPE =================
    succursale_id = db.Column(db.Integer, db.ForeignKey("succursale.id"))

    historique = db.relationship("ConfigurationHistory", backref="config")

    def __repr__(self):
        return f"<Config taux={self.taux_interet}% max_pret={self.max_pret}>"

class ConfigurationHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    config_id = db.Column(db.Integer, db.ForeignKey("configurations.id"))

    ancien_taux = db.Column(db.Float)
    nouveau_taux = db.Column(db.Float)

    date_changement = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer)

class TransactionEpargne(db.Model):
    __tablename__ = 'transactions_epargne'

    id = db.Column(db.Integer, primary_key=True)
    compte_id = db.Column(db.Integer, db.ForeignKey('epargnes.id'), nullable=False)

    # Type de transaction
    type_transaction = db.Column(db.String(20))  # 'depot', 'retrait', 'interets', 'blocage', 'deblocage'

    # Montant
    montant = db.Column(db.Float, nullable=False)
    solde_avant = db.Column(db.Float)
    solde_apres = db.Column(db.Float)

    # Description
    description = db.Column(db.Text, nullable=True)

    # Référence externe
    transaction_externe_ref = db.Column(db.String(100), nullable=True)  # Pour lier à une autre transaction
    transaction_ref = db.Column(db.String(100), nullable=True)  # ← Ajoutez ceci

    transfert_source_id = db.Column(db.Integer, db.ForeignKey('epargnes.id'), nullable=True)
    transfert_destination_id = db.Column(db.Integer, db.ForeignKey('epargnes.id'), nullable=True)
    transfert_motif = db.Column(db.String(50), default='autre')
    transfert_effectue_par = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Agent
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Date
    date_transaction = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    employe = db.relationship('User', foreign_keys=[employe_id], backref='transactions_epargne')
    status = db.Column(db.String(20), default="PENDING")

    def __repr__(self):
        return f'<TransactionEpargne {self.id}: {self.type_transaction} {self.montant} FG>'


class RetraitConfirmation(db.Model):
    __tablename__ = 'retrait_confirmations'
    id = db.Column(db.Integer, primary_key=True)

    token = db.Column(db.Text, unique=True, nullable=False)

    confirme = db.Column(db.Boolean, default=False)

    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))  # ← Ajoutez ceci
    transaction_id = db.Column(db.Integer)  # ← Ajoutez ceci

    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    employe_id = db.Column(db.Integer, nullable=True)  # ✅ AJOUTER CETTE LIGNE

class RetraitAttente(db.Model):
    __tablename__ = 'retraits_attente'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    compte_epargne_id = db.Column(db.Integer, db.ForeignKey('epargnes.id'), nullable=False)
    montant = db.Column(db.Numeric(15, 2), nullable=False)
    mode_retrait = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    token = db.Column(db.String(100), unique=True, nullable=False)
    token_expiration = db.Column(db.DateTime, nullable=False)
    statut = db.Column(db.String(50), default='en_attente_signature')
    employe_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_confirmation = db.Column(db.DateTime)

    # Relations
    client = db.relationship('Client', backref='retraits_attente')
    compte = db.relationship('Epargne', backref='retraits_attente')
    employe = db.relationship('Users', backref='retraits_inities')




class Maintenance(db.Model):
    __tablename__ = 'maintenances'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    type_maintenance = db.Column(db.String(50))  # preventive, curative, evolution, securite, sauvegarde
    date_debut = db.Column(db.DateTime, nullable=False)
    date_fin = db.Column(db.DateTime, nullable=False)
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=True)
    statut = db.Column(db.String(50), default='planifiee')  # planifiee, en_cours, terminee, annulee
    cree_par_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    succursale = db.relationship('Succursale', backref='maintenances')
    createur = db.relationship('User', backref='maintenances_planifiees')

    def __repr__(self):
        return f'<Maintenance {self.titre}>'


class ProduitEpargne(db.Model):
    __tablename__ = 'produits_epargne'

    id = db.Column(db.Integer, primary_key=True)

    # Informations du produit
    code = db.Column(db.String(20), unique=True, nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Type de produit
    type_produit = db.Column(db.String(50))  # 'classique', 'jeune', 'senior', 'entreprise', 'termine'

    # Taux d'intérêt
    taux_interet_annuel = db.Column(db.Float, default=0)
    taux_interet_mensuel = db.Column(db.Float, default=0)
    taux_initial = db.Column(db.Float, default=0)

    # Conditions d'ouverture
    depot_initial_min = db.Column(db.Float, default=0)
    depot_initial_max = db.Column(db.Float, default=10000000)
    age_min = db.Column(db.Integer, default=0)
    age_max = db.Column(db.Integer, default=120)

    # Plafonds
    solde_min = db.Column(db.Float, default=0)
    solde_max = db.Column(db.Float, default=100000000)
    plafond_depot_mensuel = db.Column(db.Float, default=5000000)
    plafond_retrait_mensuel = db.Column(db.Float, default=3000000)

    # Frais
    frais_ouverture = db.Column(db.Float, default=0)
    frais_tenue_compte_mensuel = db.Column(db.Float, default=0)
    frais_cloture = db.Column(db.Float, default=0)

    # Période de blocage (pour comptes à terme)
    duree_blocage_mois = db.Column(db.Integer, default=0)
    penalite_retrait_anticipe = db.Column(db.Float, default=0)  # Pourcentage

    # Statut
    est_actif = db.Column(db.Boolean, default=True)
    date_lancement = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=True)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ProduitEpargne {self.code}: {self.nom}>'

    @property
    def taux_annuel_en_pourcentage(self):
        return f"{self.taux_interet_annuel}%"

    def est_eligible(self, client):
        """Vérifie si un client est éligible à ce produit"""
        from datetime import date

        if client.date_naissance:
            age = date.today().year - client.date_naissance.year
            if age < self.age_min or age > self.age_max:
                return False, f"Âge non éligible ({self.age_min}-{self.age_max} ans)"

        return True, "Éligible"

    def calculer_interets_mensuels(self, solde):
        """Calcule les intérêts mensuels"""
        return solde * (self.taux_interet_annuel / 100) / 12


class CompteEpargneTerme(Epargne):
    __tablename__ = 'comptes_epargne_terme'

    id = db.Column(db.Integer, db.ForeignKey('epargnes.id'), primary_key=True)

    # Spécificités des comptes à terme
    montant_depose = db.Column(db.Float, nullable=False)
    date_echeance = db.Column(db.Date, nullable=False)
    taux_contractuel = db.Column(db.Float, nullable=False)

    # Options de renouvellement
    renouvellement_automatique = db.Column(db.Boolean, default=False)
    nb_renouvellements = db.Column(db.Integer, default=0)

    def calculer_montant_final(self):
        """Calcule le montant à l'échéance"""
        jours = (self.date_echeance - self.date_ouverture.date()).days
        interets = self.montant_depose * (self.taux_contractuel / 100) * (jours / 365)
        return self.montant_depose + interets

    def retirer_anticipe(self):
        """Retrait anticipé avec pénalité"""
        penalite = self.montant_depose * (self.produit.penalite_retrait_anticipe / 100)
        montant_net = self.montant_depose - penalite
        return montant_net


class HistoriqueEpargne(db.Model):
    __tablename__ = 'historique_epargne'

    id = db.Column(db.Integer, primary_key=True)
    compte_id = db.Column(db.Integer, db.ForeignKey('epargnes.id'), nullable=False)

    # Type d'événement
    evenement = db.Column(db.String(50))  # 'creation', 'modification', 'blocage', 'deblocage', 'cloture'

    # Anciennes et nouvelles valeurs
    anciennes_valeurs = db.Column(db.JSON, nullable=True)
    nouvelles_valeurs = db.Column(db.JSON, nullable=True)

    # Description
    description = db.Column(db.Text, nullable=True)

    # Agent
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Date
    date_evenement = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    compte = db.relationship('Epargne', backref='historique')
    agent = db.relationship('User', backref='actions_epargne')

    def __repr__(self):
        return f'<HistoriqueEpargne {self.id}: {self.evenement}>'




class PlanningPause(db.Model):
    __tablename__ = 'planning_pauses'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=False)

    # Créneaux
    creneaux = db.Column(db.JSON, default=list)  # Liste des créneaux horaires par équipe

    # Règles
    pause_max_consecutive = db.Column(db.Integer, default=15)  # minutes
    pauses_max_par_jour = db.Column(db.Integer, default=2)

    # Période
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=True)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<PlanningPause {self.id}: {self.date_debut}>'

    def get_creneaux_disponibles(self, date, equipe='matin'):
        """Récupère les créneaux disponibles pour une date"""
        if self.creneaux:
            for creneau in self.creneaux:
                if creneau.get('date') == str(date) and creneau.get('equipe') == equipe:
                    return creneau.get('creneaux', [])
        return []




class DemandeConge(db.Model):
    __tablename__ = 'demandes_conges'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    traitee_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Informations du congé
    type_conge = db.Column(db.String(50),
                           nullable=False)  # 'paye', 'maladie', 'maternite', 'sans_solde', 'exceptionnel'
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    nb_jours = db.Column(db.Integer, nullable=False)
    motif = db.Column(db.Text, nullable=True)

    # Statut
    statut = db.Column(db.String(200), default='en_attente')  # 'en_attente', 'approuve', 'refuse', 'annule'

    # Dates
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_traitement = db.Column(db.DateTime, nullable=True)

    # Commentaire du gestionnaire
    commentaire_traitement = db.Column(db.Text, nullable=True)

    # Relations
    employe = db.relationship('User', foreign_keys=[employe_id], backref='demandes_conges')
    traitee_par = db.relationship('User', foreign_keys=[traitee_par_id], backref='conges_traites')

    def __repr__(self):
        return f'<DemandeConge {self.id}: {self.employe.nom} - {self.type_conge}>'

    @property
    def jours_restants(self):
        """Calcule les jours restants avant la fin du congé"""
        if self.statut == 'approuve':
            aujourd_hui = datetime.now().date()
            if self.date_fin >= aujourd_hui:
                return (self.date_fin - aujourd_hui).days
        return 0

    @property
    def est_en_cours(self):
        """Vérifie si le congé est en cours"""
        aujourd_hui = datetime.now().date()
        return (self.statut == 'approuve' and
                self.date_debut <= aujourd_hui <= self.date_fin)

    def approuver(self, employe_id, commentaire=None):
        """Approuve la demande de congé"""
        self.statut = 'approuve'
        self.traitee_par_id = employe_id
        self.date_traitement = datetime.utcnow()
        self.commentaire_traitement = commentaire
        db.session.commit()

    def refuser(self, employe_id, commentaire=None):
        """Refuse la demande de congé"""
        self.statut = 'refuse'
        self.traitee_par_id = employe_id
        self.date_traitement = datetime.utcnow()
        self.commentaire_traitement = commentaire
        db.session.commit()



class FormationParticipant(db.Model):
    __tablename__ = 'formation_participants'

    id = db.Column(db.Integer, primary_key=True)
    formation_id = db.Column(db.Integer, db.ForeignKey('formations.id'), nullable=False)
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Statut de participation
    statut = db.Column(db.String(20), default='inscrit')  # 'inscrit', 'present', 'absent', 'termine'
    note = db.Column(db.Integer, nullable=True)  # Note sur 100
    commentaire = db.Column(db.Text, nullable=True)

    # Dates
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)
    date_presence = db.Column(db.DateTime, nullable=True)

    # Certificat
    certificat_genere = db.Column(db.Boolean, default=False)
    certificat_url = db.Column(db.String(500), nullable=True)

    # Relations
    user = db.relationship('User', backref='formations_suivies')

    __table_args__ = (
        db.UniqueConstraint('formation_id', 'employe_id', name='unique_participant'),
    )



class Candidature(db.Model):
    __tablename__ = 'candidatures'

    id = db.Column(db.Integer, primary_key=True)
    recrutement_id = db.Column(db.Integer, db.ForeignKey('recrutements.id'), nullable=False)

    # Informations personnelles
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telephone = db.Column(db.String(20), nullable=True)

    # Documents
    cv_url = db.Column(db.String(500), nullable=True)
    lettre_motivation_url = db.Column(db.String(500), nullable=True)

    # Statut de la candidature
    statut = db.Column(db.String(20),
                       default='nouvelle')  # 'nouvelle', 'vue', 'entretien', 'test', 'retenue', 'refusee'

    # Dates
    date_candidature = db.Column(db.DateTime, default=datetime.utcnow)
    date_derniere_maj = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Notes du recruteur
    notes = db.Column(db.Text, nullable=True)
    score = db.Column(db.Integer, nullable=True)  # Score sur 100

    # Entretiens
    date_entretien = db.Column(db.DateTime, nullable=True)
    commentaire_entretien = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Candidature {self.id}: {self.prenom} {self.nom} - {self.statut}>'

    def passer_entretien(self, date_entretien):
        """Planifier un entretien"""
        self.date_entretien = date_entretien
        self.statut = 'entretien'
        db.session.commit()

    def retenir(self):
        """Retenir la candidature"""
        self.statut = 'retenue'
        db.session.commit()

    def refuser(self, commentaire=None):
        """Refuser la candidature"""
        self.statut = 'refusee'
        self.notes = commentaire
        db.session.commit()


class HistoriquePointage(db.Model):
    __tablename__ = 'historique_pointages'

    id = db.Column(db.Integer, primary_key=True)
    pointage_id = db.Column(db.Integer, db.ForeignKey('pointages.id'))
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(50))  # 'arrivee', 'depart', 'modification'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text, nullable=True)
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Visite(db.Model):
    __tablename__ = 'visites'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    planifiee_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Type de visite
    type_visite = db.Column(db.String(50), nullable=False)  # 'domicile', 'travail', 'terrain', 'suivi', 'recouvrement'
    motif = db.Column(db.String(200), nullable=False)

    # Adresse de visite (peut être différente de l'adresse du client)
    adresse_visite = db.Column(db.String(200), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # Dates et heures
    date_planification = db.Column(db.DateTime, default=datetime.utcnow)
    date_visite_prevue = db.Column(db.DateTime, nullable=False)
    date_visite_reelle = db.Column(db.DateTime, nullable=True)
    duree_estimee = db.Column(db.Integer, default=30)  # en minutes
    duree_reelle = db.Column(db.Integer, nullable=True)  # en minutes

    # Statut
    statut = db.Column(db.String(20),
                       default='planifiee')  # 'planifiee', 'en_cours', 'effectuee', 'annulee', 'reportee'

    # Compte-rendu
    compte_rendu = db.Column(db.Text, nullable=True)
    observations = db.Column(db.Text, nullable=True)
    recommandations = db.Column(db.Text, nullable=True)

    # Résultats
    objectif_atteint = db.Column(db.Boolean, default=False)
    satisfaction_client = db.Column(db.Integer, nullable=True)  # Note 1-5

    # Documents
    photos = db.Column(db.JSON, default=list)  # URLs des photos prises
    signature_client = db.Column(db.String(500), nullable=True)  # URL de la signature

    # Pour les visites de recouvrement
    montant_recouvre = db.Column(db.Float, default=0)
    prochaine_visite_id = db.Column(db.Integer, db.ForeignKey('visites.id'), nullable=True)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relations
    client = db.relationship('Client', backref='visites')
    agent = db.relationship('User', foreign_keys=[agent_id], backref='visites_effectuees')
    planificateur = db.relationship('User', foreign_keys=[planifiee_par_id], backref='visites_planifiees')
    prochaine_visite = db.relationship('Visite', remote_side=[id], backref='visite_precedente')

    def __repr__(self):
        return f'<Visite {self.id}: {self.client.nom} - {self.date_visite_prevue.strftime("%d/%m/%Y")}>'

    @property
    def est_en_retard(self):
        """Vérifie si la visite est en retard"""
        if self.statut == 'planifiee' and datetime.now() > self.date_visite_prevue:
            return True
        return False

    @property
    def minutes_retard(self):
        """Minutes de retard"""
        if self.est_en_retard:
            delta = datetime.now() - self.date_visite_prevue
            return int(delta.total_seconds() / 60)
        return 0

    @property
    def couleur_statut(self):
        """Couleur pour l'affichage du statut"""
        couleurs = {
            'planifiee': 'info',
            'en_cours': 'warning',
            'effectuee': 'success',
            'annulee': 'secondary',
            'reportee': 'primary'
        }
        if self.est_en_retard and self.statut == 'planifiee':
            return 'danger'
        return couleurs.get(self.statut, 'secondary')

    def commencer(self):
        """Débute la visite"""
        self.statut = 'en_cours'
        self.date_visite_reelle = datetime.now()
        db.session.commit()

    def terminer(self, compte_rendu, objectif_atteint=False, satisfaction=None):
        """Termine la visite"""
        self.statut = 'effectuee'
        self.date_visite_reelle = datetime.now()
        self.compte_rendu = compte_rendu
        self.objectif_atteint = objectif_atteint
        self.satisfaction_client = satisfaction

        if self.date_visite_reelle and self.date_visite_prevue:
            delta = self.date_visite_reelle - self.date_visite_prevue
            self.duree_reelle = int(delta.total_seconds() / 60)

        db.session.commit()

    def annuler(self, motif):
        """Annule la visite"""
        self.statut = 'annulee'
        self.observations = motif
        db.session.commit()

    def reporter(self, nouvelle_date, motif):
        """Reporte la visite"""
        self.statut = 'reportee'
        self.observations = f"Reportée: {motif}"

        # Créer une nouvelle visite
        nouvelle_visite = Visite(
            client_id=self.client_id,
            employe_id=self.agent_id,
            planifiee_par_id=self.planifiee_par_id,
            type_visite=self.type_visite,
            motif=self.motif,
            adresse_visite=self.adresse_visite,
            date_visite_prevue=nouvelle_date,
            statut='planifiee'
        )
        db.session.add(nouvelle_visite)
        db.session.commit()

        return nouvelle_visite

    @classmethod
    def get_visites_du_jour(cls, employe_id=None):
        """Récupère les visites du jour"""
        aujourd_hui = datetime.now().date()
        query = cls.query.filter(
            func.date(cls.date_visite_prevue) == aujourd_hui
        )
        if employe_id:
            query = query.filter_by(employe_id=employe_id)
        return query.order_by(cls.date_visite_prevue).all()

    @classmethod
    def get_visites_a_venir(cls, employe_id=None, jours=7):
        """Récupère les visites à venir"""
        date_limite = datetime.now() + timedelta(days=jours)
        query = cls.query.filter(
            cls.date_visite_prevue <= date_limite,
            cls.statut == 'planifiee'
        )
        if employe_id:
            query = query.filter_by(employe_id=employe_id)
        return query.order_by(cls.date_visite_prevue).all()


## 👥 **Classe Reunion**

class Reunion(db.Model):
    __tablename__ = 'reunions'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    organisee_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    compte_rendu_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=True)

    # Informations de la réunion
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type_reunion = db.Column(db.String(50))  # 'equipe', 'direction', 'projet', 'formation', 'client'

    # Dates
    date_reunion = db.Column(db.DateTime, nullable=False)
    duree_prevue = db.Column(db.Integer, default=60)  # en minutes
    duree_reelle = db.Column(db.Integer, nullable=True)

    # Lieu
    lieu = db.Column(db.String(200), nullable=True)
    est_virtuelle = db.Column(db.Boolean, default=False)
    lien_virtuel = db.Column(db.String(500), nullable=True)

    # Participants
    participants = db.Column(db.JSON, default=list)  # Liste des IDs des participants
    participants_externes = db.Column(db.JSON, default=list)  # Noms des participants externes

    # Ordre du jour
    ordre_du_jour = db.Column(db.JSON, default=list)  # Liste des points à aborder

    # Compte-rendu
    compte_rendu = db.Column(db.Text, nullable=True)
    decisions = db.Column(db.JSON, default=list)  # Liste des décisions prises
    actions = db.Column(db.JSON, default=list)  # Liste des actions décidées

    # Pièces jointes
    documents = db.Column(db.JSON, default=list)  # URLs des documents

    # Statut
    statut = db.Column(db.String(20), default='planifiee')  # 'planifiee', 'en_cours', 'terminee', 'annulee'

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relations
    organisateur = db.relationship('User', foreign_keys=[organisee_par_id], backref='reunions_organisees')
    redacteur_cr = db.relationship('User', foreign_keys=[compte_rendu_par_id], backref='reunions_redigees')
    succursale = db.relationship('Succursale', backref='reunions')

    def __repr__(self):
        return f'<Reunion {self.id}: {self.titre} - {self.date_reunion.strftime("%d/%m/%Y")}>'

    @property
    def nb_participants(self):
        """Nombre de participants"""
        return len(self.participants) if self.participants else 0

    @property
    def est_passee(self):
        """Vérifie si la réunion est passée"""
        return datetime.now() > self.date_reunion

    @property
    def couleur_statut(self):
        """Couleur pour l'affichage"""
        if self.statut == 'terminee':
            return 'success'
        elif self.statut == 'en_cours':
            return 'warning'
        elif self.statut == 'planifiee':
            if self.est_passee:
                return 'danger'
            return 'info'
        else:
            return 'secondary'

    def ajouter_participant(self, employe_id):
        """Ajoute un participant à la réunion"""
        if not self.participants:
            self.participants = []
        if employe_id not in self.participants:
            self.participants.append(employe_id)
            db.session.commit()

    def retirer_participant(self, employe_id):
        """Retire un participant"""
        if self.participants and employe_id in self.participants:
            self.participants.remove(employe_id)
            db.session.commit()

    def commencer(self):
        """Débute la réunion"""
        self.statut = 'en_cours'
        db.session.commit()

    def terminer(self, compte_rendu=None, decisions=None, actions=None):
        """Termine la réunion"""
        self.statut = 'terminee'
        if compte_rendu:
            self.compte_rendu = compte_rendu
        if decisions:
            self.decisions = decisions
        if actions:
            self.actions = actions

        # Calculer la durée réelle
        if self.statut == 'en_cours':
            delta = datetime.now() - self.date_reunion
            self.duree_reelle = int(delta.total_seconds() / 60)

        db.session.commit()

    def annuler(self, motif):
        """Annule la réunion"""
        self.statut = 'annulee'
        self.description = f"{self.description}\n\nANNULÉE: {motif}" if self.description else f"ANNULÉE: {motif}"
        db.session.commit()

    @classmethod
    def get_reunions_du_jour(cls, employe_id=None):
        """Récupère les réunions du jour"""
        aujourd_hui = datetime.now().date()
        query = cls.query.filter(
            func.date(cls.date_reunion) == aujourd_hui
        )
        if employe_id:
            query = query.filter(cls.participants.contains([employe_id]) | (cls.organisee_par_id == employe_id))
        return query.order_by(cls.date_reunion).all()

    @classmethod
    def get_prochaines_reunions(cls, employe_id=None, limite=5):
        """Récupère les prochaines réunions"""
        maintenant = datetime.now()
        query = cls.query.filter(
            cls.date_reunion > maintenant,
            cls.statut == 'planifiee'
        ).order_by(cls.date_reunion)

        if employe_id:
            query = query.filter(cls.participants.contains([employe_id]) | (cls.organisee_par_id == employe_id))

        return query.limit(limite).all()





## ✅ **Classe Action**

class Action(db.Model):
    __tablename__ = 'actions'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    assignee_a_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creee_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reunion_id = db.Column(db.Integer, db.ForeignKey('reunions.id'), nullable=True)
    visite_id = db.Column(db.Integer, db.ForeignKey('visites.id'), nullable=True)

    # Informations de l'action
    pret_id = db.Column(db.Integer, db.ForeignKey('prets.id'), nullable=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type_action = db.Column(db.String(50))  # 'tache', 'decision', 'rappel', 'alerte'
    priorite = db.Column(db.String(20), default='moyenne')  # 'basse', 'moyenne', 'haute', 'critique'

    # Dates
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_echeance = db.Column(db.DateTime, nullable=False)
    date_realisation = db.Column(db.DateTime, nullable=True)
    date_action = db.Column(db.DateTime, default=datetime.utcnow)

    # Statut
    statut = db.Column(db.String(20), default='a_faire')  # 'a_faire', 'en_cours', 'terminee', 'annulee', 'en_retard'
    progression = db.Column(db.Integer, default=0)  # Pourcentage 0-100

    # Résultat
    resultat = db.Column(db.Text, nullable=True)
    commentaire = db.Column(db.Text, nullable=True)

    # Notifications
    notification_envoyee = db.Column(db.Boolean, default=False)
    date_notification = db.Column(db.DateTime, nullable=True)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relations
    assigne = db.relationship('User', foreign_keys=[assignee_a_id], backref='actions_assignees')
    createur = db.relationship('User', foreign_keys=[creee_par_id], backref='actions_creees')
    reunion = db.relationship('Reunion', backref='actions_associees')
    visite = db.relationship('Visite', backref='actions_associees')

    def __repr__(self):
        return f'<Action {self.id}: {self.titre} - {self.statut}>'

    @property
    def jours_restants(self):
        """Jours avant échéance"""
        if self.date_echeance:
            delta = self.date_echeance - datetime.now()
            return delta.days
        return None

    @property
    def est_en_retard(self):
        """Vérifie si l'action est en retard"""
        return (self.statut in ['a_faire', 'en_cours'] and
                datetime.now() > self.date_echeance)

    @property
    def couleur_priorite(self):
        """Couleur pour la priorité"""
        couleurs = {
            'basse': 'info',
            'moyenne': 'warning',
            'haute': 'danger',
            'critique': 'dark'
        }
        return couleurs.get(self.priorite, 'secondary')

    @property
    def couleur_statut(self):
        """Couleur pour le statut"""
        if self.est_en_retard:
            return 'danger'
        couleurs = {
            'a_faire': 'secondary',
            'en_cours': 'info',
            'terminee': 'success',
            'annulee': 'dark'
        }
        return couleurs.get(self.statut, 'secondary')

    def demarrer(self):
        """Démarre l'action"""
        self.statut = 'en_cours'
        db.session.commit()

    def mettre_a_jour_progression(self, progression):
        """Met à jour la progression"""
        self.progression = min(100, max(0, progression))
        if self.progression == 100:
            self.statut = 'terminee'
            self.date_realisation = datetime.now()
        db.session.commit()

    def terminer(self, resultat=None):
        """Termine l'action"""
        self.statut = 'terminee'
        self.progression = 100
        self.date_realisation = datetime.now()
        if resultat:
            self.resultat = resultat
        db.session.commit()

    def annuler(self, motif):
        """Annule l'action"""
        self.statut = 'annulee'
        self.commentaire = motif
        db.session.commit()

    def notifier_retard(self):
        """Marque la notification de retard comme envoyée"""
        self.notification_envoyee = True
        self.date_notification = datetime.now()
        db.session.commit()

    @classmethod
    def get_actions_urgentes(cls, employe_id=None):
        """Récupère les actions urgentes (échéance <= 2 jours)"""
        date_limite = datetime.now() + timedelta(days=2)
        query = cls.query.filter(
            cls.date_echeance <= date_limite,
            cls.statut.in_(['a_faire', 'en_cours'])
        ).order_by(cls.date_echeance)

        if employe_id:
            query = query.filter_by(assignee_a_id=employe_id)

        return query.all()

    @classmethod
    def get_actions_en_retard(cls, employe_id=None):
        """Récupère les actions en retard"""
        maintenant = datetime.now()
        query = cls.query.filter(
            cls.date_echeance < maintenant,
            cls.statut.in_(['a_faire', 'en_cours'])
        ).order_by(cls.date_echeance)

        if employe_id:
            query = query.filter_by(assignee_a_id=employe_id)

        return query.all()

    @classmethod
    def get_statistiques(cls, employe_id=None):
        """Statistiques des actions pour un utilisateur"""
        query = cls.query
        if employe_id:
            query = query.filter_by(assignee_a_id=employe_id)

        total = query.count()
        a_faire = query.filter_by(statut='a_faire').count()
        en_cours = query.filter_by(statut='en_cours').count()
        terminees = query.filter_by(statut='terminee').count()
        en_retard = cls.get_actions_en_retard(employe_id).count()

        return {
            'total': total,
            'a_faire': a_faire,
            'en_cours': en_cours,
            'terminees': terminees,
            'en_retard': en_retard,
            'taux_realisation': round((terminees / total * 100) if total > 0 else 0, 1)
        }


class TermsAcceptance(db.Model):
    __tablename__ = 'terms_acceptance'

    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(
        db.Integer,
        db.ForeignKey('clients.id'),
        nullable=False
    )

    date_acceptation = db.Column(db.DateTime, nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)

    client = db.relationship('Client', backref='terms_acceptances')

class Competence(db.Model):
    __tablename__ = "competences"

    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(
        db.Integer,
        db.ForeignKey("clients.id"),
        nullable=False
    )

    employe_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    nom = db.Column(db.String(100), nullable=False)
    niveau = db.Column(db.String(50))
    description = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    client = db.relationship(
        "Client",
        foreign_keys=[client_id],
        backref=db.backref("competences_client", lazy=True)
    )

    employe = db.relationship(
        "User",
        foreign_keys=[employe_id],
        backref=db.backref("competences_employe", lazy=True)
    )


class ErrorLog(db.Model):
    __tablename__ = 'error_logs'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    traceback = db.Column(db.Text)
    url = db.Column(db.String(500))

    # Sans foreign key - juste des entiers
    employe_id = db.Column(db.Integer, nullable=True)
    succursale_id = db.Column(db.Integer, nullable=True)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    seen = db.Column(db.Boolean, default=False)
    level = db.Column(db.String(20), default='error')

    # Pas de relationships
    def __repr__(self):
        return f'<ErrorLog {self.id}: {self.message[:50]}>'




class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    auteur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, nullable=True)

    # Relations
    user = db.relationship('User', foreign_keys=[employe_id], backref='notes_recues')
    auteur = db.relationship('User', foreign_keys=[auteur_id], backref='notes_ecrites')

    def __repr__(self):
        return f'<Note {self.id} - {self.auteur.prenom} -> {self.user.prenom}>'

    def modifier(self, nouveau_contenu):
        """Modifier le contenu de la note"""
        self.contenu = nouveau_contenu
        self.date_modification = datetime.utcnow()


class ContactHistorique(db.Model):
    __tablename__ = 'contacts_historique'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # email, sms, les_deux
    sujet = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_envoi = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.String(20), default='envoyé')  # envoyé, échoué, en_attente
    erreur = db.Column(db.Text, nullable=True)

    # Relations
    admin = db.relationship('User', foreign_keys=[admin_id], backref='contacts_envoyes')
    user = db.relationship('User', foreign_keys=[employe_id], backref='contacts_recus')

    def __repr__(self):
        return f'<Contact {self.id} - {self.type} - {self.sujet[:30]}>'

    @property
    def type_icone(self):
        """Retourne l'icône Font Awesome correspondant au type"""
        icons = {
            'email': 'fa-envelope',
            'sms': 'fa-phone',
            'les_deux': 'fa-envelope-open-text'
        }
        return icons.get(self.type, 'fa-bell')

    @property
    def type_libelle(self):
        """Retourne le libellé du type de contact"""
        libelles = {
            'email': 'Email',
            'sms': 'SMS',
            'les_deux': 'Email + SMS'
        }
        return libelles.get(self.type, self.type)

    @classmethod
    def get_contacts_by_user(cls, employe_id, limit=50):
        """Récupère l'historique des contacts pour un utilisateur"""
        return cls.query.filter_by(employe_id=employe_id).order_by(cls.date_envoi.desc()).limit(limit).all()

    @classmethod
    def get_contacts_by_admin(cls, admin_id, limit=50):
        """Récupère l'historique des contacts envoyés par un admin"""
        return cls.query.filter_by(admin_id=admin_id).order_by(cls.date_envoi.desc()).limit(limit).all()


class HistoriqueAction(db.Model):
    __tablename__ = 'historique_actions'

    id = db.Column(db.Integer, primary_key=True)
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=True)
    ip = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relation
    user = db.relationship('User', backref='historique_actions')

    def __repr__(self):
        return f'<Historique {self.id} - {self.action} - {self.date.strftime("%d/%m/%Y %H:%M")}>'

    @classmethod
    def ajouter(cls, employe_id, action, details=None, request=None):
        """Ajoute une entrée dans l'historique"""
        historique = cls(
            employe_id=employe_id,
            action=action,
            details=details,
            ip=request.remote_addr if request else None,
            user_agent=request.user_agent.string if request and request.user_agent else None
        )
        db.session.add(historique)
        db.session.commit()
        return historique

    @classmethod
    def get_by_user(cls, employe_id, limit=50):
        """Récupère l'historique d'un utilisateur"""
        return cls.query.filter_by(employe_id=employe_id).order_by(cls.date.desc()).limit(limit).all()

    @classmethod
    def get_by_action(cls, action, limit=50):
        """Récupère l'historique par type d'action"""
        return cls.query.filter_by(action=action).order_by(cls.date.desc()).limit(limit).all()

    @classmethod
    def get_recent(cls, limit=100):
        """Récupère les actions récentes"""
        return cls.query.order_by(cls.date.desc()).limit(limit).all()

    @property
    def action_icone(self):
        """Retourne l'icône Font Awesome selon l'action"""
        icons = {
            'connexion': 'fa-sign-in-alt',
            'deconnexion': 'fa-sign-out-alt',
            'creation': 'fa-plus-circle',
            'modification': 'fa-edit',
            'suppression': 'fa-trash-alt',
            'approbation': 'fa-check-circle',
            'rejet': 'fa-times-circle',
            'blocage': 'fa-ban',
            'deblocage': 'fa-check-circle',
            'transfert': 'fa-exchange-alt',
            'suspension': 'fa-pause-circle',
            'activation': 'fa-play-circle',
            'envoi_email': 'fa-envelope',
            'envoi_sms': 'fa-phone',
            'consultation': 'fa-eye',
            'export': 'fa-download',
            'import': 'fa-upload',
            'paiement': 'fa-money-bill-wave',
            'remboursement': 'fa-hand-holding-usd',
            'pret': 'fa-hand-holding-heart',
        }
        # Chercher une correspondance partielle
        for key, icon in icons.items():
            if key in self.action.lower():
                return icon
        return 'fa-history'

    @property
    def action_classe(self):
        """Retourne la classe CSS selon l'action"""
        classes = {
            'connexion': 'info',
            'deconnexion': 'secondary',
            'creation': 'success',
            'modification': 'warning',
            'suppression': 'danger',
            'approbation': 'success',
            'rejet': 'danger',
            'blocage': 'danger',
            'deblocage': 'success',
            'transfert': 'info',
            'suspension': 'warning',
            'activation': 'success',
            'envoi_email': 'info',
            'envoi_sms': 'info',
            'consultation': 'secondary',
            'export': 'primary',
            'import': 'primary',
            'paiement': 'success',
            'remboursement': 'success',
            'pret': 'warning',
        }
        for key, classe in classes.items():
            if key in self.action.lower():
                return classe
        return 'secondary'


class Dossier(db.Model):
    __tablename__ = 'dossiers'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    # === LIENS ===
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Propriétaire du dossier
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Agent responsable

    # === INFORMATIONS GÉNÉRALES ===
    reference = db.Column(db.String(50), unique=True, nullable=False)  # DOS-2024-0001
    type = db.Column(db.String(50), nullable=False)  # 'client', 'employe', 'pret', 'document'
    statut = db.Column(db.String(50), default='actif')  # 'actif', 'archive', 'en_attente', 'cloture'

    # === MÉTADONNÉES ===
    nom = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, onupdate=datetime.utcnow)
    date_cloture = db.Column(db.DateTime, nullable=True)

    # === PRIORITÉ ET TAGS ===
    priorite = db.Column(db.String(20), default='normale')  # 'basse', 'normale', 'haute', 'urgente'
    tags = db.Column(db.String(500), nullable=True)  # Stocké comme JSON ou texte séparé par virgules

    # === STATISTIQUES ===
    nb_documents = db.Column(db.Integer, default=0)
    nb_notes = db.Column(db.Integer, default=0)
    nb_actions = db.Column(db.Integer, default=0)

    # === RELATIONS ===
    user = db.relationship('User', foreign_keys=[employe_id], backref='dossiers')
    succursale = db.relationship('Succursale', backref='dossiers')
    agent = db.relationship('User', foreign_keys=[agent_id], backref='dossiers_assignes')

    # === DOCUMENTS LIÉS ===
    documents = db.relationship('Document', secondary=dossier_documents, backref='dossiers')

    client_id = db.Column(
        db.Integer,
        db.ForeignKey('clients.id'),
        nullable=True
    )

    def __repr__(self):
        return f'<Dossier {self.reference}: {self.nom}>'

    @property
    def couleur_priorite(self):
        """Couleur Bootstrap selon la priorité"""
        couleurs = {
            'basse': 'success',
            'normale': 'info',
            'haute': 'warning',
            'urgente': 'danger'
        }
        return couleurs.get(self.priorite, 'secondary')

    @property
    def icone_type(self):
        """Icône Font Awesome selon le type"""
        icones = {
            'client': 'fa-user',
            'employe': 'fa-user-tie',
            'pret': 'fa-hand-holding-usd',
            'document': 'fa-file-alt'
        }
        return icones.get(self.type, 'fa-folder')

    @property
    def statut_couleur(self):
        """Couleur Bootstrap selon le statut"""
        couleurs = {
            'actif': 'success',
            'archive': 'secondary',
            'en_attente': 'warning',
            'cloture': 'dark'
        }
        return couleurs.get(self.statut, 'light')

    @classmethod
    def generer_reference(cls, type_dossier):
        """Génère une référence unique pour le dossier"""
        prefix = type_dossier[:3].upper()
        annee = datetime.now().year
        mois = datetime.now().month
        count = cls.query.filter(
            cls.reference.like(f"{prefix}-{annee}{mois:02d}%")
        ).count() + 1
        return f"{prefix}-{annee}{mois:02d}-{count:04d}"

    @classmethod
    def get_by_succursale(cls, succursale_id, statut=None):
        """Récupère les dossiers d'une succursale"""
        query = cls.query.filter_by(succursale_id=succursale_id)
        if statut:
            query = query.filter_by(statut=statut)
        return query.order_by(cls.date_creation.desc()).all()

    @classmethod
    def get_by_user(cls, employe_id):
        """Récupère les dossiers d'un utilisateur"""
        return cls.query.filter_by(employe_id=employe_id).order_by(cls.date_creation.desc()).all()

    @classmethod
    def get_en_attente(cls, succursale_id=None):
        """Récupère les dossiers en attente"""
        query = cls.query.filter_by(statut='en_attente')
        if succursale_id:
            query = query.filter_by(succursale_id=succursale_id)
        return query.order_by(cls.date_creation).all()

    def ajouter_document(self, document):
        """Ajoute un document au dossier"""
        if document not in self.documents:
            self.documents.append(document)
            self.nb_documents += 1
            db.session.commit()

    def retirer_document(self, document):
        """Retire un document du dossier"""
        if document in self.documents:
            self.documents.remove(document)
            self.nb_documents = max(0, self.nb_documents - 1)
            db.session.commit()

    def cloturer(self):
        """Clôture le dossier"""
        self.statut = 'cloture'
        self.date_cloture = datetime.utcnow()
        db.session.commit()

    def archiver(self):
        """Archive le dossier"""
        self.statut = 'archive'
        db.session.commit()



class Decision(db.Model):
    __tablename__ = 'decisions'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type_decision = db.Column(db.String(50), nullable=False)  # 'strategique', 'operationnelle', 'financiere', 'rh'

    # Dates
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_echeance = db.Column(db.DateTime, nullable=True)
    date_execution = db.Column(db.DateTime, nullable=True)

    # Statut
    statut = db.Column(db.String(20), default='en_attente')  # 'en_attente', 'en_cours', 'realisee', 'annulee'
    priorite = db.Column(db.String(20), default='moyenne')  # 'haute', 'moyenne', 'basse'

    # Progression
    progression = db.Column(db.Integer, default=0)  # 0-100%

    # Responsables
    cree_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    responsable_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Succursale concernée (optionnel)
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=True)

    # Relations
    createur = db.relationship('User', foreign_keys=[cree_par_id], backref='decisions_crees')
    responsable = db.relationship('User', foreign_keys=[responsable_id], backref='decisions_responsables')
    succursale = db.relationship('Succursale', backref='decisions')

    def __repr__(self):
        return f'<Decision {self.id}: {self.titre}>'


class ActionDecision(db.Model):
    __tablename__ = 'actions_decisions'

    id = db.Column(db.Integer, primary_key=True)
    decision_id = db.Column(db.Integer, db.ForeignKey('decisions.id'), nullable=False)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    # Dates
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_echeance = db.Column(db.DateTime, nullable=True)
    date_realisation = db.Column(db.DateTime, nullable=True)

    # Statut
    statut = db.Column(db.String(20), default='a_faire')  # 'a_faire', 'en_cours', 'terminee'

    # Responsable
    responsable_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relations
    decision = db.relationship('Decision', backref='actions')
    responsable = db.relationship('User', foreign_keys=[responsable_id])


class CommentaireDecision(db.Model):
    __tablename__ = 'commentaires_decisions'

    id = db.Column(db.Integer, primary_key=True)
    decision_id = db.Column(db.Integer, db.ForeignKey('decisions.id'), nullable=False)
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    decision = db.relationship('Decision', backref='commentaires')
    user = db.relationship('User', backref='commentaires_decisions')

class Badge(db.Model):
    __tablename__ = 'badges'
    id = db.Column(db.Integer, primary_key=True)
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    nom = db.Column(db.String(100))
    icone = db.Column(db.String(50))
    description = db.Column(db.String(200))
    obtenu = db.Column(db.Boolean, default=False)
    date_obtention = db.Column(db.DateTime)

class Defi(db.Model):
    __tablename__ = 'defis'
    id = db.Column(db.Integer, primary_key=True)
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    nom = db.Column(db.String(100))
    description = db.Column(db.String(200))
    recompense = db.Column(db.Integer, default=0)
    termine = db.Column(db.Boolean, default=False)
    progression = db.Column(db.String(50))
    date_completion = db.Column(db.DateTime)

class RecompenseEchange(db.Model):
    __tablename__ = 'recompenses_echanges'
    id = db.Column(db.Integer, primary_key=True)
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recompense_id = db.Column(db.Integer)
    points_depenses = db.Column(db.Integer)
    date_echange = db.Column(db.DateTime)
    statut = db.Column(db.String(50))

class Entreprise(db.Model):
    __tablename__ = "entreprises"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String)
    plan = db.Column(db.String)  # SaaS (basic, pro, enterprise)


class Tracking(db.Model):
    __tablename__ = "tracking"

    id = db.Column(db.Integer, primary_key=True)
    employe_id = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)

class QuestionSecrete(db.Model):
    __tablename__ = 'questions_secetes'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    question = db.Column(db.String(255), nullable=False)
    reponse = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relation utilisateur (celui qui pose la question)
    user = db.relationship(
        "User",
        foreign_keys=[user_id],
        backref="questions_posees"
    )

    # Relation employé (celui concerné / assigné)
    employe = db.relationship(
        "User",
        foreign_keys=[employe_id],
        backref=db.backref("questions_secretes", cascade="all, delete-orphan")
    )

class ProjetSocial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200))
    description = db.Column(db.Text)
    objectif = db.Column(db.Float)
    collecte = db.Column(db.Float, default=0)
    statut = db.Column(db.String(20), default='en_cours')
    image = db.Column(db.String(100))
    date_debut = db.Column(db.DateTime, default=datetime.utcnow)

class Famille(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    statut = db.Column(db.String(20), default='aidee')

class Emploi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100))
    statut = db.Column(db.String(20), default='actif')



class Echeancier(db.Model):
    """Payment schedule for loans"""
    __tablename__ = 'echeanciers'

    id = db.Column(db.Integer, primary_key=True)
    pret_id = db.Column(db.Integer, db.ForeignKey('prets.id', ondelete='CASCADE'), nullable=False)
    numero_echeance = db.Column(db.Integer, nullable=False)  # Payment number (1, 2, 3, ...)
    date_echeance = db.Column(db.Date, nullable=False)  # Due date
    montant = db.Column(db.Float, nullable=False)  # Amount due
    montant_paye = db.Column(db.Float, default=0.0)  # Amount paid
    statut = db.Column(db.String(20), default='en_attente')  # en_attente, paye, impaye, partiel
    date_paiement = db.Column(db.DateTime)  # When payment was made
    penalite = db.Column(db.Float, default=0.0)  # Late payment penalty
    jours_retard = db.Column(db.Integer, default=0)  # Days overdue
    reference_paiement = db.Column(db.String(100))  # Payment reference number
    notes = db.Column(db.Text)  # Additional notes

    # Relationships
    pret = db.relationship('Pret', backref=db.backref('echeanciers', lazy='dynamic', cascade='all, delete-orphan'))

    def __init__(self, pret_id, numero_echeance, date_echeance, montant):
        self.pret_id = pret_id
        self.numero_echeance = numero_echeance
        self.date_echeance = date_echeance
        self.montant = montant
        self.montant_paye = 0.0
        self.statut = 'en_attente'
        self.penalite = 0.0
        self.jours_retard = 0

    def calculate_penalty(self, current_date=None):
        """Calculate late payment penalty"""
        if current_date is None:
            current_date = date.today()

        if self.statut != 'paye' and self.date_echeance < current_date:
            days_late = (current_date - self.date_echeance).days
            self.jours_retard = days_late

            # Example: 1% penalty per month (0.033% per day)
            daily_rate = 0.00033
            penalty_rate = min(daily_rate * days_late, 0.10)  # Max 10% penalty
            self.penalite = round(self.montant * penalty_rate, 2)
            return self.penalite
        return 0

    def make_payment(self, amount, reference=None):
        """Process a payment for this installment"""
        remaining = self.montant - self.montant_paye

        if amount >= remaining:
            # Full payment
            self.montant_paye = self.montant
            self.statut = 'paye'
            self.date_paiement = datetime.now()
            self.penalite = 0
            self.jours_retard = 0
            overpayment = amount - remaining
            return {'success': True, 'overpayment': overpayment, 'message': 'Paiement complet effectué'}

        else:
            # Partial payment
            self.montant_paye += amount
            self.statut = 'partiel'
            self.date_paiement = datetime.now()
            return {'success': True, 'remaining': remaining - amount, 'message': 'Paiement partiel enregistré'}

    def to_dict(self):
        """Convert to dictionary for JSON responses"""
        return {
            'id': self.id,
            'numero': self.numero_echeance,
            'date_echeance': self.date_echeance.strftime('%d/%m/%Y'),
            'montant': self.montant,
            'montant_paye': self.montant_paye,
            'statut': self.statut,
            'date_paiement': self.date_paiement.strftime('%d/%m/%Y %H:%M') if self.date_paiement else None,
            'penalite': self.penalite,
            'jours_retard': self.jours_retard,
            'reference_paiement': self.reference_paiement
        }

    def __repr__(self):
        return f'<Echeancier {self.pret_id} - #{self.numero_echeance}>'


class DocumentPret(db.Model):
    """Documents attached to loan applications"""
    __tablename__ = 'documents_prets'

    id = db.Column(db.Integer, primary_key=True)
    pret_id = db.Column(db.Integer, db.ForeignKey('prets.id', ondelete='CASCADE'), nullable=False)
    titre = db.Column(db.String(200), nullable=False)  # Document title
    filename = db.Column(db.String(255), nullable=False)  # Original filename
    filepath = db.Column(db.String(500), nullable=False)  # Stored file path
    file_size = db.Column(db.Integer)  # Size in bytes
    file_type = db.Column(db.String(50))  # MIME type
    type_document = db.Column(db.String(50))  # CIN, contrat, justificatif, etc.
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # User who uploaded
    date_upload = db.Column(db.DateTime, default=datetime.now)
    description = db.Column(db.Text)  # Optional description
    version = db.Column(db.Integer, default=1)  # Document version

    # Relationships
    pret = db.relationship('Pret', backref=db.backref('documents', lazy='dynamic', cascade='all, delete-orphan'))
    uploader = db.relationship('User', backref='uploaded_documents')

    ALLOWED_TYPES = ['CIN', 'contrat', 'justificatif_revenu', 'justificatif_domicile', 'photo', 'autre']
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'xls', 'xlsx'}

    def __init__(self, pret_id, filename, filepath, uploaded_by, titre=None, type_document='autre'):
        self.pret_id = pret_id
        self.filename = filename
        self.filepath = filepath
        self.uploaded_by = uploaded_by
        self.titre = titre or filename
        self.type_document = type_document if type_document in self.ALLOWED_TYPES else 'autre'

    def get_file_icon(self):
        """Return Font Awesome icon based on file type"""
        ext = self.filename.rsplit('.', 1)[1].lower() if '.' in self.filename else ''
        icons = {
            'pdf': 'fa-file-pdf',
            'jpg': 'fa-file-image',
            'jpeg': 'fa-file-image',
            'png': 'fa-file-image',
            'doc': 'fa-file-word',
            'docx': 'fa-file-word',
            'xls': 'fa-file-excel',
            'xlsx': 'fa-file-excel'
        }
        return icons.get(ext, 'fa-file-alt')

    def get_type_badge(self):
        """Return badge class for document type"""
        badges = {
            'CIN': 'primary',
            'contrat': 'success',
            'justificatif_revenu': 'info',
            'justificatif_domicile': 'warning',
            'photo': 'secondary',
            'autre': 'secondary'
        }
        return badges.get(self.type_document, 'secondary')

    def to_dict(self):
        """Convert to dictionary for JSON responses"""
        return {
            'id': self.id,
            'titre': self.titre,
            'filename': self.filename,
            'type_document': self.type_document,
            'file_size': self.file_size,
            'date_upload': self.date_upload.strftime('%d/%m/%Y %H:%M'),
            'uploaded_by_name': self.uploader.nom if self.uploader else 'Inconnu',
            'icon': self.get_file_icon(),
            'badge_class': self.get_type_badge()
        }

    def __repr__(self):
        return f'<DocumentPret {self.pret_id} - {self.filename}>'


# models.py - Ajoutez cette classe

class Depense(db.Model):
    """Modèle pour gérer les dépenses de l'institution"""
    __tablename__ = 'depenses'

    id = db.Column(db.Integer, primary_key=True)


    numero_depense = db.Column(db.String(50), unique=True, nullable=False)
    libelle = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    montant = db.Column(db.Numeric(15, 2), nullable=False)
    date_depense = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    categorie = db.Column(db.String(50),
                          nullable=False)  # salaire, electricite, eau, internet, fourniture, entretien, imprevu, etc.
    mode_paiement = db.Column(db.String(50), default='especes')  # especes, cheque, virement, carte
    reference = db.Column(db.String(100))  # Numéro de chèque, référence virement
    piece_jointe = db.Column(db.String(255))  # Chemin du fichier (facture, reçu)

    # Fournisseur / Bénéficiaire
    fournisseur = db.Column(db.String(200))

    # Approbation
    statut = db.Column(db.String(20), default='en_attente')  # en_attente, approuve, rejete, annule

    date_approbation = db.Column(db.DateTime)
    motif_rejet = db.Column(db.String(255))
    # ✅ CLÉ ÉTRANGÈRE
    approbateur_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )

    approbateur = db.relationship(
        'User',
        foreign_keys=[approbateur_id],
        backref='depenses_approuvees'
    )

    # Liens
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=False)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'))  # Si vous avez un module budget

    # Relations
    employe = db.relationship('User', foreign_keys=[employe_id])

    succursale = db.relationship('Succursale')
    budget = db.relationship('Budget')

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        if 'numero_depense' not in kwargs:
            # Générer un numéro unique: DEP-2024-00001
            annee = datetime.now().year
            dernier = Depense.query.filter(
                Depense.numero_depense.like(f'DEP-{annee}-%')
            ).order_by(Depense.id.desc()).first()

            if dernier:
                num = int(dernier.numero_depense.split('-')[-1]) + 1
            else:
                num = 1
            kwargs['numero_depense'] = f'DEP-{annee}-{num:05d}'

        super().__init__(**kwargs)

    @property
    def montant_htg(self):
        """Retourne le montant formaté"""
        return f"{self.montant:,.0f} HTG"

    @property
    def est_approuvee(self):
        return self.statut == 'approuve'

    @property
    def est_en_attente(self):
        return self.statut == 'en_attente'

    def approuver(self, utilisateur_id, commentaire=None):
        """Approuver la dépense"""
        self.statut = 'approuve'
        self.approuve_par = utilisateur_id
        self.date_approbation = datetime.utcnow()
        if commentaire:
            self.description += f"\n\nApprobation: {commentaire}"
        db.session.commit()

    def rejeter(self, utilisateur_id, motif):
        """Rejeter la dépense"""
        self.statut = 'rejete'
        self.approuve_par = utilisateur_id
        self.date_approbation = datetime.utcnow()
        self.motif_rejet = motif
        db.session.commit()

    def annuler(self):
        """Annuler la dépense"""
        self.statut = 'annule'
        db.session.commit()

    def __repr__(self):
        return f"<Depense {self.numero_depense}: {self.libelle} - {self.montant} HTG>"
class Budget(db.Model):
    __tablename__ = 'budgets'

    id = db.Column(db.Integer, primary_key=True)
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    mois = db.Column(db.Integer, nullable=False)  # 1-12
    categorie = db.Column(db.String(100))  # 'fonctionnement', 'investissement', 'salaires', etc.
    montant_prevu = db.Column(db.Float, default=0)
    montant_depense = db.Column(db.Float, default=0)
    ecart = db.Column(db.Float, default=0)  # montant_prevu - montant_depense
    pourcentage_utilisation = db.Column(db.Float, default=0)
    statut = db.Column(db.String(20), default='actif')  # actif, clos, annule
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relations
    succursale = db.relationship('Succursale', backref='budgets')
    createur = db.relationship('User', backref='budgets')

    def __repr__(self):
        return f'<Budget {self.succursale.nom} {self.mois}/{self.annee} - {self.categorie}>'

    @property
    def taux_utilisation(self):
        if self.montant_prevu > 0:
            return (self.montant_depense / self.montant_prevu) * 100
        return 0



class CompteCaisse(db.Model):
    __tablename__ = 'comptes_caisse'

    id = db.Column(db.Integer, primary_key=True)
    compte_caisse_id = db.Column(db.Integer,db.ForeignKey('comptes_caisse.id'))
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    solde = db.Column(db.Float, default=0)
    solde_ouverture = db.Column(db.Float, default=0)
    date_ouverture = db.Column(db.DateTime, default=datetime.utcnow)
    date_derniere_fermeture = db.Column(db.DateTime, nullable=True)
    statut = db.Column(db.String(20), default='actif')  # actif, ferme, suspendu
    plafond_max = db.Column(db.Float, default=10000000)
    plafond_min = db.Column(db.Float, default=-1000000)  # découvert autorisé
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relations
    succursale = db.relationship('Succursale', backref='comptes_caisse')
    transactions = db.relationship('TransactionCaisse', backref='compte', lazy='dynamic')

    def __repr__(self):
        return f'<CompteCaisse {self.code}: {self.solde}>'


class PaiementPret(db.Model):
    __tablename__ = 'paiements_pret'

    id = db.Column(db.Integer, primary_key=True)
    pret_id = db.Column(db.Integer, db.ForeignKey('prets.id'), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    interets = db.Column(db.Float, default=0)
    penalites = db.Column(db.Float, default=0)
    date_paiement = db.Column(db.DateTime, default=datetime.utcnow)
    mode_paiement = db.Column(db.String(50), default='especes')  # especes, cheque, virement
    reference = db.Column(db.String(100), nullable=True)
    statut = db.Column(db.String(20), default='valide')  # valide, annule
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    pret = db.relationship('Pret', backref='paiements')

    def __repr__(self):
        return f'<PaiementPret {self.id}: {self.montant}>'


class RetardPaiement(db.Model):
    __tablename__ = "retards_paiement"

    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(
        db.Integer,
        db.ForeignKey('clients.id'),
        nullable=False
    )

    pret_id = db.Column(
        db.Integer,
        db.ForeignKey('prets.id'),
        nullable=False
    )

    echeance_prevue = db.Column(db.Date, nullable=False)

    date_paiement = db.Column(db.Date)

    jours_retard = db.Column(db.Integer, default=0)

    montant_retard = db.Column(db.Float, default=0)

    penalite = db.Column(db.Float, default=0)

    statut = db.Column(
        db.String(20),
        default="impaye"
    )  # impaye, regle, partiel

    date_creation = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    client = db.relationship(
        'Client',
        backref='retards'
    )

    pret = db.relationship(
        'Pret',
        backref='retards'
    )

    def __repr__(self):
        return f"<RetardPaiement {self.id} - {self.jours_retard} jours>"


# models.py - Ajoute ces classes à la fin du fichier

class Partner(db.Model):
    __tablename__ = "partner"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)

    description = db.Column(db.Text)

    contact_name = db.Column(db.String(200))
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))

    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)

    monthly_limit = db.Column(db.Float, default=1000000)
    per_transaction_limit = db.Column(db.Float, default=100000)
    daily_limit = db.Column(db.Float, default=500000)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relations
    api_keys = db.relationship("PartnerAPIKey", back_populates="partner")
    webhooks = db.relationship("PartnerWebhook", back_populates="partner")
    integrations = db.relationship("PartnerIntegration", back_populates="partner")


class PartnerIntegration(db.Model):
    __tablename__ = "partner_integrations"

    id = db.Column(db.Integer, primary_key=True)

    partner_id = db.Column(db.Integer, db.ForeignKey("partner.id"), nullable=False)
    api_key_id = db.Column(db.Integer, db.ForeignKey("partner_api_keys.id"), nullable=False)

    name = db.Column(db.String(200), nullable=False)

    webhook_url = db.Column(db.String(500))
    events = db.Column(db.JSON, default=['payment'])

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relations propres
    partner = db.relationship("Partner", back_populates="integrations")
    api_key = db.relationship("PartnerAPIKey")


class PartnerWebhook(db.Model):
    """Webhooks pour les partenaires"""
    __tablename__ = "partner_webhooks"

    id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey("partner.id"))

    url = db.Column(db.String(500), nullable=False)
    secret = db.Column(db.String(255))
    events = db.Column(db.JSON, default=['payment.created', 'payment.completed'])

    is_active = db.Column(db.Boolean, default=True)
    failed_attempts = db.Column(db.Integer, default=0)
    last_triggered_at = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relation - UNIQUEMENT back_populates
    partner = db.relationship("Partner", back_populates="webhooks")

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'events': self.events,
            'is_active': self.is_active,
            'failed_attempts': self.failed_attempts,
            'last_triggered_at': self.last_triggered_at.isoformat() if self.last_triggered_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class PartnerAPIKey(db.Model):
    """Clés API pour les partenaires"""
    __tablename__ = "partner_api_keys"

    id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey("partner.id"))

    client_id = db.Column(db.String(100), unique=True, nullable=False)
    client_secret = db.Column(db.String(255), nullable=False)
    secret_plain = db.Column(db.String(255))

    permissions = db.Column(db.JSON, default={
        'can_create_payment': True,
        'can_refund': False,
        'can_check_balance': True,
        'can_webhook': True
    })

    is_active = db.Column(db.Boolean, default=True)
    expires_at = db.Column(db.DateTime)
    last_used_at = db.Column(db.DateTime)
    requests_count = db.Column(db.Integer, default=0)
    daily_requests = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relation - UNIQUEMENT back_populates
    partner = db.relationship("Partner", back_populates="api_keys")


class Satisfaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    note = db.Column(db.Integer)







