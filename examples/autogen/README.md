# Autogen x Agent Wallet example

This example shows a very simple Autogen-based agent that is monetized using Agent Wallet.

To call it, use its name `autogen-agent1`. The agent implements a very minimal OpenAI-compatible API: only the `/chat/completions` endpoint.



### Agent 1 details

Registration response:
```
{
  "response": "OK",
  "agent": {
    "endpoint_id": "7271d4ae-02a2-4315-b65f-22d7a463d85a",
    "name": "test-autogen-agent1a",
    "description": "test",
    "author": "Taivo",
    "price_usd_cents": 1,
    "wallet_id": "91b71269-141f-4fe1-b754-e5e592af8091",
    "type": "OPENAI",
    "authorization": "Bearer AGENT1_API_KEY",
    "external_id": null,
    "url": "https://aw-autogen-agent1.replit.app/"
  }
}
```    
