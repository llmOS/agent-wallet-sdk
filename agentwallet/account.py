from typing import List
from typing import Optional

from .wallet import Wallet


class Account:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    @classmethod
    def from_key(cls, api_key: str) -> "Account":
        return cls(api_key)

    def get_wallet(self) -> Optional[Wallet]:
        pass

    def get_wallets(self) -> List[Wallet]:
        pass
