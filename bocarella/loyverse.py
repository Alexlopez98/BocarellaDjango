import requests
from django.conf import settings

class LoyverseAPI:
    def __init__(self):
        self.base_url = "https://api.loyverse.com/v1.0/"
        self.headers = {
            "Authorization": f"Bearer {settings.LOYVERSE_TOKEN}",
            "Content-Type": "application/json"
        }

    def get_items(self):
        url = f"{self.base_url}items"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

# CREAMOS ESTE .PY PARA ORGANIZARLO MEJOR Y NO MEZCLARLO TODO EN VIEWS Y ASÍ QUE ESTO SEA LLAMADO DESDE VIEWS.