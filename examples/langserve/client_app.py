import requests
import json

# API endpoint where speech_agent.py can be reached
# our example is hosted with Replit: 
# url = "https://agent-2.replit.app/invoke/"
url = ""

payload = json.dumps({
  "input": {
    "input": "Please help me write a speech about AI, but include on joke in the speech."
  }
})

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer call_me_with_this_key_2' # API key to auth into speech_agent.py service (hosted on Replit)
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
