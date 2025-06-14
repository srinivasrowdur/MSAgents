from pydantic import BaseModel, Field
from agno.agent import Agent  # noqa
from agno.models.google import Gemini
from dotenv import load_dotenv

load_dotenv()

class RequestIntake(BaseModel):
    user_name: str = Field(
        ...,
        description="User's name extracted from the request message."
    )
    requested_role: str = Field(
        ...,
        description="Role being requested, as extracted from the message."
    )

request_intake_agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    description=(
        "You are a request parser. Your only job is to read an unstructured text request for system access "
        "and extract the key entities: the user's name and the role being requested. Format your output as "
        "a simple, clean JSON object. Do not infer, assume, or add any other information.\n\n"
        "Example Input: \"Hey, can you grant Alex the 'Payment Approver' role so he can cover for someone.\"\n"
        "Example Output: {\"user_name\": \"Alex\", \"requested_role\": \"Payment Approver\"}"
    ),
    response_model=RequestIntake,
)
