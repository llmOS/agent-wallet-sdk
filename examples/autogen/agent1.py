from fastapi import FastAPI, HTTPException, Request, Depends, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# Define a model for the request body
class ChatRequest(BaseModel):
    message: str

# Initialize FastAPI app
app = FastAPI()

# Define API key header info
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == "Bearer AGENT1_API_KEY":
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Invalid API Key")

# Initialize your assistant and user_proxy agents
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})

@app.post("/chat", dependencies=[Depends(get_api_key)])
async def chat_endpoint(request: ChatRequest):
    try:
        # Call user_proxy.initiate_chat with the request message
        response = user_proxy.initiate_chat(assistant, message=request.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run with: uvicorn agent1:app --reload