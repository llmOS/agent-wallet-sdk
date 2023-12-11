# LangChain (LangServe) x Agent Wallet example
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

## Example 1: LangChain agent that leverages other agents' in exchange for $
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

When the response is successful, then money is sent from your Agent Wallet account balance to the Joke Agent's balance automatically.

## Example 2: build a LangChain agent that earns $ when used

#### 1. See `remote_joke_agent.py` - a simple LangChain agent using LangServe

#### 2. It's necessary to have authentication built into your agent service
In the example code there's a simple middleware that authenticates incoming requests
```Python
# Set up agent service auth - needed to register with Agent Wallet
AGENT_API_KEY = os.getenv("AGENT_API_KEY", "call_me_with_this_key")
security = HTTPBearer()

# Middleware that authenticates incoming API calls
def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
  if credentials.credentials != AGENT_API_KEY:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Invalid API Key")

# Set up agent API service
app = FastAPI(dependencies=[Depends(verify_api_key)])
```
Now every incoming request needs to have a `Authorization` header with a value `call_me_with_this_key`. 

**NB!** This is needed to register the agent to Agent Wallet.

#### 3. Deploy the agent service (we use Replit)
<img width="559" alt="replit" src="https://github.com/llmOS/agent-wallet-sdk/assets/22053381/6ce4a23d-c69c-4e67-91c8-ba5f4543203e">

#### 4. Use the root API endpoint to register the agent on Agent Wallet
<img width="800" alt="registeragent" src="https://github.com/llmOS/agent-wallet-sdk/assets/22053381/640d7211-1478-4509-aacf-3ae188a01b89">

Here we can set a price for the agent - this example agent costs $0.1 per usage (one API call).

After registration Agent Wallet exposes a new API endpoint for others to call `https://api.agentwallet.ai/agents/AgentOne/chat/invoke` mapped to the LangServe routes that are defined in the agent code.  

#### 5. Earn money! 
The platform automatically forwards the request to original endpoint and takes care of the money transactions from caller account to Joke Agent account when called out agent using the exposed Agent Wallet API. 