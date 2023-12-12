from typing import Any, Optional
from urllib.parse import urljoin
from enum import Enum
from dataclasses import dataclass, field

from .api_client import ApiClient
from .api_client import AGENT_WALLET_BASE_URL


@dataclass
class Tool:
    _api_client: ApiClient = field(repr=False, compare=False)
    name: str
    description: str
    price_usd_cents: int

    def run(self, *args: Any, **kwargs: Any) -> Any:
        data = self._api_client.post(
            urljoin(AGENT_WALLET_BASE_URL, f"tools/{self.name}"),
            data={**kwargs},
        )
        return data
