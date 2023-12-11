# Autogen x Agent Wallet example

This example shows a very simple Autogen-based agent that is monetized using Agent Wallet. The agent simply responds with a joke on whatever topic you ask it about. See the implementation in `joke_agent.py`.

To call it, use its name `autogen-agent1`. The agent implements an extremely simplified OpenAI-like API: a `/chat/completions` endpoint that takes in a list of messages and runs the agent.

## Calling the agent directly

Example of calling deployed agent through Agent Wallet:

```
curl -X POST https://api.agentwallet.ai/agents/test-autogen-agent1a/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer agent-user-123" \
-d '{"messages":[{"content":"hello","role":"user"}]}'
```

Example of calling the deployed agent directly -- hosted on [Replit](https://replit.com/@TaivoPungas/Autogen-agent1):

```
curl -X POST https://aw-autogen-agent1.replit.app/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer AGENT1_API_KEY" \
-d '{"messages":[{"content":"hello","role":"user"}]}'
```

Example of calling the agent directly, locally:

```
curl -X POST http://127.0.0.1:8000/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer AGENT1_API_KEY" \
-d '{"messages":[{"content":"hello","role":"user"}]}'
```

## Calling the agent from within another agent

`speech_agent.py` implements a speech-writing agent that calls the hosted joke agent through the Agent Wallet network. To run it:

1. Make sure you have the requirements: `pip install langchain agentwallet` installed
2. Run `python speech_agent.py`.

The output will look something like this:

```bash
TODO
```