from fastapi import Depends
from fastapi import FastAPI
import uvicorn
import sys
import requests
from fastapi import Security
from fastapi.security import APIKeyHeader
from typing import List, Optional
from openai import OpenAI
from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import json

app = FastAPI()
security = HTTPBearer()
client = OpenAI()

AGENT_API_KEY = os.getenv("AGENT_API_KEY", "agent-user-123")

class Message(BaseModel):
    content: Optional[str] = Field(
        description="The contents of the message. `content is required for all messages, and may be null for assistant messages with function calls."
    )
    role: str = Field(description="Role")


class ChatCompletionRequest(BaseModel):
    messages: List[Message] = Field(
        ..., description="A list of messages comprising the conversation so far. "
    )

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello!"},
                ],
            }
        }


def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != AGENT_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key"
        )


@app.get("/info")
async def read_root(_=Depends(verify_api_key)):
    return {"name": "startup-agent", "price_usd_cents": 10}


# Mock startup agent - currently just system prompt
# Flow: 
# 1. End user asks startup agent a question
# 2. Startup agent requests Crunchbase agent price via /info
# 3. Checks if price is under 20 cents - then request CB agent
# 4. Present end user with data
@app.post("/v1/chat/completions")
async def agent_endpoint(
    request: ChatCompletionRequest,
    _=Depends(verify_api_key),
):
    cb_price = get_cb_agent_price()
    if cb_price < 100:
        startup_info = get_startup_info_crunchbase(request.messages[0].content)
    else:
        print("fart")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or any other suitable model
            messages=[
                {
                    "content": "You are a reseach agent for VCs, helping investors do researh about startups. You'll get information from Crunchbase that you need to present to the user.",
                    "role": "system"
                },
                {"content": request.messages[0].content, "role": "user"},
                {"content": startup_info, "role": "assistant"},
                {"content": "make it sound more official", "role": "user"}
            ],
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def get_cb_agent_price() -> int:
    try:
        url = "http://127.0.0.1:5001/info"
        payload = {}
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer agent-hoster-123'
        }
        response = requests.request("GET", url, headers=headers, data=payload).json()

        return response["price_usd_cents"]
    except Exception as e:
        print(e)


def get_startup_info_crunchbase(message):
    url = "http://127.0.0.1:5001/v1/chat/completions"
    payload = json.dumps({"messages":[{"content": message,"role": "user"}],"model": "cb-agent"})
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer agent-hoster-123'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


if __name__ == "__main__":
    port = 5003  # default port
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number. Using default port {port}.")

    uvicorn.run(app, host="localhost", port=port)