import requests


class GmesAPI:

    BASE_URL = "https://gmeshaiti-aeo3.onrender.com"

    def __init__(self):
        self.token = None

    def headers(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        return headers

    # =========================================================
    # TEST API
    # =========================================================

    def test(self):

        response = requests.get(
            f"{self.BASE_URL}/api/mobile/test",
            timeout=30
        )

        return response.json()

    # =========================================================
    # LOGIN
    # =========================================================

    def login(self, identifier, password):

        response = requests.post(
            f"{self.BASE_URL}/api/mobile/login",
            json={
                "identifier": identifier,
                "password": password,
            },
            timeout=30
        )

        data = response.json()

        if response.ok and data.get("success"):
            self.token = data.get("token")

        return data

    # =========================================================
    # CLIENT CONNECTÉ
    # =========================================================

    def client_me(self):

        if not self.token:
            return {
                "success": False,
                "error": "Utilisateur non connecté."
            }

        response = requests.get(
            f"{self.BASE_URL}/api/mobile/client/me",
            headers=self.headers(),
            timeout=30
        )

        return response.json()

    # =========================================================
    # LOGOUT
    # =========================================================

    def logout(self):

        response = requests.post(
            f"{self.BASE_URL}/api/mobile/logout",
            headers=self.headers(),
            timeout=30
        )

        self.token = None

        return response.json()