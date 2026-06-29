import os  # ← AJOUTEZ CETTE LIGNE
import pickle
from datetime import datetime, date
from database import db

import requests
import flet as ft  # Assurez-vous d'avoir importé votre bibliothèque d'interface
# from deepface import DeepFace
from werkzeug.security import generate_password_hash, check_password_hash


from database import db
import sqlite3
from flask_login import UserMixin  # ← AJOUTEZ CETTE LIGNE

import random
import string

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DecimalField, DateField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Optional

user_permissions = db.Table('user_permissions',
                            db.Column('employe_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                            db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'),
                                      primary_key=True)
                            )
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # Champs communs à tous les utilisateurs
    username = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(20), default='client')  # client, employe, admin, superviseur
    statut = db.Column(db.String(20), default='actif')  # 'actif', 'en_attente', 'inactif'

    # approuve_par = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Admin qui a approuvé

    # permissions = db.Column(db.Text)  # Stocke les permissions en JSON
    nom_complet=db.Column(db.String(100))
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    groupe_id = db.Column(db.Integer, db.ForeignKey('groupes.id'), nullable=True)

    # Champs spécifiques aux clients
    id_client = db.Column(db.String(20), unique=True, nullable=True)
    adresse = db.Column(db.Text)
    cin_nif = db.Column(db.String(50), unique=True, nullable=True)
    date_naissance = db.Column(db.DateTime, nullable=True)
    profession = db.Column(db.String(100))
    lieu_naissance = db.Column(db.String(100))
    nationalite = db.Column(db.String(100))
    autre_nationalite = db.Column(db.String(100))
    commune = db.Column(db.String(100))
    duree_adresse = db.Column(db.Integer)
    etat_civil = db.Column(db.String(100))
    nom_conjoint = db.Column(db.String(100))
    nb_enfants = db.Column(db.Integer)

    revenu_mensuel = db.Column(db.Float, default=0)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)

    # ⚠️ AJOUTEZ CES CHAMPS MANQUANTS :
    niveau_habilitation = db.Column(db.Integer, default=1)  # Niveau 1-4
    derniere_activite = db.Column(db.DateTime, default=datetime.utcnow)
    verifications_completes = db.Column(db.Boolean, default=False)
    formation_aml_cft = db.Column(db.Boolean, default=False)
    matricule = db.Column(db.String(20), unique=True, default=lambda: "EMP-" + ''.join(random.choices("0123456789", k=6)))  # Matricule d'employé

    # Nouveaux champs
    depenses_mensuelles = db.Column(db.Float, default=0)
    capacite_remboursement = db.Column(db.Float, default=0)
    photo_id = db.Column(db.String(255))
    photo_selfie = db.Column(db.String(255))
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
    motif_depart = db.Column(db.String(100), nullable=True)
    fonction = db.Column(db.String(100), nullable=True)  # si vous avez ajouté ce champ

    # Dans models.py, classe User
    cree_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    token_signature = db.Column(db.String(100), unique=True, nullable=True)
    date_envoi_terms = db.Column(db.DateTime, nullable=True)
    date_signature = db.Column(db.DateTime, nullable=True)
    sexe = db.Column(db.String(1), nullable=True)  # 'M' ou 'F'

    parent_nom = db.Column(db.String(100), nullable=True)
    parent_signature = db.Column(db.Text, nullable=True)
    date_expiration_token = db.Column(db.DateTime, nullable=True)
    date_signature_terms = db.Column(db.DateTime, nullable=True)

    date_approbation = db.Column(db.DateTime, nullable=True)
    approuve_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    motif_rejet = db.Column(db.Text, nullable=True)
    date_rejet = db.Column(db.DateTime, nullable=True)
    rejete_par_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    derniere_connexion = db.Column(db.DateTime, nullable=True)

    photo_profil = db.Column(db.String(255))
    photo_recto = db.Column(db.String(255))
    photo_verso = db.Column(db.String(255))

    id_number = db.Column(db.String(100), unique=True)
    id_type = db.Column(db.String(50))

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

    carte_numero = db.Column(db.String(50), unique=True, nullable=True)
    est_actif = db.Column(db.Boolean, default=True)

    # Relation avec Partner


    # Ajoute cette ligne pour la relation avec Partner



    # # ➕ AJOUTEZ CETTE RELATION (vers ligne ~600)
    # permissions = db.relationship(
    #     "Permission",
    #     secondary=user_permissions,
    #     back_populates="users",
    #     lazy="select"
    # )

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
    id_client = db.Column(db.String(20), unique=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    nom_complet = db.Column(db.String(100))
    sexe = db.Column(db.String(10), nullable=True)
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    adresse = db.Column(db.Text)
    cin = db.Column(db.String(50))
    date_naissance = db.Column(db.DateTime)
    profession = db.Column(db.String(100))
    revenu_mensuel = db.Column(db.Float)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)

    statut = db.Column(db.String(20), default='actif')
    mot_de_passe_hash = db.Column(db.String(255))
    groupe_id = db.Column(db.Integer)
    terms_accepted = db.Column(db.Boolean, default=False)
    terms_accepted_at = db.Column(db.DateTime, nullable=True)
    compte_actif = db.Column(db.Boolean, default=True)

    user = db.relationship('User', backref='client_profile', foreign_keys=[employe_id])

    terms_signature_ip = db.Column(db.String(45))
    terms_signature_user_agent = db.Column(db.Text)
    terms_signature_hash = db.Column(db.String(256))

    # ------------------- Champs pour vérification faciale annuelle -------------------
    selfie_reference = db.Column(db.String(255))  # Selfie principal de référence
    photo_face_left = db.Column(db.String(255))  # Face côté gauche
    photo_face_right = db.Column(db.String(255))  # Face côté droit
    photo_id_verified = db.Column(db.Boolean, default=False)  # ID vérifié
    photo_id= db.Column(db.Boolean, default=False)  # ID vérifié
    photo_face = db.Column(db.String(255), nullable=True)  # Photo recto
    photo_dos = db.Column(db.String(255), nullable=True)  # Photo verso
    photo_selfie = db.Column(db.String(255), nullable=True)
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
    lieu_naissance = db.Column(db.String(100), nullable=True)
    nationalite = db.Column(db.String(50), default='Haïtienne')
    autre_nationalite = db.Column(db.String(50), nullable=True)
    cin_nif = db.Column(db.String(50), unique=True, nullable=True)  # Alternative à cin

    # Adresse détaillée
    commune = db.Column(db.String(100), nullable=True)
    departement = db.Column(db.String(50), nullable=True)
    duree_adresse = db.Column(db.Integer, nullable=True)  # en années

    # Situation familiale
    etat_civil = db.Column(db.String(20), nullable=True)  # celibataire, marie, union_libre, divorce
    nom_conjoint = db.Column(db.String(100), nullable=True)
    nb_enfants = db.Column(db.Integer, default=0)

    # Informations professionnelles
    entreprise = db.Column(db.String(100), nullable=True)
    adresse_travail = db.Column(db.String(200), nullable=True)
    tel_travail = db.Column(db.String(20), nullable=True)
    autres_revenus = db.Column(db.Text, nullable=True)

    # Informations financières
    depenses_mensuelles = db.Column(db.Float, default=0)
    capacite_remboursement = db.Column(db.Float, default=0)

    # Gestion des tokens
    token_signature = db.Column(db.String(256), nullable=True)
    date_expiration_token = db.Column(db.DateTime, nullable=True)

    # ✅ Ajoute ces champs si nécessaire
    verification_faciale = db.Column(db.Boolean, default=False)
    score_verification = db.Column(db.Float, default=0)
    date_envoi_terms = db.Column(db.DateTime, nullable=True)
    solde = db.Column(db.Float, default=0.0)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    numero_compte = db.Column(db.String(50), unique=True)
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
    statut = db.Column(db.String(20), default='en_attente')
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
    signature = db.Column(db.String(255), nullable=True)

    numero_dossier = db.Column(db.VARCHAR(250), unique=True)

    derniere_activite = db.Column(db.DateTime, nullable=True)

    # ===== AJOUTEZ CES COLONNES =====
    date_reception = db.Column(db.DateTime, nullable=True)
    date_debut = db.Column(db.DateTime, nullable=True)
    date_creation = db.Column(db.DateTime, nullable=True)
    decision = db.Column(db.String(50), nullable=True)  # approuve, refuse, en_attente
    montant_demande = db.Column(db.Float, nullable=True)
    montant_accorde = db.Column(db.Float, nullable=True)
    signature_responsable = db.Column(db.String(255), nullable=True)
    motif_refus = db.Column(db.Text, nullable=True)
    numero_pret = db.Column(db.VARCHAR(50), unique=True)  # ou db.VARCHAR(50)
    date_echeance = db.Column(db.DateTime)  # ← Ajouter cette ligne
    date_decaissement = db.Column(db.DateTime, nullable=True)  # ← ADD THIS LINE


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
    statut = db.Column(db.String(20), default='en_attente')
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
    statut = db.Column(db.String(20), default='en_attente')  # ← Modifier 'actif' en 'en_attente'
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
    statut = db.Column(db.String(20), default='en_attente')  # en_attente, paye, echoue
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_confirmation = db.Column(db.DateTime)
    metadata_info = db.Column(db.Text)  # Données supplémentaires au format JSON
    date = db.Column(db.DateTime)
    succursale_id = db.Column(db.Integer, db.ForeignKey('succursale.id'))


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
    statut = db.Column(db.String(20), default='en_attente')

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
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ← AJOUT foreign key
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
    formateur = db.Column(db.String(100), nullable=True)

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

    # Relations
    participants = db.relationship('FormationParticipant', backref='formation', lazy='dynamic')

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
    statut = db.Column(db.String(20), default='en_attente')  # 'en_attente', 'payee', 'retard', 'impayee', 'renégociée'

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
    statut = db.Column(db.String(20), default='en_attente')  # 'en_attente', 'approuvee', 'rejetee', 'en_cours'

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
    statut = db.Column(db.String(20), default='en_attente')  # 'en_attente', 'appele', 'en_cours', 'termine', 'annule'

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
        self.agent_id = agent_id
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
    statut = db.Column(db.String(20), default='en_attente')  # 'en_attente', 'approuve', 'refuse', 'annule'

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




class AlerteConformite(db.Model):
    __tablename__ = "alertes_conformite"

    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=True)
    pret_id = db.Column(db.Integer, db.ForeignKey("prets.id"), nullable=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey("transactions.id"), nullable=True)

    type_alerte = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    niveau_risque = db.Column(db.String(50), default="moyen")
    statut = db.Column(db.String(50), default="non_traitee")

    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    traite_par = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    date_traitement = db.Column(db.DateTime, nullable=True)

    # Relations (optionnel mais recommandé)
    client = db.relationship("Client", backref="alertes")
    pret = db.relationship("Pret", backref="alertes")
    transaction = db.relationship("Transaction", backref="alertes")


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
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_acceptation = db.Column(db.DateTime, nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)

    client = db.relationship('User', backref='terms_acceptances')

class Competence(db.Model):
    __tablename__ = 'competences'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    employe_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=True)  # ← Changé à True (permet NULL)
    nom = db.Column(db.String(100), nullable=False)
    niveau = db.Column(db.String(50))  # débutant, intermédiaire, expert
    description = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.now)

    # Spécifier explicitement quelle clé étrangère utiliser
    client = db.relationship('User', foreign_keys=[client_id], backref='competences_client')
    user = db.relationship('User', foreign_keys=[employe_id], backref='competences_user')


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



# Modèle pour les erreurs
class ErrorLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    traceback = db.Column(db.Text)
    url = db.Column(db.String(500))
    employe_id = db.Column(db.Integer)
    succursale_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    seen = db.Column(db.Boolean, default=False)
    level = db.Column(db.String(20), default='error')


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
    documents = db.relationship('Document', secondary='dossier_documents', backref='dossiers')

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


# Table d'association pour la relation many-to-many entre Dossier et Document
dossier_documents = db.Table('dossier_documents',
                             db.Column('dossier_id', db.Integer, db.ForeignKey('dossiers.id'), primary_key=True),
                             db.Column('document_id', db.Integer, db.ForeignKey('documents.id'), primary_key=True),
                             db.Column('date_ajout', db.DateTime, default=datetime.utcnow)
                             )

class Account:
    pass


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







