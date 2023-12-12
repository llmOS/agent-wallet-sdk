# Research and Summary Agent

## Introduction

This example showcases the integration of LangChain agents with AgentWallet's `search-tool` and `email-tool`. These tools enable the agent to access premium services seamlessly, bypassing the need for individual platform signups. The project is structured into two main components: the agent implementation (`agent.py`) and an OpenAI-like interface for the agent (`app.py`).

## Features

- **LangChain Integration**: Utilizes LangChain to harness the capabilities of advanced language models.
- **AgentWallet Tools**: Employs AgentWallet's tools for efficient web searching and email handling.
- **Simplified Access**: Offers a streamlined approach to access premium services without individual platform signups.

## Setup

```shell
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."
export AGENT_WALLET_API_KEY="aw-..."
```

## Usage

To use the agent:

1. **Start the Server**: Launch the FastAPI server with Uvicorn using the command:
   ```shell
   uvicorn app:app

2. **Interact with the Agent**: Once the server is running, you can interact with the agent through the defined FastAPI endpoints.