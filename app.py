import os
import json
from dotenv import load_dotenv
from agno.agent import Agent, RunResponse
from agno.models.google import Gemini

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

# Initialize the agent
agent = Agent(
    model=Gemini(
        id="gemini-2.0-flash-exp",
        name="IT Operations Orchestrator",
        api_key=api_key,
        temperature=0.7,
        top_p=0.8,
        top_k=40,
        max_output_tokens=2048,
        grounding=True,
        search=True,
        generation_config={
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 2048
        }
    ),
    markdown=True,
    use_json_mode=True
)

def create_plan_from_request(user_request: str):
    print(f"\nReceived request: '{user_request}'")
    print("Generating plan with Gemini...")

    try:
        # Use Agno's agent to generate the plan
        run: RunResponse = agent.run(user_request)
        plan_json = run.json()
        print("Successfully generated and parsed plan.")
        return plan_json
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == '__main__':
    # Define the user request from the demo scenario
    request = "Hey, can you get Sarah Smith access to the main marketing dashboard?"

    # Ask the agent to create a plan
    generated_plan = create_plan_from_request(request)

    # Display the result
    if generated_plan:
        print("\n--- Generated Plan ---")
        # Pretty-print the JSON for readability
        print(json.dumps(generated_plan, indent=2))
        print("--------------------")

        # Example of how the next agent might use this plan
        first_step = generated_plan.get("plan", [{}])[0]
        print(f"\nThe next step for the Access Control Agent would be to call the tool: '{first_step.get('tool')}'")

