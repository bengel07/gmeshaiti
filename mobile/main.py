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
    photo_profil_path = None  # 👈 AJOUT

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
                    f"{API_URL}/api/mobile/demande-pret",
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

    def afficher_transfert():
        print("🔥 ÉCRAN TRANSFERT")

        page.controls.clear()

        resultat = ft.Text("", size=13)

        destinataire = ft.TextField(
            label="Numéro de compte du destinataire",
            prefix_icon=ft.Icons.PERSON_OUTLINE,
            border_radius=12,
        )

        montant = ft.TextField(
            label="Montant du transfert (HTG)",
            prefix_icon=ft.Icons.ATTACH_MONEY,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=12,
        )

        motif = ft.TextField(
            label="Motif du transfert (facultatif)",
            prefix_icon=ft.Icons.DESCRIPTION_OUTLINED,
            border_radius=12,
        )

        def effectuer_transfert(e):
            numero = destinataire.value.strip()
            montant_value = montant.value.strip()
            motif_value = motif.value.strip()

            if not numero or not montant_value:
                resultat.value = "Veuillez remplir tous les champs obligatoires."
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

            if not token:
                resultat.value = "Session expirée. Veuillez vous reconnecter."
                resultat.color = "#D32F2F"
                page.update()
                return

            try:
                response = requests.post(
                    f"{API_URL}/api/mobile/transfert",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                    },
                    json={
                        "numero_compte_destinataire": numero,
                        "montant": montant_float,
                        "motif": motif_value,
                    },
                    timeout=30,
                )

                print("================================")
                print("TRANSFERT")
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
                        "Transfert effectué avec succès."
                    )
                    resultat.color = GREEN

                    montant.value = ""
                    motif.value = ""

                    page.update()

                    # Recharge les informations du client
                    try:
                        me_response = requests.get(
                            f"{API_URL}/auth/api/mobile/client/me",
                            headers={
                                "Authorization": f"Bearer {token}",
                                "Accept": "application/json",
                            },
                            timeout=30,
                        )

                        if me_response.status_code == 200:
                            me_data = me_response.json()

                            if me_data.get("success"):
                                client.clear()
                                client.update(
                                    me_data.get("client") or {}
                                )

                    except Exception as ex:
                        print(
                            "⚠️ Impossible de rafraîchir le solde :",
                            repr(ex)
                        )

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
                print("❌ ERREUR TRANSFERT :", repr(ex))
                resultat.value = "Une erreur est survenue."
                resultat.color = "#D32F2F"
                page.update()

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
                                    on_click=lambda e: afficher_epargne(),
                                ),

                                ft.Text(
                                    "Transfert",
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
                                    "Transférer de l'argent",
                                    size=24,
                                    color=TEXT,
                                    weight=ft.FontWeight.BOLD,
                                ),

                                ft.Text(
                                    "Envoyez de l'argent vers un autre compte GMES.",
                                    size=14,
                                    color=GREY,
                                ),

                                ft.Container(height=15),

                                ft.Container(
                                    padding=20,
                                    bgcolor="#F0EDFF",
                                    border_radius=18,
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "Solde disponible",
                                                size=14,
                                                color=GREY,
                                            ),

                                            ft.Text(
                                                f"{client.get('solde', 0):,.2f} HTG",
                                                size=28,
                                                color=PURPLE,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                        ],
                                        spacing=5,
                                    ),
                                ),

                                ft.Container(height=10),

                                destinataire,
                                montant,
                                motif,

                                resultat,

                                ft.ElevatedButton(
                                    "Envoyer le transfert",
                                    icon=ft.Icons.SEND,
                                    width=300,
                                    height=50,
                                    on_click=effectuer_transfert,
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

                                ft.ElevatedButton(
                                    "Transférer de l'argent",
                                    icon=ft.Icons.SEND,
                                    width=300,
                                    height=50,
                                    on_click=lambda e: afficher_transfert(),
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

    # ============================================================
    # AVATAR DE PROFIL RÉUTILISABLE
    # ============================================================

    def creer_avatar_profil(taille=64, taille_icone=32):
        """
        Retourne un Container contenant :
        - la photo du client si elle existe
        - sinon une icône PERSON par défaut
        """

        url_photo = (
            client.get("photo_url")
            or client.get("photo")
            or photo_profil_path
        )

        if url_photo:
            contenu = ft.Image(
                src=url_photo,
                width=taille,
                height=taille,
                fit=ft.ImageFit.COVER,
                border_radius=ft.BorderRadius.all(taille / 2),
            )
            bgcolor = None
        else:
            contenu = ft.Icon(
                ft.Icons.PERSON,
                color=ft.Colors.WHITE,
                size=taille_icone,
            )
            bgcolor = PROFILE_GREEN

        return ft.Container(
            width=taille,
            height=taille,
            border_radius=taille / 2,
            bgcolor=bgcolor,
            alignment=ft.Alignment.CENTER,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=contenu,
        )

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
                    creer_avatar_profil(taille=64, taille_icone=32),


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
                        lambda e: afficher_modifier_profil(),
                    ),
                    profil_action_row(
                        ft.Icons.LOCK_OUTLINE,
                        "Changer mon mot de passe",
                        lambda e: afficher_changer_mot_de_passe(),
                    ),
                    profil_action_row(
                        ft.Icons.DESCRIPTION_OUTLINED,
                        "Historique de mes opérations",
                        lambda e: afficher_historique_operations(),
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



    def afficher_modifier_profil():
        print("🔥 ÉCRAN MODIFIER MON PROFIL")

        page.controls.clear()

        # ============================================================
        # PHOTO DE PROFIL
        # ============================================================

        photo_selectionnee = {
            "path": None
        }

        # ------------------------------------------------------------
        # APERÇU PHOTO
        # ------------------------------------------------------------

        # ------------------------------------------------------------
        # APERÇU PHOTO (dynamique)
        # ------------------------------------------------------------

        def creer_contenu_apercu():
            url = client.get("photo_url") or photo_profil_path
            if url:
                return ft.Image(
                    src=url,
                    width=110,
                    height=110,
                    fit=ft.ImageFit.COVER,
                    border_radius=ft.BorderRadius.all(55),
                )
            return ft.Icon(
                ft.Icons.PERSON,
                color=BLUE,
                size=55,
            )

        photo_preview = ft.Container(
            width=110,
            height=110,
            border_radius=55,
            bgcolor="#EAF2FF",
            alignment=ft.Alignment.CENTER,
            border=ft.Border.all(
                5,
                ft.Colors.WHITE,
            ),
            shadow=ft.BoxShadow(
                blur_radius=12,
                spread_radius=1,
                color="#25000000",
            ),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=creer_contenu_apercu(),
        )

        # ============================================================
        # FILE PICKER
        # ============================================================

        def photo_selectionnee_result(e):

            if not e.files:
                return

            fichier = e.files[0]

            photo_selectionnee["path"] = fichier.path

            print("📷 PHOTO SÉLECTIONNÉE :", fichier.path)

            photo_preview.content = ft.Image(
                src=fichier.path,
                width=110,
                height=110,
                fit=ft.ImageFit.COVER,
                border_radius=ft.BorderRadius.all(55),
            )

            page.update()

        file_picker = ft.FilePicker()

        file_picker.on_result = photo_selectionnee_result

        page.services.append(file_picker)  # ✅ Utilise services au lieu de overlay

        # ============================================================
        # MODIFIER PHOTO
        # ============================================================

        async def modifier_photo(e):
            print("📷 CLIC MODIFIER PHOTO")

            fichiers = await file_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=["jpg", "jpeg", "png"],
            )

            if not fichiers:
                return

            fichier = fichiers[0]

            photo_selectionnee["path"] = fichier.path
            client["photo_url"] = fichier.path

            print("📷 PHOTO SÉLECTIONNÉE :", fichier.path)

            photo_preview.content = ft.Image(
                src=fichier.path,
                width=110,
                height=110,
                fit=ft.ImageFit.COVER,
                border_radius=ft.BorderRadius.all(55),
            )

            page.update()

        # ============================================================
        # CHAMPS
        # ============================================================

        prenom_field = ft.TextField(
            label="Prénom",
            value=client.get("prenom", "") or "",
            prefix_icon=ft.Icons.PERSON_OUTLINE,
            border_radius=14,
            border_color="#D4E0F5",
            focused_border_color=BLUE,
            text_size=16,
            color=TEXT,
        )

        nom_field = ft.TextField(
            label="Nom",
            value=client.get("nom", "") or "",
            prefix_icon=ft.Icons.PERSON_OUTLINE,
            border_radius=14,
            border_color="#D4E0F5",
            focused_border_color=BLUE,
            text_size=16,
            color=TEXT,
        )

        telephone_field = ft.TextField(
            label="Téléphone",
            value=client.get("telephone", "") or "",
            prefix_icon=ft.Icons.PHONE_OUTLINED,
            keyboard_type=ft.KeyboardType.PHONE,
            border_radius=14,
            border_color="#D4E0F5",
            focused_border_color=BLUE,
            text_size=16,
            color=TEXT,
        )

        email_field = ft.TextField(
            label="Email",
            value=(
                    user.get("email", "")
                    or client.get("email", "")
                    or ""
            ),
            prefix_icon=ft.Icons.EMAIL_OUTLINED,
            keyboard_type=ft.KeyboardType.EMAIL,
            border_radius=14,
            border_color="#D4E0F5",
            focused_border_color=BLUE,
            text_size=16,
            color=TEXT,
        )

        resultat = ft.Text(
            "",
            size=13,
            text_align=ft.TextAlign.CENTER,
        )

        # ============================================================
        # ENREGISTRER
        # ============================================================

        def enregistrer_modifications(e):

            print("💾 ENREGISTREMENT PROFIL")

            if not token:
                resultat.value = (
                    "Session expirée. Veuillez vous reconnecter."
                )

                resultat.color = "#D32F2F"

                page.update()

                return

            prenom = prenom_field.value.strip()
            nom = nom_field.value.strip()
            telephone = telephone_field.value.strip()
            email = email_field.value.strip()

            # --------------------------------------------------------
            # VALIDATION
            # --------------------------------------------------------

            if not prenom:
                resultat.value = "Le prénom est obligatoire."
                resultat.color = "#D32F2F"

                page.update()

                return

            if not nom:
                resultat.value = "Le nom est obligatoire."
                resultat.color = "#D32F2F"

                page.update()

                return

            if not telephone:
                resultat.value = "Le numéro de téléphone est obligatoire."
                resultat.color = "#D32F2F"

                page.update()

                return

            if not email:
                resultat.value = "L'adresse email est obligatoire."
                resultat.color = "#D32F2F"

                page.update()

                return

            # --------------------------------------------------------
            # POUR L'INSTANT :
            # MISE À JOUR LOCALE
            #
            # L'API sera branchée ensuite.
            # --------------------------------------------------------

            client["prenom"] = prenom
            client["nom"] = nom
            client["telephone"] = telephone
            client["email"] = email

            user["email"] = email

            resultat.value = (
                "✓ Vos informations ont été mises à jour."
            )

            resultat.color = PROFILE_GREEN

            print("✅ PROFIL MIS À JOUR LOCALEMENT")

            page.update()

        # ============================================================
        # HEADER
        # ============================================================

        header = ft.Container(
            bgcolor=BLUE,
            padding=ft.Padding.only(
                left=8,
                right=15,
                top=18,
                bottom=18,
            ),
            border_radius=ft.BorderRadius.only(
                bottom_left=20,
                bottom_right=20,
            ),
            content=ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.WHITE,
                        icon_size=30,
                        on_click=lambda e: afficher_profil(),
                    ),

                    ft.Text(
                        "Modifier mon profil",
                        color=ft.Colors.WHITE,
                        size=21,
                        weight=ft.FontWeight.BOLD,
                        expand=True,
                        text_align=ft.TextAlign.CENTER,
                    ),

                    # Équilibre visuel avec le bouton retour
                    ft.Container(
                        width=45,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        # ============================================================
        # AVATAR + NOM
        # ============================================================

        avatar_section = ft.Container(
            padding=ft.Padding.only(
                top=25,
                bottom=20,
            ),
            content=ft.Column(
                [
                    # ------------------------------------------------
                    # AVATAR + CAMÉRA
                    # ------------------------------------------------

                    ft.Stack(
                        [
                            photo_preview,

                            ft.Container(
                                width=38,
                                height=38,
                                right=-2,
                                bottom=0,
                                border_radius=19,
                                bgcolor=BLUE,
                                alignment=ft.Alignment.CENTER,
                                border=ft.Border.all(
                                    3,
                                    ft.Colors.WHITE,
                                ),
                                content=ft.IconButton(
                                    icon=ft.Icons.CAMERA_ALT,
                                    icon_color=ft.Colors.WHITE,
                                    icon_size=19,
                                    tooltip="Modifier la photo",
                                    on_click=modifier_photo,
                                ),
                            ),
                        ],
                        width=118,
                        height=118,
                    ),

                    ft.Container(height=8),

                    # ------------------------------------------------
                    # NOM COMPLET
                    # ------------------------------------------------

                    ft.Text(
                        (
                            f"{client.get('prenom', '')} "
                            f"{client.get('nom', '')}"
                        ).strip() or "Client GMES",
                        size=25,
                        color=TEXT,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),

                    ft.Text(
                        "Client GMES",
                        size=16,
                        color=GREY,
                        text_align=ft.TextAlign.CENTER,
                    ),

                    ft.TextButton(
                        "Modifier la photo",
                        icon=ft.Icons.CAMERA_ALT,
                        on_click=modifier_photo,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=3,
            ),
        )

        # ============================================================
        # TITRE INFORMATIONS PERSONNELLES
        # ============================================================

        titre_formulaire = ft.Row(
            [
                ft.Icon(
                    ft.Icons.PERSON_OUTLINE,
                    color=BLUE,
                    size=30,
                ),

                ft.Text(
                    "Informations personnelles",
                    size=21,
                    color=TEXT,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # ============================================================
        # FORMULAIRE
        # ============================================================

        formulaire = ft.Container(
            margin=ft.Margin.only(
                left=20,
                right=20,
            ),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=22,
            border=ft.Border.all(
                1,
                "#E5EAF2",
            ),
            shadow=ft.BoxShadow(
                blur_radius=10,
                spread_radius=1,
                color="#12000000",
            ),
            content=ft.Column(
                [
                    titre_formulaire,

                    ft.Container(height=8),

                    prenom_field,

                    nom_field,

                    telephone_field,

                    email_field,

                    ft.Container(height=5),

                    resultat,

                    # ------------------------------------------------
                    # BOUTON ENREGISTRER
                    # ------------------------------------------------

                    ft.Container(
                        height=55,
                        border_radius=15,
                        bgcolor=PROFILE_GREEN,
                        content=ft.ElevatedButton(
                            "Enregistrer les modifications",
                            icon=ft.Icons.SAVE_OUTLINED,
                            on_click=enregistrer_modifications,
                            style=ft.ButtonStyle(
                                bgcolor=PROFILE_GREEN,
                                color=ft.Colors.WHITE,
                                shape=ft.RoundedRectangleBorder(
                                    radius=15,
                                ),
                            ),
                        ),
                    ),
                ],
                spacing=14,
            ),
        )

        # ============================================================
        # INFORMATION COMPTE
        # ============================================================

        information_compte = ft.Container(
            margin=ft.Margin.only(
                left=20,
                right=20,
                top=18,
                bottom=25,
            ),
            padding=17,
            bgcolor="#EAF3FF",
            border_radius=18,
            content=ft.Row(
                [
                    ft.Container(
                        width=42,
                        height=42,
                        border_radius=21,
                        bgcolor="#D6E8FF",
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            ft.Icons.INFO_OUTLINE,
                            color=BLUE,
                            size=25,
                        ),
                    ),

                    ft.Text(
                        "Votre numéro de compte et votre ID client "
                        "ne peuvent pas être modifiés depuis cette page.",
                        size=13,
                        color=BLUE,
                        weight=ft.FontWeight.W_500,
                        expand=True,
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        # ============================================================
        # PAGE COMPLÈTE
        # ============================================================

        page.add(
            ft.Column(
                [
                    header,

                    ft.Column(
                        [
                            avatar_section,

                            formulaire,

                            information_compte,
                        ],
                        spacing=0,
                    ),
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                spacing=0,
            )
        )

        page.update()



    def afficher_changer_mot_de_passe():
        print("🔥 ÉCRAN CHANGER MOT DE PASSE")

        page.controls.clear()

        # ============================================================
        # CHAMPS
        # ============================================================

        ancien_mot_de_passe = ft.TextField(
            label="Mot de passe actuel",
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            password=True,
            can_reveal_password=True,
            border_radius=14,
            border_color="#D4E0F5",
            focused_border_color=BLUE,
            text_size=16,
        )

        nouveau_mot_de_passe = ft.TextField(
            label="Nouveau mot de passe",
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            password=True,
            can_reveal_password=True,
            border_radius=14,
            border_color="#D4E0F5",
            focused_border_color=BLUE,
            text_size=16,
        )

        confirmer_mot_de_passe = ft.TextField(
            label="Confirmer le nouveau mot de passe",
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            password=True,
            can_reveal_password=True,
            border_radius=14,
            border_color="#D4E0F5",
            focused_border_color=BLUE,
            text_size=16,
        )

        resultat = ft.Text(
            "",
            size=13,
            text_align=ft.TextAlign.CENTER,
        )

        # ============================================================
        # CHANGER LE MOT DE PASSE
        # ============================================================

        def changer_mot_de_passe(e):

            print("🔐 CLIC CHANGER MOT DE PASSE")

            ancien = ancien_mot_de_passe.value.strip()
            nouveau = nouveau_mot_de_passe.value.strip()
            confirmation = confirmer_mot_de_passe.value.strip()

            # --------------------------------------------------------
            # SESSION
            # --------------------------------------------------------

            if not token:
                resultat.value = (
                    "Session expirée. Veuillez vous reconnecter."
                )
                resultat.color = "#D32F2F"
                page.update()
                return

            # --------------------------------------------------------
            # VALIDATION
            # --------------------------------------------------------

            if not ancien:
                resultat.value = "Entrez votre mot de passe actuel."
                resultat.color = "#D32F2F"
                page.update()
                return

            if not nouveau:
                resultat.value = "Entrez votre nouveau mot de passe."
                resultat.color = "#D32F2F"
                page.update()
                return

            if not confirmation:
                resultat.value = (
                    "Confirmez votre nouveau mot de passe."
                )
                resultat.color = "#D32F2F"
                page.update()
                return

            if len(nouveau) < 8:
                resultat.value = (
                    "Le nouveau mot de passe doit contenir "
                    "au moins 8 caractères."
                )
                resultat.color = "#D32F2F"
                page.update()
                return

            if nouveau != confirmation:
                resultat.value = (
                    "Les deux nouveaux mots de passe ne correspondent pas."
                )
                resultat.color = "#D32F2F"
                page.update()
                return

            if ancien == nouveau:
                resultat.value = (
                    "Le nouveau mot de passe doit être différent "
                    "de l'ancien."
                )
                resultat.color = "#D32F2F"
                page.update()
                return

            # ========================================================
            # API
            # ========================================================
            #
            # Cette partie sera branchée sur la vraie route Flask.
            #
            # NE PAS modifier le mot de passe localement.
            # Le serveur doit vérifier l'ancien mot de passe
            # et enregistrer le nouveau.
            # ========================================================

            try:

                response = requests.post(
                    f"{API_URL}/auth/api/mobile/change-password",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                    },
                    json={
                        "ancien_mot_de_passe": ancien,
                        "nouveau_mot_de_passe": nouveau,
                    },
                    timeout=30,
                )

                print("================================")
                print("CHANGEMENT MOT DE PASSE")
                print("STATUT :", response.status_code)
                print("REPONSE :", response.text[:2000])
                print("================================")

                try:
                    data = response.json()
                except Exception:
                    data = {}

                if response.status_code == 200 and data.get("success"):
                    resultat.value = (
                        "✓ Votre mot de passe a été modifié avec succès."
                    )
                    resultat.color = PROFILE_GREEN

                    ancien_mot_de_passe.value = ""
                    nouveau_mot_de_passe.value = ""
                    confirmer_mot_de_passe.value = ""

                    page.update()

                    return

                resultat.value = data.get(
                    "error",
                    data.get(
                        "message",
                        f"Erreur serveur ({response.status_code})"
                    ),
                )

                resultat.color = "#D32F2F"

                page.update()

            except requests.exceptions.Timeout:

                resultat.value = (
                    "Le serveur GMES ne répond pas."
                )

                resultat.color = "#D32F2F"

                page.update()

            except requests.exceptions.ConnectionError:

                resultat.value = (
                    "Impossible de contacter le serveur GMES."
                )

                resultat.color = "#D32F2F"

                page.update()

            except Exception as ex:

                print(
                    "❌ ERREUR CHANGEMENT MOT DE PASSE :",
                    repr(ex),
                )

                resultat.value = (
                    "Une erreur est survenue."
                )

                resultat.color = "#D32F2F"

                page.update()

        # ============================================================
        # HEADER
        # ============================================================

        header = ft.Container(
            bgcolor=BLUE,
            padding=ft.Padding.only(
                left=8,
                right=15,
                top=18,
                bottom=18,
            ),
            border_radius=ft.BorderRadius.only(
                bottom_left=20,
                bottom_right=20,
            ),
            content=ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.WHITE,
                        icon_size=30,
                        on_click=lambda e: afficher_profil(),
                    ),

                    ft.Text(
                        "Changer mon mot de passe",
                        color=ft.Colors.WHITE,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        expand=True,
                        text_align=ft.TextAlign.CENTER,
                    ),

                    ft.Container(
                        width=45,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        # ============================================================
        # INTRODUCTION
        # ============================================================

        introduction = ft.Container(
            padding=ft.Padding.only(
                top=30,
                bottom=20,
                left=20,
                right=20,
            ),
            content=ft.Column(
                [
                    ft.Container(
                        width=85,
                        height=85,
                        border_radius=43,
                        bgcolor="#EAF2FF",
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            ft.Icons.LOCK_OUTLINE,
                            color=BLUE,
                            size=45,
                        ),
                    ),

                    ft.Container(height=8),

                    ft.Text(
                        "Sécurité du compte",
                        size=24,
                        color=TEXT,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),

                    ft.Text(
                        "Modifiez votre mot de passe pour "
                        "sécuriser votre compte GMES.",
                        size=14,
                        color=GREY,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=7,
            ),
        )

        # ============================================================
        # FORMULAIRE
        # ============================================================

        formulaire = ft.Container(
            margin=ft.Margin.only(
                left=20,
                right=20,
            ),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=22,
            border=ft.Border.all(
                1,
                "#E5EAF2",
            ),
            shadow=ft.BoxShadow(
                blur_radius=10,
                spread_radius=1,
                color="#12000000",
            ),
            content=ft.Column(
                [
                    ft.Text(
                        "Modifier le mot de passe",
                        size=19,
                        color=TEXT,
                        weight=ft.FontWeight.BOLD,
                    ),

                    ft.Container(height=5),

                    ancien_mot_de_passe,

                    nouveau_mot_de_passe,

                    confirmer_mot_de_passe,

                    # ------------------------------------------------
                    # CONSEILS
                    # ------------------------------------------------

                    ft.Container(
                        padding=15,
                        bgcolor="#F5F8FF",
                        border_radius=15,
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Conseils de sécurité",
                                    size=14,
                                    color=BLUE,
                                    weight=ft.FontWeight.BOLD,
                                ),

                                ft.Text(
                                    "• Au moins 8 caractères",
                                    size=12,
                                    color=GREY,
                                ),

                                ft.Text(
                                    "• Utilisez un mot de passe différent "
                                    "de l'ancien",
                                    size=12,
                                    color=GREY,
                                ),
                            ],
                            spacing=5,
                        ),
                    ),

                    resultat,

                    # ------------------------------------------------
                    # BOUTON
                    # ------------------------------------------------

                    ft.Container(
                        height=55,
                        border_radius=15,
                        bgcolor=BLUE,
                        content=ft.ElevatedButton(
                            "Modifier le mot de passe",
                            icon=ft.Icons.LOCK_RESET,
                            on_click=changer_mot_de_passe,
                            style=ft.ButtonStyle(
                                bgcolor=BLUE,
                                color=ft.Colors.WHITE,
                                shape=ft.RoundedRectangleBorder(
                                    radius=15,
                                ),
                            ),
                        ),
                    ),
                ],
                spacing=14,
            ),
        )

        # ============================================================
        # INFORMATION
        # ============================================================

        information = ft.Container(
            margin=ft.Margin.only(
                left=20,
                right=20,
                top=18,
                bottom=25,
            ),
            padding=17,
            bgcolor="#EAF3FF",
            border_radius=18,
            content=ft.Row(
                [
                    ft.Container(
                        width=42,
                        height=42,
                        border_radius=21,
                        bgcolor="#D6E8FF",
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            ft.Icons.INFO_OUTLINE,
                            color=BLUE,
                            size=25,
                        ),
                    ),

                    ft.Text(
                        "Après la modification, utilisez votre "
                        "nouveau mot de passe pour vous connecter "
                        "à GMES.",
                        size=13,
                        color=BLUE,
                        expand=True,
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        # ============================================================
        # AFFICHAGE
        # ============================================================

        page.add(
            ft.Column(
                [
                    header,

                    ft.Column(
                        [
                            introduction,
                            formulaire,
                            information,
                        ],
                        spacing=0,
                    ),
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                spacing=0,
            )
        )

        page.update()

    def afficher_historique_operations():
        print("🔥 ÉCRAN HISTORIQUE DES OPÉRATIONS")

        page.controls.clear()

        # ============================================================
        # DONNÉES DES OPÉRATIONS
        # ============================================================

        operations = [
            {
                "type": "transfert_envoye",
                "titre": "Transfert envoyé",
                "description": "Vers : 7-12519-1234567890",
                "date": "20 sept. 2026",
                "montant": -5000,
                "statut": "Effectué",
            },
            {
                "type": "transfert_recu",
                "titre": "Transfert reçu",
                "description": "De : 7-12519-9876543210",
                "date": "18 sept. 2026",
                "montant": 8000,
                "statut": "Reçu",
            },
            {
                "type": "remboursement",
                "titre": "Remboursement prêt",
                "description": "Prêt : GMES_Pret-20260912-66403",
                "date": "15 sept. 2026",
                "montant": -6200,
                "statut": "Effectué",
            },
            {
                "type": "depot_epargne",
                "titre": "Dépôt épargne",
                "description": "Compte épargne",
                "date": "12 sept. 2026",
                "montant": 2000,
                "statut": "Crédité",
            },
            {
                "type": "retrait_epargne",
                "titre": "Retrait épargne",
                "description": "Compte épargne",
                "date": "08 sept. 2026",
                "montant": -3000,
                "statut": "Effectué",
            },
            {
                "type": "transfert_recu",
                "titre": "Transfert reçu",
                "description": "De : 7-12519-5555555555",
                "date": "28 août 2026",
                "montant": 4500,
                "statut": "Reçu",
            },
        ]

        # ============================================================
        # VARIABLES POUR LES FILTRES
        # ============================================================

        filtre_actuel = "Toutes"

        # ============================================================
        # LISTE DES OPÉRATIONS
        # ============================================================

        liste_operations = ft.Column(
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        # ============================================================
        # ICÔNE ET COULEUR SELON LE TYPE
        # ============================================================

        def configuration_operation(operation):

            type_operation = operation.get("type")

            if type_operation == "transfert_envoye":
                return (
                    ft.Icons.ARROW_UPWARD,
                    "#E5A817",
                    "#FFF6D9",
                )

            if type_operation == "transfert_recu":
                return (
                    ft.Icons.ARROW_DOWNWARD,
                    GREEN,
                    "#DDF6E5",
                )

            if type_operation == "remboursement":
                return (
                    ft.Icons.CREDIT_CARD,
                    "#D32F2F",
                    "#FBE9E9",
                )

            if type_operation == "depot_epargne":
                return (
                    ft.Icons.SAVINGS,
                    GREEN,
                    "#DDF6E5",
                )

            if type_operation == "retrait_epargne":
                return (
                    ft.Icons.SAVINGS_OUTLINED,
                    "#D32F2F",
                    "#FBE9E9",
                )

            return (
                ft.Icons.RECEIPT_LONG,
                BLUE,
                "#EAF2FF",
            )

        # ============================================================
        # AFFICHER LES OPÉRATIONS
        # ============================================================

        def afficher_liste():

            liste_operations.controls.clear()

            if filtre_actuel == "Toutes":

                operations_filtrees = operations

            elif filtre_actuel == "Prêts":

                operations_filtrees = [
                    operation
                    for operation in operations
                    if operation.get("type") == "remboursement"
                ]

            elif filtre_actuel == "Épargne":

                operations_filtrees = [
                    operation
                    for operation in operations
                    if operation.get("type")
                       in (
                           "depot_epargne",
                           "retrait_epargne",
                       )
                ]

            elif filtre_actuel == "Transferts":

                operations_filtrees = [
                    operation
                    for operation in operations
                    if operation.get("type")
                       in (
                           "transfert_envoye",
                           "transfert_recu",
                       )
                ]

            else:

                operations_filtrees = operations

            if not operations_filtrees:
                liste_operations.controls.append(
                    ft.Container(
                        padding=40,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Column(
                            [
                                ft.Icon(
                                    ft.Icons.RECEIPT_LONG_OUTLINED,
                                    size=55,
                                    color=GREY,
                                ),

                                ft.Text(
                                    "Aucune opération",
                                    size=18,
                                    color=TEXT,
                                    weight=ft.FontWeight.BOLD,
                                ),

                                ft.Text(
                                    "Aucune opération ne correspond "
                                    "à ce filtre.",
                                    size=13,
                                    color=GREY,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                            horizontal_alignment=(
                                ft.CrossAxisAlignment.CENTER
                            ),
                            spacing=8,
                        ),
                    )
                )

                page.update()
                return

            # --------------------------------------------------------
            # CRÉER LES CARTES
            # --------------------------------------------------------

            for operation in operations_filtrees:

                icone, couleur, couleur_fond = (
                    configuration_operation(operation)
                )

                montant_operation = operation.get(
                    "montant",
                    0,
                )

                # ----------------------------------------------------
                # SIGNE
                # ----------------------------------------------------

                if montant_operation >= 0:
                    signe = "+"
                    couleur_montant = GREEN
                else:
                    signe = "-"
                    couleur_montant = "#D32F2F"

                montant_affiche = (
                    f"{signe} "
                    f"{abs(montant_operation):,.2f} HTG"
                )

                # ----------------------------------------------------
                # OPÉRATION
                # ----------------------------------------------------

                liste_operations.controls.append(
                    ft.Container(
                        padding=ft.Padding.symmetric(
                            vertical=13,
                        ),
                        border=ft.Border.only(
                            bottom=ft.BorderSide(
                                1,
                                "#E5EAF2",
                            )
                        ),
                        content=ft.Row(
                            [
                                # ------------------------------------
                                # ICÔNE
                                # ------------------------------------

                                ft.Container(
                                    width=48,
                                    height=48,
                                    border_radius=24,
                                    bgcolor=couleur_fond,
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Icon(
                                        icone,
                                        color=couleur,
                                        size=23,
                                    ),
                                ),

                                # ------------------------------------
                                # DESCRIPTION
                                # ------------------------------------

                                ft.Column(
                                    [
                                        ft.Text(
                                            operation.get(
                                                "titre",
                                                "Opération",
                                            ),
                                            size=15,
                                            color=TEXT,
                                            weight=(
                                                ft.FontWeight.BOLD
                                            ),
                                        ),

                                        ft.Text(
                                            operation.get(
                                                "description",
                                                "",
                                            ),
                                            size=11,
                                            color=GREY,
                                            max_lines=1,
                                            overflow=(
                                                ft.TextOverflow
                                                .ELLIPSIS
                                            ),
                                        ),

                                        ft.Text(
                                            operation.get(
                                                "date",
                                                "",
                                            ),
                                            size=11,
                                            color=GREY,
                                        ),
                                    ],
                                    expand=True,
                                    spacing=3,
                                ),

                                # ------------------------------------
                                # MONTANT + STATUT
                                # ------------------------------------

                                ft.Column(
                                    [
                                        ft.Text(
                                            montant_affiche,
                                            size=14,
                                            color=couleur_montant,
                                            weight=(
                                                ft.FontWeight.BOLD
                                            ),
                                            text_align=(
                                                ft.TextAlign.RIGHT
                                            ),
                                        ),

                                        ft.Container(
                                            bgcolor=(
                                                couleur_fond
                                            ),
                                            border_radius=20,
                                            padding=(
                                                ft.Padding.symmetric(
                                                    horizontal=8,
                                                    vertical=3,
                                                )
                                            ),
                                            content=ft.Text(
                                                operation.get(
                                                    "statut",
                                                    "Effectué",
                                                ),
                                                size=10,
                                                color=couleur,
                                                weight=(
                                                    ft.FontWeight.BOLD
                                                ),
                                            ),
                                        ),
                                    ],
                                    horizontal_alignment=(
                                        ft.CrossAxisAlignment.END
                                    ),
                                    spacing=4,
                                ),
                            ],
                            vertical_alignment=(
                                ft.CrossAxisAlignment.CENTER
                            ),
                        ),
                    )
                )

            page.update()

        # ============================================================
        # BOUTONS FILTRES
        # ============================================================

        boutons_filtres = ft.Row(
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        )

        def changer_filtre(nouveau_filtre):

            nonlocal filtre_actuel

            filtre_actuel = nouveau_filtre

            boutons_filtres.controls.clear()

            for nom_filtre in [
                "Toutes",
                "Prêts",
                "Épargne",
                "Transferts",
            ]:
                actif = nom_filtre == filtre_actuel

                boutons_filtres.controls.append(
                    ft.Container(
                        padding=ft.Padding.symmetric(
                            horizontal=15,
                            vertical=9,
                        ),
                        border_radius=20,
                        bgcolor=(
                            BLUE
                            if actif
                            else ft.Colors.WHITE
                        ),
                        border=ft.Border.all(
                            1,
                            BLUE if actif else "#DCE3EF",
                        ),
                        on_click=lambda e, f=nom_filtre:
                        changer_filtre(f),
                        content=ft.Text(
                            nom_filtre,
                            size=13,
                            color=(
                                ft.Colors.WHITE
                                if actif
                                else TEXT
                            ),
                            weight=(
                                ft.FontWeight.BOLD
                                if actif
                                else ft.FontWeight.NORMAL
                            ),
                        ),
                    )
                )

            afficher_liste()
            page.update()

        # ============================================================
        # HEADER
        # ============================================================

        header = ft.Container(
            bgcolor=PURPLE,
            padding=ft.Padding.only(
                left=8,
                right=15,
                top=18,
                bottom=18,
            ),
            content=ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.WHITE,
                        icon_size=30,
                        on_click=lambda e: afficher_profil(),
                    ),

                    ft.Text(
                        "Historique des opérations",
                        color=ft.Colors.WHITE,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        expand=True,
                        text_align=ft.TextAlign.CENTER,
                    ),

                    ft.Container(
                        width=45,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        # ============================================================
        # RÉSUMÉ
        # ============================================================

        resume = ft.Container(
            margin=ft.Margin.only(
                left=20,
                right=20,
                top=18,
            ),
            padding=18,
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            border=ft.Border.all(
                1,
                "#E5EAF2",
            ),
            content=ft.Row(
                [
                    ft.Container(
                        width=45,
                        height=45,
                        border_radius=23,
                        bgcolor="#F0EBFF",
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            ft.Icons.RECEIPT_LONG,
                            color=PURPLE,
                            size=24,
                        ),
                    ),

                    ft.Column(
                        [
                            ft.Text(
                                "Mes opérations",
                                size=14,
                                color=GREY,
                            ),

                            ft.Text(
                                f"{len(operations)} opérations",
                                size=20,
                                color=TEXT,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        # ============================================================
        # CONSTRUCTION INITIALE DES FILTRES
        # ============================================================

        changer_filtre("Toutes")

        # ============================================================
        # AFFICHAGE
        # ============================================================

        page.add(
            ft.Column(
                [
                    header,

                    resume,

                    ft.Container(
                        padding=ft.Padding.only(
                            left=20,
                            right=20,
                            top=18,
                            bottom=8,
                        ),
                        content=boutons_filtres,
                    ),

                    ft.Container(
                        margin=ft.Margin.only(
                            left=20,
                            right=20,
                            bottom=20,
                        ),
                        padding=18,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=22,
                        expand=True,
                        content=liste_operations,
                    ),
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
                    # 👤 PHOTO DU CLIENT
                    creer_avatar_profil(
                        taille=50,
                        taille_icone=30,
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