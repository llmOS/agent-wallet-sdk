from fastapi import Depends
from fastapi import FastAPI
import uvicorn
import sys

from fastapi import Security
from fastapi.security import APIKeyHeader
from typing import List, Optional
from openai import OpenAI
from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

app = FastAPI()
security = HTTPBearer()
client = OpenAI()

AGENT_API_KEY = os.getenv("AGENT_API_KEY", "agent-hoster-123")


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
    return {"name": "cb-agent", "price_usd_cents": 10}


# Mock agent - currently just system prompt
@app.post("/v1/chat/completions")
async def agent_endpoint(
    request: ChatCompletionRequest,
    _=Depends(verify_api_key),
):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or any other suitable model
            messages=[
                {
                    "content": "You are Crunchbase agent providing data about startups. You only have info about NFTPort right now, their funding is $26M.",
                    "role": "system"
                },
                {"role": "user", "content": request.messages[0].content}
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


if __name__ == "__main__":
    port = 5001  # default port
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number. Using default port {port}.")

    uvicorn.run(app, host="localhost", port=port)