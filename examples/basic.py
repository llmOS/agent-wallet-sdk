from agentwallet import Account

print("Agent Wallet Python SDK example")
print("================================")
account = Account.from_key("agent-hoster-123")
print("\nFetching wallets...")
wallets = account.get_wallets()
print(f"Wallets: {account.get_wallets()}")
print(f"\nFetching wallet {wallets[0].wallet_uid}")
wallet = account.get_wallet(wallets[0].wallet_uid)
print(f"Wallet {wallets[0].wallet_uid}: {wallet}")
transfer_ok = wallet.transfer("email2@email.com", 100)
print(f"\nTransfer successful: {transfer_ok}")
balance = wallet.balance()
print("\nNew balance: ${:.2f}".format(balance / 100))

card_name = "Mock Card"
print(f"\nGetting card for wallet {wallets[0].wallet_uid} and name {card_name}")
card = wallet.get_card(card_name)
print("Got card:", card)
