from agent.agent import Agent
import os
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    goal = "Extract the YouTube channel owner's name, description, latest video title and description."
    start_url = input("Enter the YouTube channel URL: ")
    agent = Agent(goal, service_to_sell=None, template_content=None)
    agent.run(start_url)