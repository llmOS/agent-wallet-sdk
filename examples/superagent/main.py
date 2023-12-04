from agentwallet import Account
from superagent.client import Superagent

# AgentWallet API keys
AGENTWALLET_SPORTS_AGENT_KEY = "aw-Ii78bWz__bDwl_VTmdPQ4srHICPLZHaNDVQYapkeOnE9DkTU"
AGENTWALLET_KARATE_AGENT_KEY = "aw-ftUYzKeXB9D7p3-n9lgdnSN3-OqB0WgMdvO1nRXxh85CVRhs"

# AgentWallet Agent IDs
SPORTS_AGENT_ID = "f60830db-8cd2-47c3-98ea-671ef4e0ee4c"
KARATE_AGENT_ID = "3d1ca3f9-38d9-4079-bc8f-c259a817ed85"


def check_account_balance(account: Account) -> int:
    wallets = account.get_wallets()
    wallet = account.get_wallet(wallets[0].wallet_uid)
    return wallet.balance_usd_cents


def is_help_needed(prediction: str) -> str:
    steps = prediction.data.get("intermediate_steps")
    if len(steps) > 0:
        agent_dispatch = {
            "call_karate_agent": query_agent_2,
        }
        item = steps[0][0]
        print(f"Asking Karate agent for help...")
        tool_name = item.get("tool")
        tool_function = agent_dispatch.get(tool_name)

        if tool_function:
            tool_input = item.get("tool_input", {})
            return tool_function(**tool_input)
    return None


def query_agent_1(question: str) -> str:
    # initialize Superagent client with AgentWallet base URL and API key
    client = Superagent(
        base_url="https://testwallet.sidekik.ai/agents/krešimir",
        token=AGENTWALLET_SPORTS_AGENT_KEY,
    )
    # ask agent a question
    prediction = client.agent.invoke(
        agent_id=SPORTS_AGENT_ID,
        input=question,
        enable_streaming=False,
    )
    # check if agent needs help from Karate agent
    help = is_help_needed(prediction)
    if help is not None:
        print(f"Karate agent: {help}")
    else:
        print(f"Olympic agent: {prediction.data['output']}")


def query_agent_2(question: str) -> str:
    client = Superagent(
        base_url="https://testwallet.sidekik.ai/agents/karate",
        token=AGENTWALLET_SPORTS_AGENT_KEY,  # <-- Account that is using the agent,
        # not the agent's account
    )
    prediction = client.agent.invoke(
        agent_id=KARATE_AGENT_ID,
        input=question,
        enable_streaming=False,
    )
    return prediction.data["output"]


if __name__ == "__main__":
    sports_agent_aw_account = Account.from_key(AGENTWALLET_SPORTS_AGENT_KEY)
    karate_agent_aw_account = Account.from_key(AGENTWALLET_KARATE_AGENT_KEY)
    print(
        f"Agent 1 starting balance: {check_account_balance(sports_agent_aw_account)/100:.2f} USD"
    )
    print(
        f"Agent 2 starting balance: {check_account_balance(karate_agent_aw_account)/100:.2f} USD"
    )
    query_agent_1(
        "How does the practice of Karate differ in terms of techniques and philosophy between traditional Okinawan styles and modern competitive styles?"
    )
    print(
        f"Agent 1 end balance: {check_account_balance(sports_agent_aw_account)/100:.2f} USD"
    )
    print(
        f"Agent 2 end balance: {check_account_balance(karate_agent_aw_account)/100:.2f} USD"
    )
