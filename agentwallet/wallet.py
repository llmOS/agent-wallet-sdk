from typing import List, Optional
from dataclasses import dataclass, field

from .api_client import ApiClient
from .transaction import Transaction


@dataclass
class Wallet:
    _api_key: str = field(repr=False, compare=False)
    wallet_uid: str
    transactions: Optional[List[Transaction]] = None
    balance_usd_cents: Optional[int] = None

    def transfer(self, transfer_to: str, amount_usd_cents: int) -> bool:
        data = {
            "transfer_to_user_email": transfer_to,
            "amount_usd_cents": amount_usd_cents,
        }
        response = ApiClient(self._api_key).post(
            f"wallet/{self.wallet_uid}/transfer", data=data
        )
        return response["response"] == "OK"

    def balance(self) -> int:
        response = ApiClient(self._api_key).get(f"wallets/{self.wallet_uid}/")
        self.balance_usd_cents = response["wallet"]["balance_usd_cents"]
        return self.balance_usd_cents
