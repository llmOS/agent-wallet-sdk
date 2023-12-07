# Agent Wallet Python SDK

The Agent Wallet Python SDK is a powerful tool designed to simplify the integration of your AI agent with the AgentWallet platform. This SDK allows you to easily manage your agent's account, perform transactions, and access wallet information programmatically.

## Key Features

- **Simple Account Management:** Create and manage your agent's account with ease.
- **Wallet Operations:** Retrieve wallet information, check balances, and perform fund transfers.
- **Seamless Integration:** Designed to work effortlessly with AgentWallet's API platform.
- **Secure Authentication:** Utilizes API keys for secure interactions with your agent's account.

## Getting Started

❗ AgentWallet is in alpha stage and accessible only to early design partners. If you'd like to get access [please sign up for early access](https://form.typeform.com/to/Z7R4V1BM?typeform-source=github.com). We will contact you shortly after that.

1. **Installation:**

Install it using `pip`:

```bash
pip install agentwallet
```

2. **Setting Up Your Account:**

Import the Account class from the SDK and initialize it with your API key:

```python
from agentwallet import Account

account = Account.from_key("your-api-key")
```

3. **Managing Wallets:**

Fetch wallet information and manage transactions:
  
```python
# Fetch all wallets associated with the account
wallets = account.get_wallets()
print(f"Wallets: {wallets}")

# Access a specific wallet
wallet = account.get_wallet(wallets[0].wallet_uid)
print(f"Wallet: {wallet}")

# Perform a fund transfer
transfer_ok = wallet.transfer("recipient@email.com", amount)
print(f"Transfer successful: {transfer_ok}")

# Check the new balance
balance = wallet.balance()
print(f"New balance: ${balance / 100:.2f}")
```

## Support

If you have any questions or need help:

* Join our [Discord](https://discord.gg/AmdF5d94vE) and ask.
* Directly email Johannes, CEO of AgentWallet: `johannes@agentwallet.ai`.
