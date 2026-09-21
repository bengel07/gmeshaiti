import flet as ft
import requests


# ============================================================
# CONFIGURATION
# ============================================================

API_BASE_URL = "https://gmeshaiti-aeo3.onrender.com"


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
            text="Se connecter",
            icon=ft.Icons.LOGIN,
            width=320,
            height=48,
            on_click=self.login
        )

        register_button = ft.TextButton(
            text="Créer un compte",
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
            text="Créer mon compte",
            icon=ft.Icons.PERSON_ADD,
            width=320,
            height=48,
            on_click=self.handle_register
        )

        back_button = ft.TextButton(
            text="← Retour à la connexion",
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
    # TABLEAU DE BORD
    # ========================================================

    def show_dashboard(self, e=None):

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
        # STATISTIQUES
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
                    "Prêts",
                    "—",
                    "#1565C0"
                ),

                self.create_stat_card(
                    "⏰",
                    "Prochain",
                    "—",
                    "#EF6C00"
                )
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            spacing=10
        )

        # ----------------------------------------------------
        # MENU
        # ----------------------------------------------------

        menu_grid = ft.GridView(
            runs_count=2,
            max_extent=170,
            child_aspect_ratio=1,
            spacing=10,
            run_spacing=10,
            expand=False
        )

        menu_grid.controls = [

            self.create_menu_card(
                "📋",
                "Mes prêts",
                self.show_my_loans
            ),

            self.create_menu_card(
                "💳",
                "Rembourser",
                self.show_payment
            ),

            self.create_menu_card(
                "👥",
                "Mon groupe",
                self.show_my_group
            ),

            self.create_menu_card(
                "📊",
                "Statistiques",
                self.show_stats
            ),

            self.create_menu_card(
                "🔔",
                "Notifications",
                self.show_notifications
            ),

            self.create_menu_card(
                "⚙️",
                "Paramètres",
                self.show_settings
            )
        ]

        # ----------------------------------------------------
        # DÉCONNEXION
        # ----------------------------------------------------

        logout_button = ft.OutlinedButton(
            text="Se déconnecter",
            icon=ft.Icons.LOGOUT,
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

                menu_grid,

                ft.Container(
                    height=15
                ),

                logout_button
            ],
            spacing=10
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
                    text="Se déconnecter",
                    icon=ft.Icons.LOGOUT,
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

    def show_success(self, message):

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message)
        )

        self.page.snack_bar.open = True

        self.page.update()

    def show_error(self, message):

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message)
        )

        self.page.snack_bar.open = True

        self.page.update()


# ============================================================
# LANCEMENT
# ============================================================

def main():

    app = GMESMobileApp()

    ft.app(
        target=app.main
    )


if __name__ == "__main__":
    main()

