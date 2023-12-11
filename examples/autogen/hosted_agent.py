from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from typing import List, Optional, Union, Dict
from pydantic import BaseModel, Field
from pydantic import BaseModel
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json


class Message(BaseModel):
    content: Optional[str] = Field(
        description="The contents of the message."
    )
    role: str = Field(description="Role")

# Define a model for the request body
class ChatCompletionRequest(BaseModel):
    messages: List[Message] = Field(
        ..., description="A list of messages comprising the conversation so far. "
    )


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
assistant = AssistantAgent("assistant", llm_config={"config_list": config_list},
                           system_message="Tell a joke about the topic given by the user.")
user_proxy = UserProxyAgent("user_proxy", human_input_mode="NEVER", max_consecutive_auto_reply=0, code_execution_config=False)


@app.post(
    "/chat/completions",
    dependencies=[Depends(get_api_key)]
)
async def openai_chat_endpoint(request: ChatCompletionRequest):
    input_message = request.messages[-1].content # Ignore all messages except the last one
    user_proxy.initiate_chat(assistant, message=input_message)
    last_message = assistant.last_message()

    result = {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": last_message
            }
        ],
        "model": "autogen-assistant"
    }
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port="8080")

# alternatively, run with: uvicorn hosted_agent:app --reload


