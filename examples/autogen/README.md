# Autogen x Agent Wallet example

This example shows a very simple Autogen-based agent that is monetized using Agent Wallet. The agent simply responds with a joke on whatever topic you ask it about. See the implementation in `joke_agent.py`.

To call it, use its name `autogen-agent1`. The agent implements an extremely simplified OpenAI-like API: a `/chat/completions` endpoint that takes in a list of messages and runs the agent.

## Calling the agent directly

Example of calling deployed agent through Agent Wallet:

```
curl -X POST https://api.agentwallet.ai/agents/test-autogen-agent1a/v1/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer agent-user-123" \
-d '{"messages":[{"content":"hello","role":"user"}]}'
```

Example of calling the deployed agent directly -- hosted on [Replit](https://replit.com/@TaivoPungas/Autogen-agent1):

```
curl -X POST https://aw-autogen-agent1.replit.app/v1/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer AGENT1_API_KEY" \
-d '{"messages":[{"content":"hello","role":"user"}]}'
```

Example of calling the agent directly, locally:

```
curl -X POST http://127.0.0.1:8000/v1/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer AGENT1_API_KEY" \
-d '{"messages":[{"content":"hello","role":"user"}]}'
```

## Calling the agent from within another agent

`speech_agent.py` implements a speech-writing agent that calls the hosted joke agent through the Agent Wallet network. To run it:

1. Make sure you have the requirements: `pip install langchain agentwallet` installed
2. Run `python speech_agent.py`.

The output will look something like this:

```bash
$ python speech_agent.py


> Entering new AgentExecutor chain...
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"

Invoking: `get_joke_agent` with `{'query': 'AI'}`


INFO:__main__:Calling joke agent now...
INFO:__main__:Balance AFTER calling the tool: $49.48
https://api.agentwallet.ai/agents/test-autogen-agent1a/v1/chat/completions
INFO:__main__:Sucessfully called joke agent.
INFO:__main__:Balance AFTER calling the tool: $49.47; spent $0.01.
Why did the AI go to school?

Because it wanted to improve its "neural" networks and get a bit "smarter"!INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Ladies and gentlemen,

Today, I want to talk to you about a topic that has been revolutionizing the world as we know it: Artificial Intelligence, or AI. AI refers to the development of computer systems that can perform tasks that would typically require human intelligence. From self-driving cars to virtual assistants, AI is transforming various industries and enhancing our daily lives.

One of the fascinating aspects of AI is its ability to learn and adapt. AI algorithms can analyze vast amounts of data to identify patterns and make predictions. This has led to significant advancements in fields such as healthcare, finance, and transportation. For example, AI-powered systems can diagnose diseases more accurately, identify fraudulent transactions, and optimize traffic flow in cities.

But let's not forget that even AI has a sense of humor. In fact, there's a joke I'd like to share with you. Why did the AI go to school? Because it wanted to improve its "neural" networks and get a bit "smarter"! This lighthearted joke reminds us that AI, despite its sophistication, still has a touch of humor.

However, as we embrace the benefits of AI, it's crucial to address the ethical implications and ensure that it is used responsibly. AI should prioritize privacy, security, and fairness. It should be transparent and accountable, with human oversight to prevent any unintended consequences.

Moreover, we should also consider the impact of AI on the workforce. While AI can automate repetitive tasks and increase productivity, it also raises concerns about job displacement. It is essential to invest in education and upskilling programs to ensure a smooth transition for workers and create new opportunities in the AI-driven economy.

In conclusion, AI is a powerful tool that has the potential to shape the future in remarkable ways. It offers endless possibilities for innovation and improvement across various sectors. However, we must approach AI with caution, ensuring that it aligns with our values and serves humanity's best interests. Let's harness the power of AI while keeping our sense of humor intact.

Thank you.


```