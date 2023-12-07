# AgentWallet and Superagent Integration Example

## Overview
This example demonstrates the integration of AgentWallet for agent monetization and Superagent for agent-to-agent communication. It involves two specialized agents, a Sports agent and a Karate agent, to showcase inter-agent queries and fund transfers.

## Functionality

* **Initialization:** Import AgentWallet and Superagent modules, and set up API keys and Agent IDs for the Sports and Karate agents.
* **Account Balance Check:** Use `check_account_balance` to get the wallet balance of an account in USD.
* **Fund Transfer:** Demonstrate the transactional capabilities between agents' wallets during the query process.
* **Execution Flow:** Display the starting and ending balances of both agents to illustrate the financial transactions.

## How to run

To set up and run this example, follow these steps:

1) Ensure that `agentwallet` and `superagent-py` are installed in your Python environment.
```python
pip install agentwallet superagent-py
```

2) Run the script
```bash
python main.py
```

3) Observe the script's output, including agents' balance and their responses.
