import os
import requests
from langchain.agents import AgentType, initialize_agent
from langchain.tools import tool
from langchain.chat_models import ChatOpenAI
from urllib.parse import urljoin

AW_BASE_URL = os.getenv("AW_BASE_URL", "http://127.0.0.1:5000/")
AW_TOOLS = ["search-tool", "email-tool"]

AGENT_WALLET_API_KEY = os.getenv("AGENT_WALLET_API_KEY", "agent-user-123")


def _call_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name in AW_TOOLS:
        headers = {"Authorization": f"Bearer {AGENT_WALLET_API_KEY}"}
        response = requests.post(
            url=urljoin(AW_BASE_URL, f"/tools/{tool_name}"),
            json=tool_input,
            headers=headers,
        )
        return response.json()
    else:
        raise Exception(f"Unknown tool {tool_name}")


@tool("search-tool")
def _search_tool(query: str) -> str:
    """Searches the web for the query."""
    return str(_call_tool("search-tool", {"query": query}))


@tool("email-tool")
def _email_tool(to: str, subject: str, body: str) -> str:
    """Sends an email to an address with a subject and body in HTML format."""
    return str(_call_tool("email-tool", {"to": to, "subject": subject, "body": body}))


tools = [
   _search_tool,
   _email_tool,
]


def start_research(topic: str, email_to: str):
    prompt = f"Do a research on {topic}, then email it to {email_to}. Write a short summary on the topic. Include at least 3 web references in the email. Sign the email as "
    return start_research_with_prompt(prompt)


def start_research_with_prompt(prompt: str):
    llm = ChatOpenAI(
        temperature=0, model_name="gpt-4-1106-preview"
    )  # Also works well with Anthropic models
    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    response = agent_chain.invoke({"input": prompt})
    print(response["output"])


if __name__ == "__main__":
    start_research(
        "penguin mating season and prognosis for 2024", "kresimir@nftport.xyz"
    )
