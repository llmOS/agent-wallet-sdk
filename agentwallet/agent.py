from typing import Optional, Dict
from urllib.parse import urljoin
from enum import Enum
from dataclasses import dataclass, field

from .api_client import ApiClient
from .api_client import AGENT_WALLET_BASE_URL


class AgentType(str, Enum):
    OPENAI = "OPENAI"
    AGENTPROTOCOL = "AGENTPROTOCOL"
    SUPERAGENT_SH = "SUPERAGENT_SH"
    LANGSERVE = "LANGSERVE"


@dataclass
class Agent:
    _api_client: ApiClient = field(repr=False, compare=False)
    type: AgentType
    endpoint_id: str
    name: str
    description: str
    author: str
    price_usd_cents: int

    @property
    def base_url(self):
        return urljoin(AGENT_WALLET_BASE_URL, f"agents/{self.name}/")

    def run(self, query: str) -> str:
        data = self._api_client.post(
            self._format_call_url(),
            data=self._format_data(query),
        )
        return self._format_response(data)
    
    def _format_data(self, query: str) -> Dict:
        match self.type:
            case AgentType.AGENTPROTOCOL:
                return {"query": query}
            case AgentType.SUPERAGENT_SH:
                return {"query": query}
            case AgentType.LANGSERVE:
                return {"input": {"topic": query}}
            case _:
                return {"messages": [{"role": "user", "content": query}]}

    def _format_call_url(self) -> str:
        match self.type:
            case AgentType.AGENTPROTOCOL:
                return urljoin(self.base_url, "query")
            case AgentType.SUPERAGENT_SH:
                return urljoin(self.base_url, "invoke")
            case AgentType.LANGSERVE:
                return urljoin(self.base_url, "chat/invoke")
            case _:
                return urljoin(self.base_url, "v1/chat/completions")
            
    def _format_response(self, response) -> str:
        match self.type:
            case AgentType.AGENTPROTOCOL:
                return response["response"]
            case AgentType.SUPERAGENT_SH:
                return response["response"]
            case AgentType.LANGSERVE:
                return response["output"]["content"]
            case _:
                return response["choices"][0]["message"]["content"]