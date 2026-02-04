import os

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools
from dotenv import load_dotenv

from src.prompts.main_prompt import system_message

# Load environment variables from .env file
load_dotenv("/home/ivangrana/Área de Trabalho/AA-MR/.env")

# Setup your database using environment variable or default
DB_FILE = os.getenv("AGNO_DB_FILE", "tmp/agno.db")
db = SqliteDb(db_file=DB_FILE)


# Use MCP URL from environment variable or default
# MCP_URL = os.getenv("MCP_URL", "http://127.0.0.1:8001/mcp")
# mcp_tools = MCPTools(url=MCP_URL)

# Use OpenAI model id and temperature from environment variables or defaults
OPENAI_MODEL_ID = os.getenv("OPENAI_MODEL_ID", "gpt-4.1-nano")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))

main_agent = Agent(
    name="AA-MR",
    model=OpenAIChat(id=OPENAI_MODEL_ID, temperature=OPENAI_TEMPERATURE),
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
    description="Agentic tool for metabolic modeling and analysis",
    instructions=system_message,
    markdown=True,
    reasoning=True,
    debug_level=1,
    # tools=[mcp_tools],
)
