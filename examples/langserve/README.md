# LangChain (LangServe) x Agent Wallet example
## Description
Agent Wallet is a dev platform & tooling that enables devs build AI agents that exchange services and earn money.

In this example, agents built with LangChain (and LangServe) use Agent Wallet to monetize the resource exchanges, helping developers:

1. **create more capable agents** by leveraging the existing agents & tools on Agent Wallet platform (example: Local Speech Agent)
2. **earn money by building agents** or tools to the Agent Wallet platform for others to use (example: Remote Joke Agent)

<img width="800" alt="agent_example2" src="https://github.com/llmOS/agent-wallet-sdk/assets/22053381/2a115c6a-2a66-409d-8f0e-d15b0a35ba9e">

The diagram shows a local agent using Agent Wallet API to access the Joke Agent, deployed on Replit and registered with Agent Wallet. The registration creates a new API endpoint and reroutes calls to the original endpoint, with the Joke Agent costing $0.1 per call - helping its developer grow the wallet balance and earn money.

## Prerequisites to run examples

#### 1. Register an account to [Agent Wallet](https://agentwallet.ai/login)
#### 2. Log in to [dashboard](https://agentwallet.ai/login) and get your API key    
#### 3. Based on `.env.example` create `.env` file and insert the needed API keys
You'll find your [OpenAI API keys from here](https://platform.openai.com/api-keys)
#### 4. Run `pip install -r requirements.txt` in this folder

## Example 1: build an agent that leverages other agents' services in exchange for $
#### 1. Browse existing agents or tools in [Agent Wallet dashboard](https://agentwallet.ai/login)
<img width="800" alt="browse" src="https://github.com/llmOS/agent-wallet-sdk/assets/22053381/94672c07-6ccf-4ed8-bd9d-581a1a263fd8">

#### 2. See example code
Go to `local_speech_agent.py` - LangChain assitant agent that writes speeches. The agent leverages a joke generating agent named "AgentOne" (name is randomly chosen for testing) in the following snippet:

```python
# Tool that uses Agent Wallet proxy to request for other agent
# You'll find other agents to call out from Agent Wallet dashboard
@tool
def get_joke_agent(query: str) -> str:
  """Returns joke agent's response which is a joke on the given topic."""
  logger.info("Calling joke agent now...")
  url = "https://api.agentwallet.ai/agents/AgentOne/chat/invoke"
  payload = json.dumps({"input": {"topic": query}})
  headers = {
      'Authorization': "Bearer " + AGENTWALLET_API_KEY,
      'Content-Type': 'application/json'
  }
  try:
    response = requests.request("POST", url, headers=headers,
                                data=payload).json()
    logger.info("Sucessfully called joke agent.")
    return response["output"]["content"]
  except Exception as e:
    return f"Error: {e}"
```
The snippet is already in the code. No need to copy.

#### 3. Run the local speech agent on CLI
```bash
python local_speech_agent.py
```
You can also change the input message in the code:
```Python
agent_executor.invoke({"input": "Please help me write a speech about AI, but include a joke in the speech."})
```
If all goes well this is how the CLI should look like:

<img width="800" alt="output" src="https://github.com/llmOS/agent-wallet-sdk/assets/22053381/196e369a-1943-41c7-9c58-b88c10a67b65">

## Example 2: build an agent that earns $ when used


### 4. Read the code in both agents
#### 4.1  `local_speech_agent.py` is a LangChain agent implementation that is using Agent Wallet API as a tool to call out the other agent. This python script is meant to be used locally.
#### 4.2 The other agent `remote_joke_agent.py` is built with **LangServe**. We have deployed it via Replit (you can also deploy it yourself, see step 6) and registered to Agent Wallet to expose a wallet URL endpoint that monetizes the agent when others use it.