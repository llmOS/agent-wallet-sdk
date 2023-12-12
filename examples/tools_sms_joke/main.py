import os
from typing import Optional
from typing import Type
import argparse

import requests
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool

from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel
from pydantic import Field


class SMSSendingToolSchema(BaseModel):
    to: str = Field(description="the phone number to send the SMS to")
    body: str = Field(description="SMS message body to send")


class AgentWalletSMSSendingTool(BaseTool):
    name = "sms_sending_tool"
    description = "useful for when you need to send SMS to a phone number"
    args_schema: Type[SMSSendingToolSchema] = SMSSendingToolSchema

    def _run(
        self,
        to: str,
        body: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        url = "https://api.agentwallet.ai/tools/sms-tool"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {os.getenv('AGENT_WALLET_API_KEY')}"
        }
        data = {
            "to": to,
            "body": body
        }
        result = requests.post(url, headers=headers, json=data)
        return f"SMS sending result: {result}"


def main(phone_number: str):
    llm = ChatOpenAI(temperature=1)
    tools = [AgentWalletSMSSendingTool()]
    agent = initialize_agent(
        tools, llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    agent.run(
        f"Please generate me a joke and send this with SMS to {phone_number}"
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--phone_number", help="phone number to send SMS to", type=str)
    args = parser.parse_args()
    main(args.phone_number)
