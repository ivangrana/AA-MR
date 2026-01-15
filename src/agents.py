from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat

# Setup your database
db = SqliteDb(db_file="agno.db")

system_message = """You are a metabolic reconstruction agent.
your goal is to assist in the reconstruction of metabolic pathways. you should provide detailed explanations of the pathways."""

orchestrator_agent = Agent(
    name="Agno Assist",
    model=OpenAIChat(id="gpt-4.1-nano"),
    db=db,
    add_history_to_context=True,
    num_history_runs=5,
    description="Bug Bounty Hunter Agent",
    instructions=system_message,
    markdown=True,
    reasoning=False,
    debug_level=1,
    tools=[],
)
