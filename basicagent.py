from agno.agent import Agent, RunResponse  # noqa
from agno.models.google import Gemini
from dotenv import load_dotenv
load_dotenv()

agent = Agent(model=Gemini(id="gemini-2.0-flash-exp"), markdown=True)

# Get the response in a variable
run: RunResponse = agent.run("Share a 2 sentence horror story")
print(run.content)

# Print the response in the terminal
#agent.print_response("Share a 2 sentence horror story")