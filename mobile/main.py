import flet as ft
import requests

API_URL = "https://gmeshaiti-aeo3.onrender.com"

# ============================================================
# COULEURS GMES
# ============================================================

BLUE = "#0645AD"
DARK_BLUE = "#063477"
GOLD = "#F5B51B"
GREEN = "#16A085"
PURPLE = "#6545D8"
LIGHT_BG = "#F5F7FB"
TEXT = "#102A63"
GREY = "#66789C"


# ============================================================
# PETITS COMPOSANTS REUTILISABLES
# ============================================================

def action_button(icon, title, color, on_click=None):
    return ft.Container(
        width=150,
        height=125,
        border_radius=20,
        bgcolor=color,
        padding=15,
        on_click=on_click,
        content=ft.Column(
            [
                ft.Icon(icon, color=ft.Colors.WHITE, size=34),
                ft.Text(
                    title,
                    color=ft.Colors.WHITE,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
    )


def transaction_item(icon, title, date, amount, badge_text="Effectué", badge_type="blue"):
    badge_colors = {
        "green": ("#087F23", "#DDF6E5"),
        "blue": (BLUE, "#E8F0FF"),
    }
    text_color, bg_color = badge_colors.get(badge_type, badge_colors["blue"])

    return ft.Container(
        padding=ft.Padding.symmetric(vertical=12),
        border=ft.Border.only(bottom=ft.BorderSide(1, "#E5EAF2")),
        content=ft.Row(
            [
                ft.Container(
                    width=45,
                    height=45,
                    border_radius=50,
                    bgcolor="#EAF2FF",
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(icon, color=BLUE, size=23),
                ),
                ft.Column(
                    [
                        ft.Text(title, size=15, weight=ft.FontWeight.BOLD, color=TEXT),
                        ft.Text(date, size=12, color=GREY),
                    ],
                    expand=True,
                    spacing=3,
                ),
                ft.Column(
                    [
                        ft.Text(
                            amount,
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT if badge_type != "green" else "#087F23",
                        ),
                        ft.Container(
                            bgcolor=bg_color,
                            border_radius=20,
                            padding=ft.Padding.symmetric(horizontal=12, vertical=4),
                            content=ft.Text(
                                badge_text,
                                size=11,
                                color=text_color,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    spacing=3,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )


# ============================================================
# APPLICATION PRINCIPALE
# ============================================================

def main(page: ft.Page):
    # Variables de session
    token = None
    user = {}
    client = {}

    # Configuration de la page
    page.title = "GMES App"
    page.bgcolor = LIGHT_BG
    page.padding = 0
    page.window.width = 430
    page.window.height = 850
    page.theme_mode = ft.ThemeMode.LIGHT

    # Champ du formulaire de connexion
    identifier_field = ft.TextField(
        label="Email ou numéro de compte",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        border_radius=12,
    )

    password_field = ft.TextField(
        label="Mot de passe",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        border_radius=12,
    )

    error_text = ft.Text("", color="#D32F2F", size=13)

    def message(txt):
        page.snack_bar = ft.SnackBar(ft.Text(txt))
        page.snack_bar.open = True
        page.update()

    def afficher_erreur(msg):
        error_text.value = msg
        page.update()

    # --- CONNEXION BACKEND ---
    def connecter(e):
        nonlocal token, user, client

        identifier = identifier_field.value.strip() if identifier_field.value else ""
        password = password_field.value if password_field.value else ""

        if not identifier or not password:
            afficher_erreur("Veuillez remplir tous les champs.")
            return

        afficher_erreur("")  # Reinitialiser les erreurs

        try:
            response = requests.post(
                f"{API_URL}/auth/api/mobile/login",
                json={
                    "identifier": identifier,
                    "password": password,
                },
                timeout=30,
            )

            print("================================")
            print("STATUT API :", response.status_code)
            print("URL API :", response.url)
            print("CONTENT-TYPE :", response.headers.get("Content-Type"))
            print("REPONSE API :", response.text[:1000])
            print("================================")

            if not response.text.strip():
                afficher_erreur("Le serveur GMES a retourné une réponse vide.")
                return

            try:
                data = response.json()
            except Exception:
                afficher_erreur(
                    f"Réponse serveur invalide ({response.status_code})."
                )
                return

            if not data.get("success"):
                afficher_erreur(data.get("error", "Identifiants incorrects."))
                return

            token = data.get("token")
            user = data.get("user") or {}
            client = data.get("client") or {}

            # Récupérer les données fraîches depuis l'API
            me_response = requests.get(
                f"{API_URL}/auth/api/mobile/client/me",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                },
                timeout=30,
            )

            me_data = me_response.json()

            if not me_data.get("success"):
                afficher_erreur(
                    me_data.get(
                        "error",
                        "Impossible de récupérer votre compte GMES."
                    )
                )
                return

            user = me_data.get("user") or user
            client = me_data.get("client") or client

            print("LOGIN GMES RÉUSSI")
            print("CLIENT :", client)

            afficher_dashboard()

        except requests.exceptions.ConnectionError:
            afficher_erreur("Impossible de contacter le serveur GMES.")
        except requests.exceptions.Timeout:
            afficher_erreur("Le serveur GMES ne répond pas.")
        except Exception as ex:
            print("ERREUR LOGIN :", repr(ex))
            afficher_erreur("Une erreur est survenue.")

    login_button = ft.ElevatedButton(
        "Se connecter",
        icon=ft.Icons.LOGIN,
        width=300,
        height=50,
        on_click=connecter,
    )

    # --- ÉCRAN LOGIN ---
    def afficher_login():
        page.controls.clear()
        page.add(
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                padding=20,
                content=ft.Column(
                    [
                        ft.Container(
                            width=90,
                            height=90,
                            bgcolor=GOLD,
                            border_radius=50,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Icon(ft.Icons.GROUPS, color=ft.Colors.WHITE, size=48),
                        ),
                        ft.Text("GMES App", size=32, weight=ft.FontWeight.BOLD, color=BLUE),
                        ft.Text("GMES youn sipote lot", size=15, italic=True, color=GREY),
                        ft.Container(height=20),
                        identifier_field,
                        password_field,
                        error_text,
                        login_button,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
            )
        )
        page.update()

    # --- ÉCRAN DASHBOARD ---
    def afficher_dashboard():
        page.controls.clear()

        # Header
        header = ft.Container(
            padding=ft.Padding.only(left=20, right=15, top=25, bottom=20),
            bgcolor=BLUE,
            border_radius=ft.BorderRadius.only(bottom_left=35, bottom_right=35),
            content=ft.Row(
                [
                    ft.Container(
                        width=50,
                        height=50,
                        border_radius=50,
                        bgcolor=GOLD,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(ft.Icons.GROUPS, color=ft.Colors.WHITE, size=30),
                    ),
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text("GMES", size=26, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                    ft.Text("App", size=26, color=GOLD, weight=ft.FontWeight.BOLD),
                                ],
                                spacing=4,
                            ),
                            ft.Text("GMES youn sipote lot", size=13, color=ft.Colors.WHITE, italic=True),
                        ],
                        spacing=0,
                        expand=True,
                    ),
                    ft.Stack(
                        [
                            ft.IconButton(
                                icon=ft.Icons.NOTIFICATIONS_OUTLINED,
                                icon_color=ft.Colors.WHITE,
                                icon_size=28,
                                on_click=lambda e: message("2 nouvelles notifications"),
                            ),
                            ft.Container(
                                width=18,
                                height=18,
                                right=4,
                                top=4,
                                border_radius=50,
                                bgcolor="#E53935",
                                alignment=ft.Alignment.CENTER,
                                content=ft.Text("2", size=10, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            ),
                        ],
                    ),
                    ft.IconButton(
                        icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                        icon_color=ft.Colors.WHITE,
                        icon_size=30,
                        on_click=lambda e: message("Profil utilisateur"),
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        # Balance Card
        balance_card = ft.Container(
            margin=ft.Margin.only(left=20, right=20, top=15),
            padding=20,
            height=175,
            border_radius=22,
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=["#0754C9", "#063477"],
            ),
            content=ft.Stack(
                [
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        width=42,
                                        height=42,
                                        border_radius=12,
                                        bgcolor="#3184F4",
                                        alignment=ft.Alignment.CENTER,
                                        content=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, color=ft.Colors.WHITE,
                                                        size=23),
                                    ),
                                    ft.Text("Kont ou", color=ft.Colors.WHITE, size=17, weight=ft.FontWeight.BOLD),
                                    ft.Container(expand=True),
                                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.WHITE, size=28),
                                ]
                            ),
                            ft.Text(
                                f"{client.get('solde', 0):,.2f} HTG",
                                size=32,
                                color=ft.Colors.WHITE,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                f"No. kont : {client.get('numero_compte', '-')}",
                                size=13,
                                color="#DDE9FF",
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Container(
                        bottom=-20,
                        right=-20,
                        width=130,
                        height=20,
                        bgcolor=GOLD,
                        border_radius=ft.BorderRadius.only(top_left=50, bottom_right=22),
                    ),
                ]
            ),
        )

        # Loan Card
        # ============================================================
        # CARTE PRÊT
        # ============================================================

        pret_actif = client.get("a_un_pret_actif", False)

        if pret_actif:

            loan_card = ft.Container(
                margin=ft.Margin.only(
                    left=20,
                    right=20,
                    top=18,
                ),
                padding=18,
                bgcolor=ft.Colors.WHITE,
                border_radius=22,
                shadow=ft.BoxShadow(
                    blur_radius=10,
                    spread_radius=1,
                    color="#15000000",
                ),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Container(
                                    width=48,
                                    height=48,
                                    border_radius=50,
                                    bgcolor="#DDF6EA",
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Icon(
                                        ft.Icons.ACCOUNT_BALANCE,
                                        color=GREEN,
                                        size=26,
                                    ),
                                ),

                                ft.Column(
                                    [
                                        ft.Text(
                                            "Prêt en cours",
                                            size=19,
                                            color=TEXT,
                                            weight=ft.FontWeight.BOLD,
                                        ),

                                        ft.Text(
                                            "Prêt actif",
                                            size=12,
                                            color=GREY,
                                        ),
                                    ],
                                    expand=True,
                                    spacing=2,
                                ),

                                ft.Container(
                                    bgcolor="#DDF6E5",
                                    border_radius=20,
                                    padding=ft.Padding.symmetric(
                                        horizontal=12,
                                        vertical=6,
                                    ),
                                    content=ft.Text(
                                        "Actif",
                                        color="#087F23",
                                        size=12,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ),
                            ]
                        ),

                        ft.Divider(
                            height=15,
                            color="#E6EAF1",
                        ),

                        ft.Text(
                            "Votre prêt actif sera affiché ici.",
                            size=14,
                            color=GREY,
                        ),
                    ],
                    spacing=8,
                ),
            )

        else:

            loan_card = ft.Container(
                margin=ft.Margin.only(
                    left=20,
                    right=20,
                    top=18,
                ),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=22,
                shadow=ft.BoxShadow(
                    blur_radius=10,
                    spread_radius=1,
                    color="#15000000",
                ),
                content=ft.Row(
                    [
                        ft.Container(
                            width=50,
                            height=50,
                            border_radius=50,
                            bgcolor="#EAF2FF",
                            alignment=ft.Alignment.CENTER,
                            content=ft.Icon(
                                ft.Icons.ACCOUNT_BALANCE_OUTLINED,
                                color=BLUE,
                                size=27,
                            ),
                        ),

                        ft.Column(
                            [
                                ft.Text(
                                    "Aucun prêt actif",
                                    size=18,
                                    color=TEXT,
                                    weight=ft.FontWeight.BOLD,
                                ),

                                ft.Text(
                                    "Vous n'avez actuellement aucun prêt en cours.",
                                    size=13,
                                    color=GREY,
                                ),
                            ],
                            expand=True,
                            spacing=4,
                        ),
                    ],
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )

        # Actions
        actions = ft.Container(
            margin=ft.Margin.only(left=20, right=20, top=18),
            content=ft.Row(
                [
                    action_button(ft.Icons.DESCRIPTION, "Demander\nun prêt", "#0874E8",
                                  lambda e: message("Demande de prêt")),
                    action_button(ft.Icons.CREDIT_CARD, "Rembourser", "#E5A817", lambda e: message("Remboursements")),
                    action_button(ft.Icons.SAVINGS, "Épargne", GREEN, lambda e: message("Épargne")),
                    action_button(ft.Icons.SWAP_HORIZ, "Transactions", PURPLE, lambda e: message("Transactions")),
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=12,
            ),
        )

        # Transactions
        transactions_card = ft.Container(
            margin=ft.Margin.only(left=20, right=20, top=18, bottom=20),
            padding=18,
            bgcolor=ft.Colors.WHITE,
            border_radius=22,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Dernières transactions", size=18, color=TEXT, weight=ft.FontWeight.BOLD),
                            ft.Container(expand=True),
                            ft.TextButton("Voir tout ›", on_click=lambda e: message("Transactions")),
                        ]
                    ),
                    transaction_item(ft.Icons.ARROW_DOWNWARD, "Remboursement prêt", "12 sept. 2026", "- 6,200 HTG",
                                     "Reçu", "green"),
                    transaction_item(ft.Icons.ARROW_UPWARD, "Dépôt épargne", "08 sept. 2026", "+ 2,000 HTG", "Crédité",
                                     "green"),
                    transaction_item(ft.Icons.CREDIT_CARD, "Retrait guichet", "05 sept. 2026", "- 3,000 HTG",
                                     "Effectué", "blue"),
                ],
                spacing=0,
            ),
        )

        body = ft.Column(
            [
                ft.Container(
                    padding=ft.Padding.only(left=20, right=20, top=15),
                    content=ft.Column(
                        [
                            ft.Text(f"Bonjou, {client.get('prenom', '')}", size=25, color=TEXT,
                                    weight=ft.FontWeight.BOLD),
                            ft.Text("Kont ou, pi fòs ansanm !", size=15, color=GREY),
                        ],
                        spacing=2,
                    ),
                ),
                balance_card,
                loan_card,
                actions,
                transactions_card,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0,
        )

        navigation_bar = ft.NavigationBar(
            selected_index=0,
            on_change=lambda e: message(f"Onglet sélectionné: {e.control.selected_index}"),
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Accueil"),
                ft.NavigationBarDestination(icon=ft.Icons.DESCRIPTION_OUTLINED, selected_icon=ft.Icons.DESCRIPTION,
                                            label="Prêts"),
                ft.NavigationBarDestination(icon=ft.Icons.SWAP_HORIZ_OUTLINED, selected_icon=ft.Icons.SWAP_HORIZ,
                                            label="Paiements"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icons.PERSON,
                                            label="Profil"),
            ],
        )

        page.add(
            ft.Column([header, body, navigation_bar], expand=True, spacing=0)
        )
        page.update()

    # Démarrage sur la page de connexion
    afficher_login()


if __name__ == "__main__":
    ft.run(main)