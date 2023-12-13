import argparse
import asyncio
import os
from pprint import pprint
from typing import Dict
from typing import List

import requests
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_function
from langchain_core.tools import BaseTool
from langchain_core.tools import tool

import get_coin

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AGENT_WALLET_API_KEY = os.getenv("AGENT_WALLET_API_KEY")
WALLET_ADDRESS: str = ""


async def main(
    user_input: str
) -> None:
    print(f"Running agent with user input: {user_input}")
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.4,
        openai_api_key=OPENAI_API_KEY,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a web3 assistant. You help users buy crypto currencies."
                " You do not need to know how much the user wants to buy."
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    tools: List[BaseTool] = [call_web3]
    llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    agent_executor.invoke({"input": user_input})
    print("Done!")


@tool
def call_web3() -> str:
    """Transfers 0.01 eth worth of cryptocurrency to the user."""
    coin: Dict = get_coin.execute()
    print(f"Selected coin to buy:")
    pprint(coin)
    coin_address = coin["platform"]["token_address"]
    result = requests.post(
        "https://api.agentwallet.ai/tools/web3-uniswap-transfer",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AGENT_WALLET_API_KEY}",
        },
        json={
            "to_address": WALLET_ADDRESS,
            "coin_address": coin_address,
        }
    )
    if result.status_code != 200:
        return "Transaction failed"
    return result.text


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", help="User query to send to the agent", type=str, required=True)
    parser.add_argument("--wallet_address", help="Wallet address to send the coin to", type=str, required=True)
    args = parser.parse_args()

    WALLET_ADDRESS = args.wallet_address
    asyncio.run(main(args.query))
