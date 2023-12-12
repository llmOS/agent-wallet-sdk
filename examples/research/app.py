import os
from typing import List, Optional
from openai import OpenAI
from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from agent import start_research_with_prompt

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


DEFAULT_RESPONSE = {
    "id": "chatcmpl-8UszFhN3SDeIp6DEZTs7XCJApC23l",
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "message": {
                "content": "Research started.",
                "role": "assistant",
                "function_call": None,
                "tool_calls": None,
            },
        }
    ],
    "created": 1702371901,
    "model": "hardcoded",
    "object": "chat.completion",
    "system_fingerprint": "fp_6aca3b5ce1",
    "usage": {"completion_tokens": 3, "prompt_tokens": 23, "total_tokens": 26},
}


def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != AGENT_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key"
        )


@app.post("/v1/chat/completions")
def chat_completions(
    request: ChatCompletionRequest,
    background_tasks: BackgroundTasks,
    _=Depends(verify_api_key),
):
    try:
        prompt = request.messages[-1].content
        background_tasks.add_task(start_research_with_prompt, prompt)
        return DEFAULT_RESPONSE
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


if __name__ == "__main__":
    topic = "penguin mating season and prognosis for 2024"
    email_to = "kresimir@nftport.xyz"
    prompt = f"Do a research on {topic}, then email it to {email_to}. Write a short summary on the topic. Include at least 3 web references in the email. Sign the email as "
    start_research_with_prompt(prompt)
