from typing import Optional
from agno.eval.accuracy import AccuracyEval, AccuracyResult
from agno.models.openai import OpenAIChat
from requestintake import request_intake_agent
import os
import json
from dotenv import load_dotenv

load_dotenv()

class AgentResponse:
    def __init__(self, content):
        self.content = content

class JsonAgentWrapper:
    def __init__(self, agent):
        self.agent = agent
        self.agent_id = getattr(agent, "agent_id", None)
        self.model = getattr(agent, "model", None)  # Forward model attribute

    def run(self, *args, **kwargs):
        response = self.agent.run(*args, **kwargs)
        content = getattr(response, "content", response)
        if hasattr(content, "json"):
            return AgentResponse(content.json())
        elif hasattr(content, "dict"):
            return AgentResponse(json.dumps(content.dict()))
        return AgentResponse(str(content))

evaluation = AccuracyEval(
    model=OpenAIChat(id="o4-mini"),
    agent=JsonAgentWrapper(request_intake_agent),
    input="Hey, can you grant Alex the 'Payment Approver' role so he can cover for someone.",
    expected_output='{"user_name": "Alex", "requested_role": "Payment Approver"}',
    additional_guidelines="Agent output should be a simple, clean JSON object with only the user's name and the requested role, matching the expected output exactly.",
)

result: Optional[AccuracyResult] = evaluation.run(print_results=True)
assert result is not None and result.avg_score >= 8
