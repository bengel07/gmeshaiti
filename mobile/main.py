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
    return ft.GestureDetector(
        on_tap=on_click,
        content=ft.Container(
            width=150,
            height=125,
            border_radius=20,
            bgcolor=color,
            padding=15,
            content=ft.Column(
                [
                    ft.Icon(
                        icon,
                        color=ft.Colors.WHITE,
                        size=34,
                    ),
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

    # ============================================================
    # NOTIFICATIONS
    # ============================================================

    notifications = []
    nombre_notifications_non_lues = 0

    def charger_notifications():
        nonlocal notifications, nombre_notifications_non_lues

        if not token:
            return False

        try:
            response = requests.get(
                f"{API_URL}/api/mobile/notifications",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                },
                timeout=30,
            )

            print("================================")
            print("NOTIFICATIONS")
            print("STATUT :", response.status_code)
            print("REPONSE :", response.text[:2000])
            print("================================")

            if response.status_code != 200:
                print("❌ Impossible de récupérer les notifications")
                return False

            data = response.json()

            if not data.get("success"):
                print(
                    "❌ API notifications :",
                    data.get("error")
                )
                return False

            notifications = data.get("notifications", [])
            nombre_notifications_non_lues = data.get("non_lues", 0)

            print(
                f"✅ {len(notifications)} notifications "
                f"({nombre_notifications_non_lues} non lues)"
            )

            return True

        except requests.exceptions.Timeout:
            print("❌ Timeout notifications")
            return False

        except requests.exceptions.ConnectionError:
            print("❌ Serveur inaccessible")
            return False

        except Exception as ex:
            print("❌ Erreur notifications :", repr(ex))
            return False

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

            charger_notifications()

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

    def afficher_notifications(e=None):
        charger_notifications()

        page.controls.clear()

        # --------------------------------------------------------
        # HEADER
        # --------------------------------------------------------

        header = ft.Container(
            bgcolor=BLUE,
            padding=ft.Padding.only(
                left=15,
                right=15,
                top=20,
                bottom=20
            ),
            content=ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e: afficher_dashboard()
                    ),

                    ft.Text(
                        "Notifications",
                        color=ft.Colors.WHITE,
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        expand=True
                    ),

                    ft.Text(
                        str(nombre_notifications_non_lues),
                        color=ft.Colors.WHITE,
                        size=16,
                        weight=ft.FontWeight.BOLD
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        # --------------------------------------------------------
        # LISTE
        # --------------------------------------------------------

        liste = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        if not notifications:

            liste.controls.append(
                ft.Container(
                    padding=40,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.Icons.NOTIFICATIONS_NONE,
                                size=60,
                                color=GREY
                            ),

                            ft.Text(
                                "Aucune notification",
                                size=18,
                                color=TEXT,
                                weight=ft.FontWeight.BOLD
                            ),

                            ft.Text(
                                "Vous n'avez aucune notification pour le moment.",
                                size=14,
                                color=GREY,
                                text_align=ft.TextAlign.CENTER
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10
                    )
                )
            )

        else:

            for notification in notifications:

                notification_id = notification.get("id")
                titre = notification.get("titre", "Notification")
                texte = notification.get("message", "")
                type_notif = notification.get("type", "info")
                lue = notification.get("lue", False)
                date_creation = notification.get(
                    "date_creation",
                    ""
                )

                if type_notif == "success":
                    icone = ft.Icons.CHECK_CIRCLE
                    couleur = GREEN

                elif type_notif in ("danger", "error"):
                    icone = ft.Icons.ERROR
                    couleur = "#D32F2F"

                elif type_notif == "warning":
                    icone = ft.Icons.WARNING
                    couleur = GOLD

                else:
                    icone = ft.Icons.INFO
                    couleur = BLUE

                def cliquer_notification(
                        e,
                        notification=notification,
                        nid=notification_id,
                        deja_lue=lue
                ):
                    if not deja_lue:
                        marquer_notification_lue(nid)

                    lien = notification.get("lien")

                    if not lien:
                        message("Cette notification n'a pas de lien.")
                        return

                    if lien.startswith("/"):
                        lien = API_URL + lien

                    print("🔗 Ouverture :", lien)

                    async def ouvrir_url_async():
                        await ft.UrlLauncher().launch_url(lien)

                    page.run_task(ouvrir_url_async)

                liste.controls.append(
                    ft.Container(
                        margin=ft.Margin.only(
                            left=15,
                            right=15,
                            top=5
                        ),
                        padding=15,
                        bgcolor=(
                            ft.Colors.WHITE
                            if lue
                            else "#EEF4FF"
                        ),
                        border_radius=15,
                        border=ft.Border.all(
                            1,
                            "#E1E7F0"
                        ),
                        on_click=cliquer_notification,
                        content=ft.Row(
                            [
                                ft.Container(
                                    width=45,
                                    height=45,
                                    border_radius=50,
                                    bgcolor=couleur,
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Icon(
                                        icone,
                                        color=ft.Colors.WHITE,
                                        size=22
                                    )
                                ),

                                ft.Column(
                                    [
                                        ft.Text(
                                            titre,
                                            size=15,
                                            color=TEXT,
                                            weight=(
                                                ft.FontWeight.BOLD
                                                if not lue
                                                else ft.FontWeight.NORMAL
                                            )
                                        ),

                                        ft.Text(
                                            texte,
                                            size=13,
                                            color=GREY,
                                            max_lines=3,
                                            overflow=ft.TextOverflow.ELLIPSIS
                                        ),

                                        ft.Text(
                                            date_creation,
                                            size=10,
                                            color=GREY
                                        )
                                    ],
                                    expand=True,
                                    spacing=4
                                ),

                                (
                                    ft.Container(
                                        width=9,
                                        height=9,
                                        bgcolor="#D32F2F",
                                        border_radius=50
                                    )
                                    if not lue
                                    else ft.Container(width=9)
                                )
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    )
                )

        page.add(
            ft.Column(
                [
                    header,
                    liste
                ],
                expand=True,
                spacing=0
            )
        )

        page.update()

    # def ouvrir_notification(notification):
    #     lien = notification.get("lien") or notification.get("url")
    #
    #     if not lien:
    #         message("Cette notification n'a pas de lien.")
    #         return
    #
    #     print("🔗 Lien notification :", lien)
    #
    #     # Ici on ouvre le lien

    def marquer_notification_lue(notification_id):

        if not token:
            return

        try:

            response = requests.post(
                f"{API_URL}/api/mobile/notifications/{notification_id}/lire",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                },
                timeout=30,
            )

            print(
                "Notification lue :",
                notification_id,
                response.status_code
            )

            if response.status_code == 200:

                for notification in notifications:

                    if notification.get("id") == notification_id:
                        notification["lue"] = True

                nonlocal_nombre = None

        except Exception as ex:

            print(
                "❌ Erreur lecture notification :",
                repr(ex)
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

    def afficher_demande_pret():
        page.controls.clear()

        montant_field = ft.TextField(
            label="Montant demandé (HTG)",
            prefix_icon=ft.Icons.ATTACH_MONEY,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=12,
        )

        duree_field = ft.TextField(
            label="Durée (mois)",
            prefix_icon=ft.Icons.CALENDAR_MONTH,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=12,
        )

        motif_field = ft.TextField(
            label="Motif de la demande",
            prefix_icon=ft.Icons.DESCRIPTION,
            multiline=True,
            min_lines=3,
            max_lines=5,
            border_radius=12,
        )

        resultat = ft.Text("", size=13)

        def envoyer_demande(e):

            if not token:
                resultat.value = "Session expirée. Veuillez vous reconnecter."
                resultat.color = "#D32F2F"
                page.update()
                return

            montant = montant_field.value.strip()
            duree = duree_field.value.strip()
            motif = motif_field.value.strip()

            if not montant or not duree:
                resultat.value = "Veuillez remplir le montant et la durée."
                resultat.color = "#D32F2F"
                page.update()
                return

            try:
                montant_float = float(montant)
                duree_int = int(duree)
            except ValueError:
                resultat.value = "Montant ou durée invalide."
                resultat.color = "#D32F2F"
                page.update()
                return

            if montant_float < 10000:
                resultat.value = "Le montant minimum est de 10 000 HTG."
                resultat.color = "#D32F2F"
                page.update()
                return

            if duree_int < 3 or duree_int > 60:
                resultat.value = "La durée doit être entre 3 et 60 mois."
                resultat.color = "#D32F2F"
                page.update()
                return

            try:
                response = requests.post(
                    f"{API_URL}/prets/demande-pret",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Accept": "application/json",
                    },
                    json={
                        "montant": montant_float,
                        "duree_mois": duree_int,
                        "motif": motif,
                    },
                    timeout=30,
                )

                print("================================")
                print("DEMANDE DE PRÊT")
                print("STATUT :", response.status_code)
                print("REPONSE :", response.text[:2000])
                print("================================")

                try:
                    data = response.json()
                except Exception:
                    data = {}

                if response.status_code in (200, 201) and data.get("success"):
                    resultat.value = data.get(
                        "message",
                        "Votre demande de prêt a été envoyée."
                    )
                    resultat.color = GREEN

                    montant_field.value = ""
                    duree_field.value = ""
                    motif_field.value = ""

                    page.update()

                    return

                resultat.value = data.get(
                    "error",
                    data.get(
                        "message",
                        f"Erreur serveur ({response.status_code})"
                    )
                )
                resultat.color = "#D32F2F"
                page.update()

            except requests.exceptions.Timeout:
                resultat.value = "Le serveur GMES ne répond pas."
                resultat.color = "#D32F2F"
                page.update()

            except requests.exceptions.ConnectionError:
                resultat.value = "Impossible de contacter le serveur GMES."
                resultat.color = "#D32F2F"
                page.update()

            except Exception as ex:
                print("ERREUR DEMANDE PRÊT :", repr(ex))
                resultat.value = "Une erreur est survenue."
                resultat.color = "#D32F2F"
                page.update()

        page.add(
            ft.Column(
                [
                    ft.Container(
                        bgcolor=BLUE,
                        padding=ft.Padding.only(
                            left=10,
                            right=20,
                            top=20,
                            bottom=20,
                        ),
                        content=ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=ft.Colors.WHITE,
                                    on_click=lambda e: afficher_dashboard(),
                                ),
                                ft.Text(
                                    "Demande de prêt",
                                    color=ft.Colors.WHITE,
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    expand=True,
                                ),
                            ],
                        ),
                    ),

                    ft.Container(
                        padding=20,
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Nouvelle demande",
                                    size=24,
                                    color=TEXT,
                                    weight=ft.FontWeight.BOLD,
                                ),

                                ft.Text(
                                    "Remplissez les informations de votre demande de prêt.",
                                    size=14,
                                    color=GREY,
                                ),

                                ft.Container(height=10),

                                montant_field,
                                duree_field,
                                motif_field,

                                resultat,

                                ft.ElevatedButton(
                                    "Envoyer la demande",
                                    icon=ft.Icons.SEND,
                                    width=300,
                                    height=50,
                                    on_click=envoyer_demande,
                                ),
                            ],
                            spacing=15,
                        ),
                    ),
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            )
        )

        page.update()

    def afficher_remboursement():
        print("🔥 ÉCRAN REMBOURSEMENT")

        page.controls.clear()

        resultat = ft.Text("", size=13)

        numero_pret = ft.TextField(
            label="Numéro du prêt",
            prefix_icon=ft.Icons.RECEIPT_LONG,
            border_radius=12,
        )

        montant = ft.TextField(
            label="Montant du remboursement (HTG)",
            prefix_icon=ft.Icons.ATTACH_MONEY,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=12,
        )

        def effectuer_remboursement(e):
            print("🔥 CLIC EFFECTUER REMBOURSEMENT")

            numero = numero_pret.value.strip()
            montant_value = montant.value.strip()

            if not numero or not montant_value:
                resultat.value = "Veuillez remplir tous les champs."
                resultat.color = "#D32F2F"
                page.update()
                return

            try:
                montant_float = float(montant_value)
            except ValueError:
                resultat.value = "Le montant est invalide."
                resultat.color = "#D32F2F"
                page.update()
                return

            if montant_float <= 0:
                resultat.value = "Le montant doit être supérieur à zéro."
                resultat.color = "#D32F2F"
                page.update()
                return

            # Pour l'instant on vérifie uniquement le formulaire.
            # L'appel API sera branché ensuite.
            resultat.value = (
                f"Remboursement de {montant_float:,.2f} HTG "
                f"pour le prêt {numero}."
            )
            resultat.color = GREEN
            page.update()

        page.add(
            ft.Column(
                [
                    ft.Container(
                        bgcolor=BLUE,
                        padding=ft.Padding.only(
                            left=10,
                            right=20,
                            top=20,
                            bottom=20,
                        ),
                        content=ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=ft.Colors.WHITE,
                                    on_click=lambda e: afficher_dashboard(),
                                ),
                                ft.Text(
                                    "Remboursement",
                                    color=ft.Colors.WHITE,
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    expand=True,
                                ),
                            ],
                        ),
                    ),

                    ft.Container(
                        padding=20,
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Effectuer un remboursement",
                                    size=23,
                                    color=TEXT,
                                    weight=ft.FontWeight.BOLD,
                                ),

                                ft.Text(
                                    "Entrez les informations de votre remboursement.",
                                    size=14,
                                    color=GREY,
                                ),

                                ft.Container(height=10),

                                numero_pret,
                                montant,

                                resultat,

                                ft.ElevatedButton(
                                    "Effectuer le remboursement",
                                    icon=ft.Icons.PAYMENT,
                                    width=300,
                                    height=50,
                                    on_click=effectuer_remboursement,
                                ),
                            ],
                            spacing=15,
                        ),
                    ),
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            )
        )

        page.update()

    def afficher_epargne():
        print("🔥 ÉCRAN ÉPARGNE")

        page.controls.clear()

        page.add(
            ft.Column(
                [
                    ft.Container(
                        bgcolor=GREEN,
                        padding=ft.Padding.only(
                            left=10,
                            right=20,
                            top=20,
                            bottom=20,
                        ),
                        content=ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=ft.Colors.WHITE,
                                    on_click=lambda e: afficher_dashboard(),
                                ),
                                ft.Text(
                                    "Épargne",
                                    color=ft.Colors.WHITE,
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    expand=True,
                                ),
                            ],
                        ),
                    ),

                    ft.Container(
                        padding=20,
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Mon épargne",
                                    size=24,
                                    color=TEXT,
                                    weight=ft.FontWeight.BOLD,
                                ),

                                ft.Text(
                                    "Gérez votre épargne GMES.",
                                    size=14,
                                    color=GREY,
                                ),

                                ft.Container(height=20),

                                ft.Container(
                                    width=float("inf"),
                                    padding=25,
                                    bgcolor="#E5F7F1",
                                    border_radius=20,
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "Solde épargne",
                                                size=15,
                                                color=GREY,
                                            ),
                                            ft.Text(
                                                f"{client.get('solde_epargne', 0):,.2f} HTG",
                                                size=30,
                                                color=GREEN,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                        ],
                                        spacing=8,
                                    ),
                                ),

                                ft.Container(height=15),

                                ft.ElevatedButton(
                                    "Déposer dans mon épargne",
                                    icon=ft.Icons.ADD,
                                    width=300,
                                    height=50,
                                    on_click=lambda e: message(
                                        "Dépôt épargne"
                                    ),
                                ),

                                ft.ElevatedButton(
                                    "Retirer de mon épargne",
                                    icon=ft.Icons.REMOVE,
                                    width=300,
                                    height=50,
                                    on_click=lambda e: message(
                                        "Retrait épargne"
                                    ),
                                ),
                            ],
                            spacing=15,
                        ),
                    ),
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            )
        )

        page.update()

    def afficher_transactions():
        print("🔥 ÉCRAN TRANSACTIONS")

        page.controls.clear()

        liste_transactions = ft.Column(
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        liste_transactions.controls.extend(
            [
                transaction_item(
                    ft.Icons.ARROW_DOWNWARD,
                    "Remboursement prêt",
                    "12 sept. 2026",
                    "- 6,200 HTG",
                    "Reçu",
                    "green",
                ),

                transaction_item(
                    ft.Icons.ARROW_UPWARD,
                    "Dépôt épargne",
                    "08 sept. 2026",
                    "+ 2,000 HTG",
                    "Crédité",
                    "green",
                ),

                transaction_item(
                    ft.Icons.CREDIT_CARD,
                    "Retrait guichet",
                    "05 sept. 2026",
                    "- 3,000 HTG",
                    "Effectué",
                    "blue",
                ),
            ]
        )

        page.add(
            ft.Column(
                [
                    ft.Container(
                        bgcolor=PURPLE,
                        padding=ft.Padding.only(
                            left=10,
                            right=20,
                            top=20,
                            bottom=20,
                        ),
                        content=ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=ft.Colors.WHITE,
                                    on_click=lambda e: afficher_dashboard(),
                                ),
                                ft.Text(
                                    "Transactions",
                                    color=ft.Colors.WHITE,
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    expand=True,
                                ),
                            ],
                        ),
                    ),

                    ft.Container(
                        padding=20,
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Historique des transactions",
                                    size=23,
                                    color=TEXT,
                                    weight=ft.FontWeight.BOLD,
                                ),

                                ft.Text(
                                    "Consultez vos opérations récentes.",
                                    size=14,
                                    color=GREY,
                                ),

                                ft.Container(height=10),

                                liste_transactions,
                            ],
                            spacing=10,
                            expand=True,
                        ),
                        expand=True,
                    ),
                ],
                expand=True,
            )
        )

        page.update()

    # ============================================================
    # COULEURS DU PROFIL (à ajouter près de vos autres constantes)
    # ============================================================

    PROFILE_GREEN = "#178754"
    PROFILE_GREEN_LIGHT = "#E7F6EF"
    PROFILE_GREEN_BADGE = "#DFF4E9"
    ROW_ICON_BG = "#F1F3F6"

    # ============================================================
    # PETITS COMPOSANTS RÉUTILISABLES POUR LE PROFIL
    # ============================================================

    def profil_info_row(icon, label, value, is_last=False):
        return ft.Container(
            padding=ft.Padding.symmetric(vertical=12),
            border=(
                None
                if is_last
                else ft.Border.only(bottom=ft.BorderSide(1, "#EDEFF3"))
            ),
            content=ft.Row(
                [
                    ft.Container(
                        width=34,
                        height=34,
                        border_radius=50,
                        bgcolor=ROW_ICON_BG,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(icon, color=GREY, size=17),
                    ),
                    ft.Text(label, size=14, color=GREY, expand=True),
                    ft.Text(
                        value,
                        size=14,
                        color=TEXT,
                        weight=ft.FontWeight.W_600,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
        )

    def profil_status_row(icon, label, statut_texte, is_last=False):
        return ft.Container(
            padding=ft.Padding.symmetric(vertical=12),
            border=(
                None
                if is_last
                else ft.Border.only(bottom=ft.BorderSide(1, "#EDEFF3"))
            ),
            content=ft.Row(
                [
                    ft.Container(
                        width=34,
                        height=34,
                        border_radius=50,
                        bgcolor=ROW_ICON_BG,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(icon, color=GREY, size=17),
                    ),
                    ft.Text(label, size=14, color=GREY, expand=True),
                    ft.Container(
                        bgcolor=PROFILE_GREEN_BADGE,
                        border_radius=20,
                        padding=ft.Padding.symmetric(horizontal=12, vertical=4),
                        content=ft.Text(
                            statut_texte,
                            size=12,
                            color=PROFILE_GREEN,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
        )

    def profil_action_row(icon, label, on_click, is_last=False, danger=False):
        return ft.Container(
            padding=ft.Padding.symmetric(vertical=13),
            on_click=on_click,
            border=(
                None
                if is_last
                else ft.Border.only(bottom=ft.BorderSide(1, "#EDEFF3"))
            ),
            content=ft.Row(
                [
                    ft.Container(
                        width=34,
                        height=34,
                        border_radius=50,
                        bgcolor="#FBE9E9" if danger else PROFILE_GREEN,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            icon,
                            color="#D32F2F" if danger else ft.Colors.WHITE,
                            size=17,
                        ),
                    ),
                    ft.Text(
                        label,
                        size=15,
                        color="#D32F2F" if danger else TEXT,
                        weight=ft.FontWeight.W_500,
                        expand=True,
                    ),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=GREY, size=20),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
        )

    def nav_item(icon, selected_icon, label, selected, on_click):
        return ft.Container(
            padding=ft.Padding.symmetric(horizontal=14, vertical=8),
            border_radius=14,
            bgcolor=PROFILE_GREEN_LIGHT if selected else None,
            on_click=on_click,
            content=ft.Column(
                [
                    ft.Icon(
                        selected_icon if selected else icon,
                        color=PROFILE_GREEN if selected else GREY,
                        size=22,
                    ),
                    ft.Text(
                        label,
                        size=11,
                        color=PROFILE_GREEN if selected else GREY,
                        weight=ft.FontWeight.BOLD if selected else ft.FontWeight.NORMAL,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=3,
            ),
        )

    def deconnecter(e):
        nonlocal token, user, client

        print("👋 DÉCONNEXION GMES")

        token = None
        user = {}
        client = {}

        identifier_field.value = ""
        password_field.value = ""
        error_text.value = ""

        afficher_login()

    # ============================================================
    # ÉCRAN PROFIL
    # ============================================================

    def afficher_profil():

        print("🔥 ÉCRAN PROFIL")

        page.controls.clear()

        # --------------------------------------------------------
        # HEADER
        # --------------------------------------------------------

        header = ft.Container(
            bgcolor=PROFILE_GREEN,
            padding=ft.Padding.only(left=6, right=20, top=18, bottom=18),
            content=ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e: afficher_dashboard(),
                    ),
                    ft.Text(
                        "Mon Profil",
                        color=ft.Colors.WHITE,
                        size=19,
                        weight=ft.FontWeight.BOLD,
                        expand=True,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(width=40),
                ],
            ),
        )

        # --------------------------------------------------------
        # AVATAR + NOM + BADGE
        # --------------------------------------------------------

        nom_complet = (
                          f"{client.get('prenom', '')} {client.get('nom', '')}"
                      ).strip() or "Client GMES"

        entete_profil = ft.Container(
            padding=ft.Padding.only(left=20, right=20, top=20),
            content=ft.Row(
                [
                    ft.Container(
                        width=64,
                        height=64,
                        border_radius=50,
                        bgcolor=PROFILE_GREEN,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            ft.Icons.PERSON,
                            color=ft.Colors.WHITE,
                            size=32,
                        ),
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                nom_complet,
                                size=19,
                                color=TEXT,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Client GMES",
                                size=13,
                                color=GREY,
                            ),
                            ft.Container(
                                margin=ft.Margin.only(top=4),
                                bgcolor=PROFILE_GREEN_BADGE,
                                border_radius=20,
                                padding=ft.Padding.symmetric(
                                    horizontal=12, vertical=4
                                ),
                                content=ft.Row(
                                    [
                                        ft.Icon(
                                            ft.Icons.CHECK_CIRCLE,
                                            color=PROFILE_GREEN,
                                            size=14,
                                        ),
                                        ft.Text(
                                            "Compte actif",
                                            size=12,
                                            color=PROFILE_GREEN,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                    ],
                                    spacing=5,
                                    tight=True,
                                ),
                            ),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=16,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
        )

        # --------------------------------------------------------
        # CARTE SOLDE ÉPARGNE
        # --------------------------------------------------------

        carte_solde = ft.Container(
            margin=ft.Margin.only(left=20, right=20, top=18),
            padding=18,
            bgcolor=PROFILE_GREEN_LIGHT,
            border_radius=18,
            content=ft.Row(
                [
                    ft.Container(
                        width=46,
                        height=46,
                        border_radius=14,
                        bgcolor=ft.Colors.WHITE,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            ft.Icons.SAVINGS,
                            color=PROFILE_GREEN,
                            size=24,
                        ),
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                "Solde du compte épargne",
                                size=13,
                                color="#3E6B57",
                            ),
                            ft.Text(
                                f"{client.get('solde', 0):,.2f} HTG",
                                size=24,
                                color=PROFILE_GREEN,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=14,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        # --------------------------------------------------------
        # CARTE — INFORMATIONS PERSONNELLES
        # --------------------------------------------------------

        carte_infos_perso = ft.Container(
            margin=ft.Margin.only(left=20, right=20, top=18),
            padding=18,
            bgcolor=ft.Colors.WHITE,
            border_radius=18,
            border=ft.Border.all(1, "#EDEFF3"),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.PERSON_OUTLINE, color=TEXT, size=19),
                            ft.Text(
                                "Informations personnelles",
                                size=16,
                                color=TEXT,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=6),
                    profil_info_row(
                        ft.Icons.PERSON_OUTLINE, "Nom complet", nom_complet
                    ),
                    profil_info_row(
                        ft.Icons.EMAIL_OUTLINED,
                        "Email",
                        user.get("email", "-"),
                    ),
                    profil_info_row(
                        ft.Icons.PHONE_OUTLINED,
                        "Téléphone",
                        client.get("telephone", "-"),
                    ),
                    profil_info_row(
                        ft.Icons.BADGE_OUTLINED,
                        "ID client",
                        client.get("id_client", "-"),
                    ),
                    profil_status_row(
                        ft.Icons.SHIELD_OUTLINED,
                        "Statut",
                        client.get("statut", "actif").capitalize(),
                        is_last=True,
                    ),
                ],
                spacing=0,
            ),
        )

        # --------------------------------------------------------
        # CARTE — INFORMATIONS DU COMPTE
        # --------------------------------------------------------

        carte_infos_compte = ft.Container(
            margin=ft.Margin.only(left=20, right=20, top=18),
            padding=18,
            bgcolor=ft.Colors.WHITE,
            border_radius=18,
            border=ft.Border.all(1, "#EDEFF3"),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.ACCOUNT_BALANCE_OUTLINED,
                                color=TEXT,
                                size=19,
                            ),
                            ft.Text(
                                "Informations du compte",
                                size=16,
                                color=TEXT,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=6),
                    profil_info_row(
                        ft.Icons.CREDIT_CARD_OUTLINED,
                        "Numéro de compte",
                        client.get("numero_compte", "-"),
                    ),
                    profil_info_row(
                        ft.Icons.SAVINGS_OUTLINED,
                        "Type de compte",
                        "Épargne",
                    ),
                    profil_info_row(
                        ft.Icons.LOCATION_ON_OUTLINED,
                        "Succursale",
                        client.get("succursale_nom", "-"),
                        is_last=True,
                    ),
                ],
                spacing=0,
            ),
        )

        # --------------------------------------------------------
        # CARTE — ACTIONS
        # --------------------------------------------------------

        carte_actions = ft.Container(
            margin=ft.Margin.only(left=20, right=20, top=18, bottom=20),
            padding=ft.Padding.symmetric(horizontal=6, vertical=6),
            bgcolor=ft.Colors.WHITE,
            border_radius=18,
            border=ft.Border.all(1, "#EDEFF3"),
            content=ft.Column(
                [
                    profil_action_row(
                        ft.Icons.PERSON_OUTLINE,
                        "Modifier mes informations",
                        lambda e: message("Modifier mes informations"),
                    ),
                    profil_action_row(
                        ft.Icons.LOCK_OUTLINE,
                        "Changer mon mot de passe",
                        lambda e: message("Changer mon mot de passe"),
                    ),
                    profil_action_row(
                        ft.Icons.DESCRIPTION_OUTLINED,
                        "Historique de mes opérations",
                        lambda e: message("Historique de mes opérations"),
                    ),
                    profil_action_row(
                        ft.Icons.LOGOUT,
                        "Se déconnecter",
                        lambda e: deconnecter(e),
                        is_last=True,
                        danger=True,
                    ),
                ],
                spacing=0,
            ),
        )

        # --------------------------------------------------------
        # BARRE DE NAVIGATION
        # --------------------------------------------------------

        barre_navigation = ft.Container(
            padding=ft.Padding.symmetric(horizontal=10, vertical=10),
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.only(top=ft.BorderSide(1, "#EDEFF3")),
            content=ft.Row(
                [
                    nav_item(
                        ft.Icons.HOME_OUTLINED, ft.Icons.HOME,
                        "Accueil", False,
                        lambda e: afficher_dashboard(),
                    ),
                    nav_item(
                        ft.Icons.ATTACH_MONEY_OUTLINED, ft.Icons.ATTACH_MONEY,
                        "Prêt", False,
                        lambda e: message("Prêt"),
                    ),
                    nav_item(
                        ft.Icons.CREDIT_CARD_OUTLINED, ft.Icons.CREDIT_CARD,
                        "Paiement", False,
                        lambda e: message("Paiement"),
                    ),
                    nav_item(
                        ft.Icons.PERSON_OUTLINE, ft.Icons.PERSON,
                        "Profil", True,
                        lambda e: None,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
        )

        # --------------------------------------------------------
        # ASSEMBLAGE
        # --------------------------------------------------------

        page.add(
            ft.Column(
                [
                    header,
                    ft.Column(
                        [
                            entete_profil,
                            carte_solde,
                            carte_infos_perso,
                            carte_infos_compte,
                            carte_actions,
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                        spacing=0,
                    ),
                    barre_navigation,
                ],
                expand=True,
                spacing=0,
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
                                on_click=afficher_notifications,
                            ),
                            ft.Container(
                                width=18,
                                height=18,
                                right=4,
                                top=4,
                                border_radius=50,
                                bgcolor="#E53935",
                                alignment=ft.Alignment.CENTER,
                                content=ft.Text( str(nombre_notifications_non_lues), size=10, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
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
                                f"{client.get('solde_epargne', 0):,.2f} HTG",
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

        # ============================================================
        # ACTIONS
        # ============================================================

        def cliquer_demande_pret(e):
            print("🔥 CLIC DEMANDE DE PRÊT")
            afficher_demande_pret()

        actions = ft.Container(
            margin=ft.Margin.only(
                left=20,
                right=20,
                top=18
            ),
            content=ft.Row(
                [
                    action_button(
                        ft.Icons.DESCRIPTION,
                        "Demander\nun prêt",
                        "#0874E8",
                        cliquer_demande_pret
                    ),

                    action_button(
                        ft.Icons.CREDIT_CARD,
                        "Rembourser",
                        "#E5A817",
                        lambda e: afficher_remboursement()
                    ),

                    action_button(
                        ft.Icons.SAVINGS,
                        "Épargne",
                        GREEN,
                        lambda e: afficher_epargne()
                    ),

                    action_button(
                        ft.Icons.SWAP_HORIZ,
                        "Transactions",
                        PURPLE,
                        lambda e: afficher_transactions()
                    ),
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

            on_change=lambda e: (
                afficher_dashboard()
                if e.control.selected_index == 0
                else afficher_demande_pret()
                if e.control.selected_index == 1
                else afficher_remboursement()
                if e.control.selected_index == 2
                else afficher_profil()
            ),

            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.HOME_OUTLINED,
                    selected_icon=ft.Icons.HOME,
                    label="Accueil",
                ),

                ft.NavigationBarDestination(
                    icon=ft.Icons.DESCRIPTION_OUTLINED,
                    selected_icon=ft.Icons.DESCRIPTION,
                    label="Prêts",
                ),

                ft.NavigationBarDestination(
                    icon=ft.Icons.SWAP_HORIZ_OUTLINED,
                    selected_icon=ft.Icons.SWAP_HORIZ,
                    label="Paiements",
                ),

                ft.NavigationBarDestination(
                    icon=ft.Icons.PERSON_OUTLINE,
                    selected_icon=ft.Icons.PERSON,
                    label="Profil",
                ),
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