# Agent Wallet SDK

## How to test:

### 1. Make sure you're running [Agent Wallet backend](https://github.com/llmOS/agent-wallet) locally (port 5000)

#### 1.2.If you follow the set up, then there has to be `/data` folder and inside 3 files, please change the data inside to match the following:

1) `endpoints.json`
```bash
[
  {
    "user_id": "1",
    "endpoint_id": "startup-agent",
    "base_url": "http://localhost:5001/v1/chat/completions",
    "authorization": "Bearer your_api_key_here",
    "price_usd_cents": 10,
    "currency": "USD"
  },
  {
    "user_id": "2",
    "endpoint_id": "cb-agent",
    "base_url": "http://localhost:5003/v1/chat/completions",
    "authorization": "Bearer your_api_key_here",
    "price_usd_cents": 15,
    "currency": "USD"
  }
]
``````
2) `users.json`
```bash
[
  {
    "uid": "1",
    "name": "agent hoster",
    "email": "email1@email.com",
    "api_key": "agent-hoster-123"
  },
  {
    "uid": "2",
    "name": "agent hoster 2",
    "email": "email2@email.com",
    "api_key": "agent-hoster2-123"
  },
  {
    "uid": "3",
    "name": "agent user",
    "email": "email3@email.com",
    "api_key": "agent-user-123"
  }
]
``````
3) `wallets.json`
```bash
{
  "1": {
    "uid": "1",
    "user_uid": "1",
    "transactions": [],
    "balance_usd_cents": 1000
  },
  "2": {
    "uid": "2",
    "user_uid": "2",
    "transactions": [],
    "balance_usd_cents": 1000
  },
  "3": {
    "uid": "3",
    "user_uid": "3",
    "transactions": [],
    "balance_usd_cents": 1000
  }
}
``````

### 2. Install SDK locally
```bash
pip install -e .
``````
### 3. Run "Startup research agent"
```bash
cd examples/agent1
python startup_agent.py
``````

### 4. Run "Crunchbase agent"
```bash
cd examples/agent2
python cb_agent.py
``````

### 5. Interact with the "Startup research agent"
- Open `/examples/user_to_agent1.ipynb` notebook
- Run the code blocks and read comments to go through the flow