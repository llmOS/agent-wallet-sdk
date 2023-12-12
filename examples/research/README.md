# Research and summary Agent

This example demonstrates how to use AgentWallet `search-tool` and `email-tool` tools to enable a LangChain agent to easily access premium services without the bothering with signups on each platform.

`agent.py` - holds agent implementation

`app.py` - OpenAI-like interface for the agent

### Setup

```shell
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."
export AGENT_WALLET_API_KEY="aw-..."
```

### Usage

```shell
uvicorn app:app
```