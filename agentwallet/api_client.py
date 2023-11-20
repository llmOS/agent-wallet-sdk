import os
import requests

AGENT_WALLET_BASE_URL = os.getenv("AGENT_WALLET_BASE_URL", "http://127.0.0.1:5000/")


class ApiClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def get(self, url: str) -> dict:
        return requests.get(
            f"{AGENT_WALLET_BASE_URL}{url}", headers=self.headers
        ).json()

    def post(self, url: str, data: dict) -> dict:
        return requests.post(
            f"{AGENT_WALLET_BASE_URL}{url}", headers=self.headers, json=data
        ).json()
