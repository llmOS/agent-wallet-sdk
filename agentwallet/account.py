from typing import List
from typing import Optional

from .wallet import Wallet
from .transaction import Transaction
from .api_client import ApiClient


class Account:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    @classmethod
    def from_key(cls, api_key: str) -> "Account":
        return cls(api_key)

    def get_wallet(self, wallet_uid: str) -> Optional[Wallet]:
        response = ApiClient(self.api_key).get(f"wallets/{wallet_uid}/")
        if response.get("wallet"):
            transactions = []
            raw_transactions = response["wallet"].pop("transactions")
            for rt in raw_transactions:
                transactions.append(Transaction(**rt))
            return Wallet(
                _api_key=self.api_key, transactions=transactions, **response["wallet"]
            )

    def get_wallets(self) -> List[Wallet]:
        response = ApiClient(self.api_key).get("wallets")
        wallets = []
        for w in response["wallets"]:
            wallets.append(Wallet(_api_key=self.api_key, **w))
        return wallets
