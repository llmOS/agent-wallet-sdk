import os
from typing import List, Optional
from openai import OpenAI
from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()
security = HTTPBearer()
client = OpenAI()

AGENT_API_KEY = os.getenv("AGENT_API_KEY", "your_api_key_here")


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


@app.post("/v1/chat/completions")
def chat_completions(request: ChatCompletionRequest, _=Depends(verify_api_key)):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or any other suitable model
            messages=[
                {"role": msg.role, "content": msg.content} for msg in request.messages
            ],
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
