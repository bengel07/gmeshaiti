import os
import asyncio
import qrcode
import requests
from jinja2 import Template
from playwright.async_api import async_playwright


# ================= TEMPLATE =================
HTMLTEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Carte Employé GMES</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', 'Arial', 'Helvetica Neue', sans-serif;
            background: #e8e8e8;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        /* Carte principale - format carte de crédit / badge */
        .card {
            width: 1050px;
            height: 660px;
            background: #ffffff;
            border-radius: 24px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            position: relative;
            border: 1px solid #e0e0e0;
        }

        /* Bandeau supérieur */
        .card-header {
            background: #1a3a5c;
            padding: 20px 30px;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .company-title h2 {
            font-size: 22px;
            letter-spacing: 2px;
            font-weight: 600;
        }

        .company-title p {
            font-size: 12px;
            opacity: 0.8;
            margin-top: 5px;
        }

        .badge-autorise {
            background: #c9a03d;
            padding: 8px 20px;
            border-radius: 30px;
            font-size: 14px;
            font-weight: bold;
        }

        /* Valeurs */
        .values-bar {
            background: #f5f5f5;
            padding: 10px 30px;
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: #555;
            border-bottom: 1px solid #e0e0e0;
            font-weight: 500;
        }

        /* Contenu principal */
        .card-body {
            flex: 1;
            display: flex;
            padding: 25px 30px;
            gap: 30px;
        }

        /* Partie gauche - Photo et QR */
        .card-left {
            width: 220px;
            text-align: center;
        }

        .photo-frame {
            width: 180px;
            height: 250px;
            margin: 0 auto 20px;
            border-radius: 20px;
            overflow: hidden;
            border: 3px solid #D4AF37;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            background: #f0f0f0;
        }

        .photo-frame img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .qr-section {
            flex: 1;
            text-align: center;
        }

        .qr-section img {
            width: 100px;
            height: 100px;
            border: 2px solid #ddd;
            padding: 5px;
            border-radius: 12px;
            background: white;
        }

        .qr-label {
            font-size: 9px;
            color: #666;
            margin-top: 8px;
            text-transform: uppercase;
            font-weight: bold;
        }

        .qr-verified {
            font-size: 10px;
            color: #2e7d32;
            margin-top: 5px;
            font-weight: bold;
        }

        /* Partie droite - Informations */
        .card-right {
            flex: 1;
        }

        .employee-name {
            font-size: 28px;
            font-weight: 700;
            color: #1a3a5c;
            margin-bottom: 5px;
        }

        .employee-function {
            font-size: 16px;
            color: #c9a03d;
            font-weight: 600;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #eee;
        }

        .info-grid {
            display: grid;
            grid-template-columns: 130px 1fr;
            gap: 12px 10px;
            margin-bottom: 20px;
        }

        .info-label {
            font-size: 11px;
            font-weight: 600;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .info-value {
            font-size: 13px;
            font-weight: 500;
            color: #333;
        }

        .card-number-section {
            background: #f8f9fa;
            padding: 12px 15px;
            border-radius: 12px;
            margin: 15px 0;
            text-align: center;
            border: 1px dashed #c9a03d;
        }

        .card-number-label {
            font-size: 9px;
            color: #888;
            text-transform: uppercase;
        }

        .card-number {
            font-size: 16px;
            font-weight: bold;
            color: #1a3a5c;
            letter-spacing: 1px;
            font-family: monospace;
        }

        .slogan {
            font-size: 11px;
            color: #888;
            font-style: italic;
            text-align: center;
            margin-top: 10px;
        }

        /* Footer */
        .card-footer {
            background: #1a3a5c;
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
            font-size: 18px;
        }

        .footer-left .signature {
            font-size: 9px;
            font-style: italic;
            margin-top: 5px;
        }

        .footer-center {
            text-align: center;
        }

        .footer-right {
            text-align: right;
        }

        .footer-right .website {
            font-weight: bold;
            font-size: 11px;
        }

        hr {
            margin: 10px 0;
            border-color: rgba(255,255,255,0.2);
        }
    </style>
</head>
<body>
    <div class="card">
        <!-- En-tête -->
        <div class="card-header">
            <div class="company-title">
                <h2>GMES</h2>
                <p>GESTION MODERNE & SERVICES</p>
            </div>
            <div class="badge-autorise">
                EMPLOYÉ AUTORISÉ
            </div>
        </div>

        <!-- Valeurs -->
        <div class="values-bar">
            <span>CONFIANCE</span>
            <span>INTÉGRITÉ</span>
            <span>ENGAGEMENT</span>
            <span>DEPUIS 2023</span>
        </div>

        <!-- Corps -->
        <div class="card-body">
             <!-- Photo à gauche -->
            <div class="photo-section">
                <div class="photo-frame">
                    <img src="{{ photo }}" alt="Photo employé">
                </div>
            </div>
           
             <div class="info-section">
                <div class="employee-name">{{ nom }}</div>
                <div class="employee-function">{{ fonction }}</div>

                <div class="info-grid">
                    <div class="info-label">ID EMPLOYÉ</div>
                    <div class="info-value">{{ matricule }}</div>

                    <div class="info-label">DÉPARTEMENT</div>
                    <div class="info-value">{{ departement }}</div>

                    <div class="info-label">SUCCURSALE</div>
                    <div class="info-value">{{ succursale }}</div>

                    <div class="info-label">EMAIL</div>
                    <div class="info-value">{{ email }}</div>

                    <div class="info-label">TÉLÉPHONE</div>
                    <div class="info-value">{{ telephone }}</div>

                    <div class="info-label">DATE D'EMBAUCHE</div>
                    <div class="info-value">{{ date_embauche }}</div>
                </div>
     
                <div class="card-number-section">
                    <div class="card-number-label">CARTE N°</div>
                    <div class="card-number">{{ carte_numero }}</div>
                </div>

                <div class="slogan">
                    "Ensemble, construisons un avenir meilleur."
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="card-footer">
            <div class="footer-left">
                <div>Directeur Général</div>
                <div class="signature">_________________</div>
            </div>
            <div class="footer-center">
                <div>Bureau Principal</div>
                <div>Delmas 33, Port-au-Prince, Haïti</div>
            </div>
            <div class="footer-right">
                <div class="website">www.gmes.ht</div>
                <div>contact@gmes.ht</div>
                <div>+509 2813 0000</div>
            </div>
        </div>
     </div>
</body>
</html>"""

# ================= UTIL =================
def download_image(url, path):
    """Télécharge une image depuis une URL"""
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
        return path
    except Exception as e:
        print(f"Erreur téléchargement image: {e}")
        # Image par défaut si erreur
        return None


# ================= GÉNÉRATION =================
async def generate_card(user):
    """Génère une carte PDF pour un utilisateur"""

    os.makedirs("output", exist_ok=True)

    # Téléchargement photo
    photopath = f"output/photo_{user['id']}.jpg"
    if download_image(user["photo"], photopath) is None:
        photopath = None

    # Génération QR Code
    qr_data = f"GMES|{user['id']}|{user['matricule']}"
    qr = qrcode.make(qr_data)
    qrpath = f"output/qr_{user['id']}.png"
    qr.save(qrpath)

    # Rendu HTML
    template = Template(HTMLTEMPLATE)
    html = template.render(
        nom=user["nom"],
        fonction=user["fonction"],
        matricule=user["matricule"],
        departement=user["departement"],
        succursale=user.get("succursale", "Port-au-Prince"),
        email=user["email"],
        telephone=user["telephone"],
        date_embauche=user.get("date_embauche", "15 Janvier 2024"),
        carte_numero=user.get("carte_numero", "7F9A-3K8B-1D2E"),
        photo=photopath if photopath else "https://via.placeholder.com/180x180?text=Photo",
        qr=qrpath
    )

    # Sauvegarde HTML temporaire
    htmlpath = f"output/carte_{user['id']}.html"
    with open(htmlpath, "w", encoding="utf-8") as f:
        f.write(html)

    # Génération PDF
    pdfpath = f"output/carte_{user['id']}.pdf"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1200, "height": 800})

        # Convertir chemin en file:// URL
        file_url = f"file:///{os.path.abspath(htmlpath).replace(os.sep, '/')}"
        await page.goto(file_url, wait_until="networkidle")

        # PDF avec dimensions exactes
        await page.pdf(
            path=pdfpath,
            width="1050px",
            height="660px",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}
        )

        await browser.close()

    # Nettoyage HTML temporaire (optionnel)
    # os.remove(htmlpath)

    return pdfpath


# ================= TEST =================
if __name__ == "__main__":
    user = {
        "id": 1,
        "nom": "JEAN WILNER LOUIS",
        "fonction": "CONSEILLER CLIENTÈLE",
        "matricule": "GMES-2024-00125",
        "departement": "Opérations",
        "succursale": "Port-au-Prince",
        "email": "jean.louis@gmes.ht",
        "telephone": "+509 1234 5678",
        "date_embauche": "15 Janvier 2024",
        "carte_numero": "7F9A-3K8B-1D2E",
        "photo": "https://randomuser.me/api/portraits/men/32.jpg"
    }


    async def main():
        print("🔧 Génération de la carte en cours...")
        pdf = await generate_card(user)
        print(f"✅ Carte générée : {pdf}")


    asyncio.run(main())