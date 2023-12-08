import os
import requests
import json
import logging
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from langchain.agents import AgentExecutor, tool
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.pydantic_v1 import BaseModel
from langchain.tools.render import format_tool_to_openai_function
from langserve import add_routes
from starlette import status

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agent Wallet service API key to access other agents
AGENTWALLET_API_KEY = os.environ['AGENTWALLET_API_KEY']

# Set up agent service auth - needed to register with Agent Wallet
AGENT_API_KEY = os.getenv("AGENT_API_KEY", "call_me_with_this_key_2")
security = HTTPBearer()


# Middleware that authenticates incoming API calls
def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(security)):
  if credentials.credentials != AGENT_API_KEY:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Invalid API Key")


# Set up agent API service
app = FastAPI(dependencies=[Depends(verify_api_key)])


# Tool that uses Agent Wallet proxy to access another agent
# Register on agentwallet.ai to get API key
# Need to know other agent's name & endpoint e.g. "/AgentOne/chat/invoke"
@tool
def get_joke_agent(query: str) -> str:
  """Returns joke agent's response which is a joke on the given topic."""
  url = "https://testwallet.sidekik.ai/agents/AgentOne/chat/invoke"
  payload = json.dumps({"input": {"topic": query}})
  headers = {
      'Authorization': AGENTWALLET_API_KEY,
      'Content-Type': 'application/json'
  }
  try:
    response = requests.request("POST", url, headers=headers,
                                data=payload).json()
    logger.info("successfully called agent 1")
    return response["output"]["content"]
  except Exception as e:
    return f"Error: {e}"


# Agent configuration using LangChain
tools = [get_joke_agent]
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful personal speech writing assistant."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

llm = ChatOpenAI()

llm_with_tools = llm.bind(
    functions=[format_tool_to_openai_function(t) for t in tools])

agent = ({
    "input":
    lambda x: x["input"],
    "agent_scratchpad":
    lambda x: format_to_openai_functions(x["intermediate_steps"]),
}
         | prompt
         | llm_with_tools
         | OpenAIFunctionsAgentOutputParser())

agent_executor = AgentExecutor(agent=agent, tools=tools)


# We need to add these input/output schemas because the current AgentExecutor is lacking in schemas.
class Input(BaseModel):
  input: str


class Output(BaseModel):
  output: str


# Using LangServe adds routes to the app for using the chain under:
# /invoke
# /batch
# /stream
add_routes(app, agent_executor.with_types(input_type=Input,
                                          output_type=Output))

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="localhost", port=8000)