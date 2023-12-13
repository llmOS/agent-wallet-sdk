# Web3 investing agent

This agent is used to invest in cryptocurrencies through Agent Wallet.

The agent chooses a random popular currency and uses a tool to call an Agent Wallet tool to acquire it.

### Setup

```shell
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."
export AGENT_WALLET_API_KEY="aw-..."
export COINMARKETCAP_API_KEY=".....-..."
```

### Usage

```shell
python main.py --wallet_address='0x8eff3e243f018989De45100f8A84897AC4334ba1' --query='I want to invest in some crypto currency, please buy me some!'
```
