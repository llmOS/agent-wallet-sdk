from agentwallet import Account

print("Agent Wallet Python SDK example")
print("================================")
account = Account.from_key("aw-ftUYzKeXB9D7p3-n9lgdnSN3-OqB0WgMdvO1nRXxh85CVRhs")
print("\nFetching agents...")
agents = account.get_agents()
for agent in agents:
    print(agent)
    print(f"To use this agent set your library's base URL {agent.base_url}")
print("\nFetching wallets...")
wallets = account.get_wallets()
print(f"Wallets: {account.get_wallets()}")
print(f"\nFetching wallet {wallets[0].wallet_uid}")
wallet = account.get_wallet(wallets[0].wallet_uid)
print(f"Wallet {wallets[0].wallet_uid}: {wallet}")
# transfer_ok = wallet.transfer("email2@email.com", 100)
# print(f"\nTransfer successful: {transfer_ok}")
balance = wallet.balance()
print("\nNew balance: ${:.2f}".format(balance / 100))
tools = account.get_tools()
print(f"Tools: {tools}")
# fetching email tool
print("\nFetching email tool...")
email_tool = account.get_tool("email-tool")
# sending email
print("\nSending email...")
print(email_tool.run(to="test@test.com", subject="Test", body="Test body"))

card_name = "Mock Card"
print(f"\nGetting card for wallet {wallets[0].wallet_uid} and name {card_name}")
card = wallet.get_card(card_name)
print("Got card:", card)

print("Calling karate agent...")
test_agent = account.get_agent("karate") 
print(test_agent.run("How do I kick someone in the face?"))

