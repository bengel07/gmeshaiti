# diagnostic_conseiller.py
import requests
import json
from colorama import init, Fore, Style

# Initialiser colorama pour les couleurs
init(autoreset=True)

BASE_URL = "http://127.0.0.1:10000"


def print_section(title):
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def print_result(test_name, success, message, details=None):
    status = f"{Fore.GREEN}✅ SUCCÈS{Style.RESET_ALL}" if success else f"{Fore.RED}❌ ÉCHEC{Style.RESET_ALL}"
    print(f"{status} - {test_name}")
    print(f"   {message}")
    if details:
        print(f"   Détails: {json.dumps(details, indent=2, ensure_ascii=False)[:500]}")


def test_page_exists():
    """Test 1: Vérifier si la page 'conseiller' existe dans PAGES"""
    try:
        response = requests.get(f"{BASE_URL}/debug/diagnostic_complet", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'conseiller' in data.get('pages', {}):
                page_data = data['pages']['conseiller']
                if page_data.get('exists'):
                    return True, "Page 'conseiller' trouvée dans PAGES", page_data
            return False, "Page 'conseiller' non trouvée dans PAGES", data.get('pages', {})
        return False, f"Erreur HTTP {response.status_code}", None
    except Exception as e:
        return False, f"Erreur: {str(e)}", None


def test_url_generation():
    """Test 2: Vérifier la génération de l'URL"""
    try:
        response = requests.get(f"{BASE_URL}/debug/test_conseiller", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == '✅ OK':
                return True, f"URL générée: {data.get('generated_url')}", data
            return False, data.get('error', 'Erreur inconnue'), data
        return False, f"Erreur HTTP {response.status_code}", None
    except Exception as e:
        return False, f"Erreur: {str(e)}", None


def test_route_directe():
    """Test 3: Tester l'accès direct à la route"""
    try:
        # Tester avec session (simuler la connexion)
        session = requests.Session()

        # D'abord, se connecter
        login_data = {
            'email': 'super_admin@gmes.com',
            'password': 'admin123'
        }
        login_response = session.post(f"{BASE_URL}/connexion", data=login_data)

        if login_response.status_code == 302:
            # Maintenant tester la route conseiller
            response = session.get(f"{BASE_URL}/employe/conseiller", allow_redirects=False)

            if response.status_code == 200:
                return True, "Route accessible (200)", {'status_code': 200}
            elif response.status_code == 302:
                redirect_url = response.headers.get('Location', 'Inconnu')
                return False, f"Redirection vers: {redirect_url}", {'status_code': 302, 'redirect': redirect_url}
            else:
                return False, f"Code HTTP: {response.status_code}", {'status_code': response.status_code}
        else:
            return False, "Échec de la connexion", None
    except Exception as e:
        return False, f"Erreur: {str(e)}", None


def test_super_admin_redirect():
    """Test 4: Tester la redirection depuis super_admin"""
    try:
        session = requests.Session()

        # Se connecter
        login_data = {
            'email': 'super_admin@gmes.com',
            'password': 'admin123'
        }
        session.post(f"{BASE_URL}/connexion", data=login_data)

        # Tester la redirection super_admin/go
        response = session.get(f"{BASE_URL}/super_admin/go/conseiller", allow_redirects=False)

        if response.status_code == 302:
            redirect_url = response.headers.get('Location', 'Inconnu')
            return True, f"Redirection vers: {redirect_url}", {'redirect': redirect_url}
        elif response.status_code == 200:
            return True, "Page affichée directement (200)", {'status_code': 200}
        else:
            return False, f"Code HTTP: {response.status_code}", {'status_code': response.status_code}
    except Exception as e:
        return False, f"Erreur: {str(e)}", None


def test_template_exists():
    """Test 5: Vérifier si le template existe"""
    try:
        response = requests.get(f"{BASE_URL}/debug/template_exists", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('exists'):
                return True, f"Template trouvé: {data.get('template_path')}", data
            return False, f"Template non trouvé: {data.get('template_path')}", data
        return False, f"Erreur HTTP {response.status_code}", None
    except Exception as e:
        return False, f"Erreur: {str(e)}", None


def test_session_status():
    """Test 6: Vérifier l'état de la session"""
    try:
        session = requests.Session()

        # Se connecter
        login_data = {
            'email': 'super_admin@gmes.com',
            'password': 'admin123'
        }
        session.post(f"{BASE_URL}/connexion", data=login_data)

        # Vérifier la session
        response = session.get(f"{BASE_URL}/debug/session_status")
        if response.status_code == 200:
            data = response.json()
            if data.get('is_logged_in') and data.get('role') == 'super_admin':
                return True, f"Connecté en tant que: {data.get('email')} (rôle: {data.get('role')})", data
            return False, "Non connecté ou mauvais rôle", data
        return False, f"Erreur HTTP {response.status_code}", None
    except Exception as e:
        return False, f"Erreur: {str(e)}", None


def run_diagnostics():
    """Exécute tous les tests"""
    print_section("🔍 DIAGNOSTIC COMPLET - ROUTE CONSEILLER")

    # Liste des tests
    tests = [
        ("Session utilisateur", test_session_status),
        ("Page dans PAGES", test_page_exists),
        ("Génération URL", test_url_generation),
        ("Template existe", test_template_exists),
        ("Accès direct /employe/conseiller", test_route_directe),
        ("Redirection depuis super_admin", test_super_admin_redirect),
    ]

    results = []
    for name, test_func in tests:
        success, message, details = test_func()
        results.append((name, success, message, details))
        print_result(name, success, message, details)

    # Résumé
    print_section("📊 RÉSUMÉ")
    success_count = sum(1 for r in results if r[1])
    total = len(results)

    print(f"\nTests réussis: {Fore.GREEN}{success_count}{Style.RESET_ALL}/{total}")

    if success_count == total:
        print(f"\n{Fore.GREEN}🎉 TOUS LES TESTS RÉUSSISSENT !{Style.RESET_ALL}")
        print("Le problème est probablement dans le template ou les données.")
    else:
        print(f"\n{Fore.YELLOW}⚠️ {total - success_count} test(s) ont échoué{Style.RESET_ALL}")
        print("\nVérifie les détails ci-dessus pour identifier le problème.")

        # Recommandations
        print_section("💡 RECOMMANDATIONS")
        for name, success, message, details in results:
            if not success:
                if "redirection" in message.lower() or "302" in message:
                    print(f"- {Fore.YELLOW}La route {name} redirige: {message}{Style.RESET_ALL}")
                    print("  → Vérifie la condition d'accès dans conseiller_dashboard()")
                elif "template" in message.lower():
                    print(f"- {Fore.YELLOW}Problème de template: {message}{Style.RESET_ALL}")
                    print("  → Crée le fichier templates/conseiller_dashboard.html")
                elif "connexion" in message.lower():
                    print(f"- {Fore.YELLOW}Problème de connexion: {message}{Style.RESET_ALL}")
                    print("  → Vérifie les identifiants super_admin@gmes.com / admin123")
                else:
                    print(f"- {Fore.YELLOW}{name}: {message}{Style.RESET_ALL}")


if __name__ == "__main__":
    print(f"{Fore.CYAN}🚀 Lancement du diagnostic...{Style.RESET_ALL}")
    print(f"Base URL: {BASE_URL}")
    print("Assure-toi que le serveur Flask est en cours d'exécution !")

    try:
        run_diagnostics()
    except requests.exceptions.ConnectionError:
        print(f"\n{Fore.RED}❌ Impossible de se connecter au serveur !{Style.RESET_ALL}")
        print("Assure-toi que le serveur Flask est lancé sur http://127.0.0.1:10000")
    except KeyboardInterrupt:
        print("\n\nDiagnostic interrompu.")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Erreur inattendue: {str(e)}{Style.RESET_ALL}")