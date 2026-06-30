# AJOUTEZ CE BLOC AU TRÈS DÉBUT du fichier ai_scoring.py
import warnings

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from datetime import datetime

import random
import json

warnings.filterwarnings("ignore")

import sys

# Vérifier si scikit-learn est disponible
try:
    # Essayer d'importer scipy d'abord pour vérifier
    import scipy
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler

    SCIKIT_AVAILABLE = True
    print("✅ scikit-learn disponible")
except ImportError as e:
    print(f"⚠️ scikit-learn/scipy non disponible: {e}")
    print("⚠️ Utilisation du mode mock pour l'IA")
    SCIKIT_AVAILABLE = False


    # Créer des classes mock
    class RandomForestClassifier:
        def __init__(self, n_estimators=100, random_state=42):
            self.n_estimators = n_estimators
            self.random_state = random_state
            self.is_fitted = False

        def fit(self, X, y):
            print("⚠️ Mock RandomForest - simulation d'entraînement")
            self.is_fitted = True
            return self

        def predict_proba(self, X):
            # Retourne des probabilités mock
            import numpy as np
            if not hasattr(self, 'is_fitted') or not self.is_fitted:
                # Si non entraîné, retourne des valeurs par défaut
                if hasattr(X, '__len__'):
                    return np.array([[0.3, 0.7]] * len(X))
                return np.array([[0.3, 0.7]])

            # Simulation basée sur les features
            probs = []
            for features in X:
                if len(features) > 0 and features[0] > 20:  # Revenu élevé
                    probs.append([0.8, 0.2])  # 80% bon payeur
                else:
                    probs.append([0.4, 0.6])  # 40% bon payeur
            return np.array(probs)


class SimpleAIScorer:
    def calculate_user_score(self, user):
        score = 60
        if hasattr(user, 'date_creation'):
            days_old = (datetime.now() - user.date_creation).days
            if days_old > 365:
                score += 20
            elif days_old > 180:
                score += 10
            elif days_old > 30:
                score += 5
        if hasattr(user, 'role'):
            if user.role == 'admin':
                score += 30
            elif user.role == 'superviseur':
                score += 20
            elif user.role == 'employe':
                score += 10
        score += random.randint(-5, 10)
        return max(0, min(100, round(score, 1)))

    def calculate_loan_risk(self, client_data):
        risk_score = 50
        revenu = client_data.get('revenu_mensuel', 0)
        depenses = client_data.get('depenses_mensuelles', 0)
        if revenu > 0:
            ratio = depenses / revenu
            if ratio < 0.3:
                risk_score -= 20
            elif ratio < 0.6:
                risk_score -= 10
            elif ratio > 0.9:
                risk_score += 20
        risk_score += random.randint(-10, 10)
        return max(0, min(100, round(risk_score, 1)))


ai_scorer = SimpleAIScorer()

class AIScoringSystem:
    def __init__(self):
        self.model_path = "models/scoring_model.pkl"
        self.load_model()

    def load_model(self):
        """Charge ou initialise le modèle de scoring"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.is_trained = False

    def calculate_credit_score(self, client_data, pret_data, historique):
        """Calcule un score de crédit intelligent"""
        # Features pour le modèle
        features = self.extract_features(client_data, pret_data, historique)

        if self.is_trained:
            score = self.model.predict_proba([features])[0][1] * 1000
        else:
            # Score basique en attendant l'entraînement
            score = self.calculate_basic_score(client_data, historique)

        return min(850, max(300, score))

    def extract_features(self, client_data, pret_data, historique):
        """Extrait les features pour le modèle ML"""
        features = []

        # Données client
        features.append(client_data.get('revenu_mensuel', 0) / 1000)
        features.append(client_data.get('anciennete_client', 0))  # en mois
        features.append(1 if client_data.get('profession') in ['Commerçant', 'Entrepreneur'] else 0)

        # Données prêt
        features.append(pret_data.get('montant', 0) / 1000)
        features.append(pret_data.get('duree_mois', 0))
        montant_pret_ratio = pret_data.get('montant', 0) / max(client_data.get('revenu_mensuel', 1), 1)
        features.append(montant_pret_ratio)

        # Historique
        features.append(historique.get('nombre_prets', 0))
        features.append(historique.get('prets_rembourses', 0))
        features.append(historique.get('taux_remboursement', 0))
        features.append(historique.get('jours_retard_moyen', 0))
        features.append(historique.get('incidents_paiement', 0))

        return features

    def calculate_basic_score(self, client_data, historique):
        """Score basique en attendant l'IA"""
        score = 600  # Score de base

        # Ajustements selon le profil
        revenu = client_data.get('revenu_mensuel', 0)
        if revenu > 20000:
            score += 50
        elif revenu > 10000:
            score += 25

        # Historique de remboursement
        taux_remb = historique.get('taux_remboursement', 0)
        score += taux_remb * 2

        # Ancienneté
        anciennete = client_data.get('anciennete_client', 0)
        if anciennete > 24:  # 2 ans
            score += 30
        elif anciennete > 12:  # 1 an
            score += 15

        return score

    def train_model(self, training_data):
        """Entraîne le modèle avec des données historiques"""
        X = [self.extract_features(*data) for data in training_data]
        y = [data[2].get('defaut', 0) for data in training_data]  # 1 si défaut, 0 sinon

        self.model.fit(X, y)
        self.is_trained = True

        # Sauvegarder le modèle
        joblib.dump(self.model, self.model_path)

        return f"Modèle entraîné sur {len(X)} échantillons"

    def explain_score(self, client_data, pret_data, historique):
        """Explique les facteurs influençant le score"""
        factors = []

        revenu = client_data.get('revenu_mensuel', 0)
        if revenu < 5000:
            factors.append("Revenu mensuel faible")
        elif revenu > 20000:
            factors.append("Revenu mensuel élevé")

        taux_remb = historique.get('taux_remboursement', 0)
        if taux_remb > 95:
            factors.append("Excellent historique de remboursement")
        elif taux_remb < 80:
            factors.append("Historique de remboursement à améliorer")

        anciennete = client_data.get('anciennete_client', 0)
        if anciennete < 6:
            factors.append("Client récent")
        elif anciennete > 24:
            factors.append("Client fidèle")

        return factors


# Instance globale
ai_scorer = AIScoringSystem()