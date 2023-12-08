# Autogen x Agent Wallet example

This example shows a very simple Autogen-based agent that is monetized using Agent Wallet.

To call it, use its name `autogen-agent1`. The agent implements an extremely simplified OpenAI-like API: a `/chat/completions` endpoint that takes in a list of messages and runs the agent.

Example of calling deployed agent through Agent Wallet:

```
curl -X POST https://api.agentwallet.ai/agents/test-autogen-agent1a/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer agent-user-123" \
-d '{"messages":[{"content":"hello","role":"user"}]}'
```

Example of calling the deployed agent directly:

```
curl -X POST https://aw-autogen-agent1.replit.app/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer AGENT1_API_KEY" \
-d '{"messages":[{"content":"hello","role":"user"}]}'

Example of calling the agent directly, locally:

curl -X POST http://127.0.0.1:8000/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer AGENT1_API_KEY" \
-d '{"messages":[{"content":"hello","role":"user"}]}'


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
