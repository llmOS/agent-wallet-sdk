from typing import List
from typing import Optional

from .tool import Tool
from .agent import Agent
from .agent import AgentType
from .wallet import Wallet
from .transaction import Transaction
from .api_client import ApiClient


class Account:
    def __init__(self, api_key: str) -> None:
        self.api_client = ApiClient(api_key)

    @classmethod
    def from_key(cls, api_key: str) -> "Account":
        return cls(api_key)

    def get_wallet(self, wallet_uid: str) -> Optional[Wallet]:
        response = self.api_client.get(f"wallets/{wallet_uid}")
        if response.get("wallet"):
            transactions = []
            raw_transactions = response["wallet"].pop("transactions")
            for rt in raw_transactions:
                transactions.append(Transaction(**rt))
            return Wallet(
                _api_client=self.api_client,
                transactions=transactions,
                **response["wallet"],
            )

    def get_wallets(self) -> List[Wallet]:
        response = self.api_client.get("wallets")
        wallets = []
        for w in response["wallets"]:
            wallets.append(Wallet(_api_client=self.api_client, **w))
        return wallets

    def get_agents(self) -> List[Agent]:
        response = self.api_client.get("dashboard/agents")
        agents = []
        for agent in response["agents"]:
            type = AgentType(agent["type"])
            agent.pop("type", None)
            agents.append(Agent(_api_client=self.api_client, type=type, **agent))
        return agents

    def get_agent(self, name) -> Optional[Agent]:
        response = self.api_client.get(f"dashboard/agents", params={"search": name})
        if len(response["agents"]) > 0:
            agent = response["agents"][0]
            type = AgentType(agent["type"])
            agent.pop("type", None)
            return Agent(_api_client=self.api_client, type=type, **agent)
        return None

    def get_tools(self) -> List[Tool]:
        response = self.api_client.get("tools")
        tools = []
        for tool in response["tools"]:
            tools.append(Tool(_api_client=self.api_client, **tool))
        return tools
    
    def get_tool(self, name: str) -> Optional[Tool]:
        response = self.api_client.get(f"tools/{name}")
        if response.get("tool"):
            return Tool(_api_client=self.api_client, **response["tool"])
        return None