import flet as ft
import requests
import threading
import time


# ============================================================
# CONFIGURATION
# ============================================================

API_BASE_URL = "https://gmeshaiti-aeo3.onrender.com/auth"

REFRESH_INTERVAL_SECONDS = 10


# ============================================================
# APPLICATION MOBILE GMES
# ============================================================

class GMESMobileApp:

    def __init__(self):
        self.api_base_url = API_BASE_URL
        self.token = None
        self.current_user = None
        self.current_client = None
        self.page = None
        self.auto_refresh_active = False
        self.current_screen = None

    # ========================================================
    # INITIALISATION
    # ========================================================

    def main(self, page: ft.Page):

        self.page = page

        page.title = "GMES Microcrédit"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        page.scroll = ft.ScrollMode.ADAPTIVE
        page.bgcolor = "#F5F7FA"

        self.show_login_view()

    # ========================================================
    # OUTILS API
    # ========================================================

    def api_request(
        self,
        method,
        endpoint,
        data=None,
        authenticated=False
    ):

        url = f"{self.api_base_url}{endpoint}"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        if authenticated and self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        try:

            response = requests.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                timeout=20
            )

            try:
                result = response.json()

            except ValueError:

                result = {
                    "success": False,
                    "error": (
                        response.text
                        or "Réponse invalide du serveur"
                    )
                }

            if response.status_code == 401:

                self.token = None
                self.current_user = None
                self.current_client = None

            return response.status_code, result

        except requests.exceptions.Timeout:

            return 0, {
                "success": False,
                "error": (
                    "Le serveur met trop de temps à répondre."
                )
            }

        except requests.exceptions.ConnectionError:

            return 0, {
                "success": False,
                "error": (
                    "Impossible de contacter le serveur GMES."
                )
            }

        except Exception as e:

            return 0, {
                "success": False,
                "error": str(e)
            }

    # ========================================================
    # PAGE DE CONNEXION
    # ========================================================

    def show_login_view(self, e=None):

        self.stop_auto_refresh()
        self.current_screen = "login"

        self.email_field = ft.TextField(
            label="Email ou numéro de compte",
            prefix_icon=ft.Icons.EMAIL,
            width=320,
            autofocus=True
        )

        self.password_field = ft.TextField(
            label="Mot de passe",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK,
            width=320
        )

        login_button = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.LOGIN),
                    ft.Text("Se connecter")
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            width=320,
            height=48,
            on_click=self.login
        )

        register_button = ft.TextButton(
            content=ft.Text("Créer un compte"),
            on_click=self.show_register_view
        )

        content = ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        "GMES",
                        size=32,
                        weight=ft.FontWeight.BOLD
                    ),
                    alignment=ft.Alignment(0, 0)
                ),

                ft.Text(
                    "Microcrédit Solidaire",
                    size=18,
                    weight=ft.FontWeight.W_500
                ),

                ft.Text(
                    "GMES youn sipote lot",
                    size=14,
                    italic=True
                ),

                ft.Divider(),

                self.email_field,
                self.password_field,

                ft.Container(height=10),

                login_button,

                register_button
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12
        )

        self.page.clean()

        self.page.add(
            ft.Container(
                content=content,
                alignment=ft.Alignment(0, 0),
                padding=20
            )
        )

        self.page.update()

    # ========================================================
    # INSCRIPTION
    # ========================================================

    def show_register_view(self, e=None):

        self.nom_field = ft.TextField(
            label="Nom",
            width=320
        )

        self.prenom_field = ft.TextField(
            label="Prénom",
            width=320
        )

        self.telephone_field = ft.TextField(
            label="Téléphone",
            width=320
        )

        self.email_register_field = ft.TextField(
            label="Email",
            width=320
        )

        self.password_register_field = ft.TextField(
            label="Mot de passe",
            password=True,
            can_reveal_password=True,
            width=320
        )

        register_button = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.PERSON_ADD),
                    ft.Text("Créer mon compte")
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            width=320,
            height=48,
            on_click=self.handle_register
        )

        back_button = ft.TextButton(
            content=ft.Text("← Retour à la connexion"),
            on_click=self.show_login_view
        )

        content = ft.Column(
            [
                ft.Text(
                    "Créer un compte GMES",
                    size=25,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Remplissez vos informations"
                ),

                ft.Divider(),

                self.nom_field,
                self.prenom_field,
                self.telephone_field,
                self.email_register_field,
                self.password_register_field,

                ft.Container(height=10),

                register_button,

                back_button
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12
        )

        self.page.clean()

        self.page.add(
            ft.Container(
                content=content,
                padding=20,
                alignment=ft.Alignment(0, 0)
            )
        )

        self.page.update()

    # ========================================================
    # TRAITEMENT INSCRIPTION
    # ========================================================

    def handle_register(self, e):

        nom = self.nom_field.value.strip()
        prenom = self.prenom_field.value.strip()
        telephone = self.telephone_field.value.strip()
        email = self.email_register_field.value.strip()
        password = self.password_register_field.value

        if not all(
            [
                nom,
                prenom,
                telephone,
                email,
                password
            ]
        ):

            self.show_error(
                "Veuillez remplir tous les champs."
            )

            return

        status, data = self.api_request(
            "POST",
            "/api/mobile/register",
            {
                "first_name": prenom,
                "last_name": nom,
                "phone": telephone,
                "email": email,
                "password": password
            }
        )

        if status in (200, 201) and data.get(
            "success",
            True
        ):

            self.show_success(
                "Compte créé avec succès."
            )

            self.show_login_view()

        else:

            message = (
                data.get("error")
                or data.get("message")
                or "Erreur lors de la création du compte."
            )

            self.show_error(message)

    # ========================================================
    # CONNEXION
    # ========================================================

    def login(self, e):

        identifier = self.email_field.value.strip()
        password = self.password_field.value

        if not identifier or not password:

            self.show_error(
                "Veuillez saisir votre identifiant "
                "et votre mot de passe."
            )

            return

        status, data = self.api_request(
            "POST",
            "/api/mobile/login",
            {
                "identifier": identifier,
                "password": password,
                "user_type": "client"
            }
        )

        print("=== DEBUG LOGIN ===")
        print("STATUS:", status)
        print("DATA:", data)
        print("====================")

        if status == 200:

            token = (
                data.get("token")
                or data.get("access_token")
                or data.get("accessToken")
            )

            user = (
                data.get("user")
                or data.get("current_user")
                or {}
            )

            client = (
                data.get("client")
                or {}
            )

            if token:

                self.token = token

                self.current_user = user

                self.current_client = client

                self.show_success(
                    "Connexion réussie."
                )

                self.show_dashboard()

                return

        message = (
            data.get("error")
            or data.get("message")
            or "Identifiant ou mot de passe incorrect."
        )

        self.show_error(message)

    # ========================================================
    # RAFRAÎCHISSEMENT DES DONNÉES CLIENT
    # ========================================================

    def refresh_client_data(self):

        if not self.token:
            print("REFRESH: pas de token, on ignore")
            return

        status, data = self.api_request(
            "GET",
            "/api/mobile/client/me",
            authenticated=True
        )

        print("=== DEBUG REFRESH ===")
        print("STATUS:", status)
        print("DATA:", data)
        print("======================")

        if status == 200 and data.get("success"):

            if data.get("user"):
                self.current_user = data["user"]

            if data.get("client") is not None:
                self.current_client = data["client"]

    # ========================================================
    # AUTO-REFRESH EN ARRIÈRE-PLAN (POLLING)
    # ========================================================

    def start_auto_refresh(self):

        self.current_screen = "dashboard"

        if self.auto_refresh_active:
            return

        self.auto_refresh_active = True

        thread = threading.Thread(
            target=self._auto_refresh_loop,
            daemon=True
        )

        thread.start()

    def stop_auto_refresh(self):

        self.auto_refresh_active = False

    def _auto_refresh_loop(self):

        while self.auto_refresh_active:

            time.sleep(REFRESH_INTERVAL_SECONDS)

            if not self.auto_refresh_active:
                break

            if self.current_screen != "dashboard":
                break

            old_solde = (self.current_client or {}).get("solde")

            self.refresh_client_data()

            new_solde = (self.current_client or {}).get("solde")

            if (
                self.auto_refresh_active
                and self.current_screen == "dashboard"
                and new_solde != old_solde
            ):

                self.show_dashboard(_from_auto_refresh=True)

    # ========================================================
    # TABLEAU DE BORD
    # ========================================================

    def show_dashboard(self, e=None, _from_auto_refresh=False):

        self.current_screen = "dashboard"

        if not _from_auto_refresh:
            self.refresh_client_data()

        self.start_auto_refresh()

        user = self.current_user or {}
        client = self.current_client or {}

        first_name = (
            user.get("first_name")
            or user.get("prenom")
            or client.get("prenom")
            or user.get("nom")
            or client.get("nom")
            or "Utilisateur"
        )

        last_name = (
            user.get("last_name")
            or user.get("nom")
            or client.get("nom")
            or ""
        )

        account_number = (
            client.get("numero_compte")
            or user.get("numero_compte")
            or user.get("account_number")
            or ""
        )

        # ----------------------------------------------------
        # EN-TÊTE
        # ----------------------------------------------------

        header = ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                f"Bonjour {first_name} 👋",
                                size=21,
                                weight=ft.FontWeight.BOLD
                            ),

                            ft.Text(
                                last_name,
                                size=14
                            )
                        ],
                        spacing=2
                    ),

                    ft.Container(
                        expand=True
                    ),

                    ft.IconButton(
                        icon=ft.Icons.NOTIFICATIONS_OUTLINED,
                        on_click=self.show_notifications
                    )
                ],
                vertical_alignment=(
                    ft.CrossAxisAlignment.CENTER
                )
            ),
            padding=10
        )

        # ----------------------------------------------------
        # NUMÉRO DE COMPTE
        # ----------------------------------------------------

        if account_number:

            account_card = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Numéro de compte",
                            size=13
                        ),

                        ft.Text(
                            account_number,
                            size=19,
                            weight=ft.FontWeight.BOLD
                        )
                    ],
                    spacing=5
                ),
                padding=15,
                border_radius=12,
                bgcolor="#EAF2FF"
            )

        else:

            account_card = ft.Container(
                content=ft.Text(
                    "Compte GMES",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),
                padding=15,
                border_radius=12,
                bgcolor="#EAF2FF"
            )

        # ----------------------------------------------------
        # STATISTIQUES (comme le tableau de bord web)
        # ----------------------------------------------------

        solde = client.get(
            "solde",
            "—"
        )

        if isinstance(solde, (int, float)):

            solde_display = (
                f"{solde:,.2f} HTG"
            )

        else:

            solde_display = str(solde)

        prets_actifs = (
            "Oui"
            if client.get("a_un_pret_actif")
            else "Aucun"
        )

        stats_cards = ft.Row(
            [
                self.create_stat_card(
                    "💰",
                    "Solde",
                    solde_display,
                    "#2E7D32"
                ),

                self.create_stat_card(
                    "📊",
                    "Prêts actifs",
                    prets_actifs,
                    "#1565C0"
                ),

                self.create_stat_card(
                    "📈",
                    "Score crédit",
                    "—",
                    "#6A1B9A"
                ),

                self.create_stat_card(
                    "👥",
                    "Mon groupe",
                    "Aucun",
                    "#00838F"
                ),

                self.create_stat_card(
                    "💎",
                    "Niveau",
                    "—",
                    "#F9A825"
                ),

                self.create_stat_card(
                    "🔔",
                    "Notifications",
                    "—",
                    "#D84315"
                )
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            spacing=10
        )

        # ----------------------------------------------------
        # MENU — Gestion des prêts
        # ----------------------------------------------------

        section_prets = ft.Column(
            [
                ft.Text(
                    "💰 Gestion des prêts",
                    size=16,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Row(
                    [
                        self.create_menu_card(
                            "➕",
                            "Demander un prêt",
                            self.show_loan_request
                        ),

                        self.create_menu_card(
                            "📋",
                            "Mes prêts",
                            self.show_my_loans
                        ),

                        self.create_menu_card(
                            "💳",
                            "Rembourser",
                            self.show_payment
                        )
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                    spacing=10
                )
            ],
            spacing=8
        )

        # ----------------------------------------------------
        # MENU — Groupes solidaires
        # ----------------------------------------------------

        section_groupes = ft.Column(
            [
                ft.Text(
                    "👥 Groupes solidaires",
                    size=16,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Row(
                    [
                        self.create_menu_card(
                            "🏘️",
                            "Voir les groupes",
                            self.show_groups_list
                        ),

                        self.create_menu_card(
                            "👨‍👩‍👧‍👦",
                            "Mon groupe",
                            self.show_my_group
                        ),

                        self.create_menu_card(
                            "🤝",
                            "Prêt solidaire",
                            self.show_group_loan
                        )
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                    spacing=10
                )
            ],
            spacing=8
        )

        # ----------------------------------------------------
        # MENU — Intelligence artificielle
        # ----------------------------------------------------

        section_ia = ft.Column(
            [
                ft.Text(
                    "🤖 Intelligence artificielle",
                    size=16,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Row(
                    [
                        self.create_menu_card(
                            "🎯",
                            "Mon score crédit",
                            self.show_credit_score
                        ),

                        self.create_menu_card(
                            "💡",
                            "Recommandations",
                            self.show_recommendations
                        ),

                        self.create_menu_card(
                            "📊",
                            "Analytics perso",
                            self.show_stats
                        ),

                        self.create_menu_card(
                            "🔮",
                            "Prévisions",
                            self.show_forecasts
                        )
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                    spacing=10
                )
            ],
            spacing=8
        )

        # ----------------------------------------------------
        # MENU — Gamification
        # ----------------------------------------------------

        section_gamification = ft.Column(
            [
                ft.Text(
                    "💎 Gamification",
                    size=16,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Row(
                    [
                        self.create_menu_card(
                            "🏆",
                            "Mon niveau",
                            self.show_gamification_profile
                        ),

                        self.create_menu_card(
                            "🎯",
                            "Défis & objectifs",
                            self.show_challenges
                        ),

                        self.create_menu_card(
                            "🎁",
                            "Mes récompenses",
                            self.show_rewards
                        ),

                        self.create_menu_card(
                            "📈",
                            "Classement",
                            self.show_ranking
                        )
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                    spacing=10
                )
            ],
            spacing=8
        )

        # ----------------------------------------------------
        # MENU — Préférences
        # ----------------------------------------------------

        section_preferences = ft.Column(
            [
                ft.Text(
                    "⚙️ Préférences",
                    size=16,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Row(
                    [
                        self.create_menu_card(
                            "🔔",
                            "Notifications",
                            self.show_notifications
                        ),

                        self.create_menu_card(
                            "🔧",
                            "Paramètres",
                            self.show_settings
                        ),

                        self.create_menu_card(
                            "👤",
                            "Mon profil",
                            self.show_profile
                        ),

                        self.create_menu_card(
                            "🔐",
                            "Sécurité",
                            self.show_security
                        )
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                    spacing=10
                )
            ],
            spacing=8
        )

        # ----------------------------------------------------
        # DÉCONNEXION
        # ----------------------------------------------------

        logout_button = ft.OutlinedButton(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.LOGOUT),
                    ft.Text("Se déconnecter")
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            on_click=self.logout
        )

        # ----------------------------------------------------
        # CONTENU
        # ----------------------------------------------------

        content = ft.Column(
            [
                header,

                account_card,

                ft.Container(
                    height=5
                ),

                ft.Text(
                    "Résumé",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                stats_cards,

                ft.Container(
                    height=10
                ),

                ft.Text(
                    "Services GMES",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                section_prets,

                section_groupes,

                section_ia,

                section_gamification,

                section_preferences,

                ft.Container(
                    height=15
                ),

                logout_button
            ],
            spacing=15
        )

        self.page.clean()

        self.page.add(content)

        self.page.update()

    # ========================================================
    # CARTES STATISTIQUES
    # ========================================================

    def create_stat_card(
        self,
        icon,
        title,
        value,
        text_color
    ):

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        icon,
                        size=25
                    ),

                    ft.Text(
                        title,
                        size=13
                    ),

                    ft.Text(
                        value,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=text_color
                    )
                ],
                spacing=4
            ),
            width=145,
            padding=15,
            border_radius=12,
            bgcolor="#FFFFFF"
        )

    # ========================================================
    # CARTES MENU
    # ========================================================

    def create_menu_card(
        self,
        icon,
        title,
        callback
    ):

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        icon,
                        size=30
                    ),

                    ft.Text(
                        title,
                        size=15,
                        weight=ft.FontWeight.BOLD
                    )
                ],
                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
                alignment=(
                    ft.MainAxisAlignment.CENTER
                ),
                spacing=8
            ),
            padding=15,
            border_radius=12,
            bgcolor="#FFFFFF",
            on_click=callback
        )

    # ========================================================
    # MES PRÊTS
    # ========================================================

    def show_my_loans(self, e=None):

        self.show_simple_page(
            "📋 Mes prêts",
            [
                ft.Text(
                    "Vos prêts apparaîtront ici.",
                    size=17
                ),

                ft.Text(
                    "Cette section sera connectée "
                    "à l'API GMES."
                )
            ]
        )

    # ========================================================
    # REMBOURSEMENT
    # ========================================================

    def show_payment(self, e=None):

        self.show_simple_page(
            "💳 Remboursement",
            [
                ft.Text(
                    "Effectuer un remboursement",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Les moyens de paiement seront "
                    "connectés au backend GMES."
                )
            ]
        )

    # ========================================================
    # GROUPE
    # ========================================================

    def show_my_group(self, e=None):

        self.show_simple_page(
            "👥 Mon groupe",
            [
                ft.Text(
                    "Informations du groupe",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Les informations de votre groupe "
                    "apparaîtront ici."
                )
            ]
        )

    # ========================================================
    # DEMANDE DE PRÊT
    # ========================================================

    def show_loan_request(self, e=None):

        self.show_simple_page(
            "➕ Demander un prêt",
            [
                ft.Text(
                    "Nouvelle demande de prêt",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Ce formulaire sera connecté "
                    "à l'API GMES."
                )
            ]
        )

    # ========================================================
    # LISTE DES GROUPES
    # ========================================================

    def show_groups_list(self, e=None):

        self.show_simple_page(
            "🏘️ Groupes solidaires",
            [
                ft.Text(
                    "Groupes disponibles",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "La liste des groupes sera "
                    "chargée depuis l'API GMES."
                )
            ]
        )

    # ========================================================
    # PRÊT SOLIDAIRE
    # ========================================================

    def show_group_loan(self, e=None):

        self.show_simple_page(
            "🤝 Prêt solidaire",
            [
                ft.Text(
                    "Demande de prêt solidaire",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Disponible une fois que vous "
                    "aurez rejoint un groupe."
                )
            ]
        )

    # ========================================================
    # SCORE CRÉDIT
    # ========================================================

    def show_credit_score(self, e=None):

        self.show_simple_page(
            "🎯 Mon score crédit",
            [
                ft.Text(
                    "Score de crédit",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Votre score sera calculé et "
                    "affiché ici."
                )
            ]
        )

    # ========================================================
    # RECOMMANDATIONS
    # ========================================================

    def show_recommendations(self, e=None):

        self.show_simple_page(
            "💡 Recommandations",
            [
                ft.Text(
                    "Recommandations personnalisées",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Nos suggestions de prêts adaptées "
                    "seront affichées ici."
                )
            ]
        )

    # ========================================================
    # PRÉVISIONS
    # ========================================================

    def show_forecasts(self, e=None):

        self.show_simple_page(
            "🔮 Prévisions",
            [
                ft.Text(
                    "Prévisions de remboursement",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Vos prévisions financières seront "
                    "affichées ici."
                )
            ]
        )

    # ========================================================
    # GAMIFICATION — PROFIL
    # ========================================================

    def show_gamification_profile(self, e=None):

        self.show_simple_page(
            "🏆 Mon niveau",
            [
                ft.Text(
                    "Profil de gamification",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Votre niveau et vos points "
                    "seront affichés ici."
                )
            ]
        )

    # ========================================================
    # DÉFIS
    # ========================================================

    def show_challenges(self, e=None):

        self.show_simple_page(
            "🎯 Défis & objectifs",
            [
                ft.Text(
                    "Défis en cours",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Vos défis et objectifs seront "
                    "affichés ici."
                )
            ]
        )

    # ========================================================
    # RÉCOMPENSES
    # ========================================================

    def show_rewards(self, e=None):

        self.show_simple_page(
            "🎁 Mes récompenses",
            [
                ft.Text(
                    "Récompenses obtenues",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Vos récompenses seront affichées "
                    "ici."
                )
            ]
        )

    # ========================================================
    # CLASSEMENT
    # ========================================================

    def show_ranking(self, e=None):

        self.show_simple_page(
            "📈 Classement",
            [
                ft.Text(
                    "Classement des clients",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Le classement sera affiché ici."
                )
            ]
        )

    # ========================================================
    # PROFIL
    # ========================================================

    def show_profile(self, e=None):

        user = self.current_user or {}

        self.show_simple_page(
            "👤 Mon profil",
            [
                ft.Text(
                    "Informations personnelles",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    f"Nom : {user.get('last_name', '—')}"
                ),

                ft.Text(
                    f"Prénom : {user.get('first_name', '—')}"
                ),

                ft.Text(
                    f"Email : {user.get('email', '—')}"
                )
            ]
        )

    # ========================================================
    # SÉCURITÉ
    # ========================================================

    def show_security(self, e=None):

        self.show_simple_page(
            "🔐 Sécurité",
            [
                ft.Text(
                    "Mot de passe et sécurité",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "La gestion du mot de passe et de "
                    "la reconnaissance faciale sera "
                    "disponible ici."
                )
            ]
        )

    # ========================================================
    # STATISTIQUES
    # ========================================================

    def show_stats(self, e=None):

        self.show_simple_page(
            "📊 Statistiques",
            [
                ft.Text(
                    "Statistiques",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Vos statistiques financières "
                    "seront affichées ici."
                )
            ]
        )

    # ========================================================
    # NOTIFICATIONS
    # ========================================================

    def show_notifications(self, e=None):

        self.show_simple_page(
            "🔔 Notifications",
            [
                ft.Text(
                    "Notifications",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Aucune notification chargée "
                    "pour le moment."
                )
            ]
        )

    # ========================================================
    # PARAMÈTRES
    # ========================================================

    def show_settings(self, e=None):

        self.show_simple_page(
            "⚙️ Paramètres",
            [
                ft.Text(
                    "Paramètres du compte",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Divider(),

                ft.ListTile(
                    leading=ft.Icon(
                        ft.Icons.PERSON
                    ),

                    title=ft.Text(
                        "Profil"
                    ),

                    subtitle=ft.Text(
                        "Gérer vos informations personnelles"
                    )
                ),

                ft.ListTile(
                    leading=ft.Icon(
                        ft.Icons.SECURITY
                    ),

                    title=ft.Text(
                        "Sécurité"
                    ),

                    subtitle=ft.Text(
                        "Mot de passe et sécurité"
                    )
                ),

                ft.Container(
                    height=10
                ),

                ft.ElevatedButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.LOGOUT),
                            ft.Text("Se déconnecter")
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    on_click=self.logout
                )
            ]
        )

    # ========================================================
    # PAGE SIMPLE
    # ========================================================

    def show_simple_page(
        self,
        title,
        controls
    ):

        self.current_screen = "simple_page"

        back_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda e: self.show_dashboard()
        )

        header = ft.Row(
            [
                back_button,

                ft.Text(
                    title,
                    size=21,
                    weight=ft.FontWeight.BOLD
                )
            ]
        )

        content = ft.Column(
            [
                header,

                ft.Divider(),

                *controls
            ],
            spacing=15
        )

        self.page.clean()

        self.page.add(content)

        self.page.update()

    # ========================================================
    # DÉCONNEXION
    # ========================================================

    def logout(self, e=None):

        self.stop_auto_refresh()
        self.current_screen = "login"

        try:

            if self.token:

                self.api_request(
                    "POST",
                    "/api/mobile/logout",
                    authenticated=True
                )

        except Exception:
            pass

        self.token = None
        self.current_user = None
        self.current_client = None

        self.show_login_view()

    # ========================================================
    # MESSAGES
    # ========================================================

    def _notify(self, message):

        snackbar = ft.SnackBar(
            content=ft.Text(message)
        )

        page = self.page

        if hasattr(page, "open"):
            page.open(snackbar)

        elif hasattr(page, "show_dialog"):
            page.show_dialog(snackbar)

        elif hasattr(page, "show_snack_bar"):
            page.show_snack_bar(snackbar)

        else:
            page.overlay.append(snackbar)
            snackbar.open = True

        page.update()

    def show_success(self, message):

        self._notify(message)

    def show_error(self, message):

        self._notify(message)


# ============================================================
# LANCEMENT
# ============================================================

def main():

    app = GMESMobileApp()

    ft.run(
        app.main
    )


if __name__ == "__main__":
    main()