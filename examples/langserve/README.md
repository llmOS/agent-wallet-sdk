# LangServe x Agent Wallet example

## Description
Two agents in the network. 

## Steps to try yourself
### 1. Go and register an account at [Agent Wallet](https://agentwallet.ai/login)
### 2. Log in to [dashboard](https://agentwallet.ai/login) and get API key
### 3. Based on `.env.example` create `.env` file and insert the needed API keys
### 4. Read the code in both agents
#### 4.1  `local_speech_agent.py` is a LangChain agent implementation that is using Agent Wallet API as a tool to call out the other agent. This python script is meant to be used locally.
#### 4.2 The other agent `remote_joke_agent.py` is built with **LangServe**. We have deployed it via Replit (you can also deploy it yourself, see step 6) and registered to Agent Wallet to expose a wallet URL endpoint that monetizes the agent when others use it.