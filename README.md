# AA-MR: Autonomous Agents for Metabolic Reconstruction

The AA-MR (Autonomous Agents for Metabolic Reconstruction) is a multi-agent tool designed to streamline and enhance workflows for reconstructing metabolic pathways using AI-powered autonomous agents. By leveraging tools like Streamlit, OpenAI Chat models, and custom agents, AA-MR offers an interactive platform for metabolic pathway analysis, reconstruction, and exploration.

---

## Features and Functionalities

- **Dashboard Module**: A comprehensive view of metabolic reconstruction data using visualizations, metrics, and trends. Includes:
  - Visualization of pathway activity across samples with heatmaps.
  - Monitoring of total metabolic pathways, active reactions, and coverage scores.
  - Trend analysis for pathway activity.

- **Chat Module**: An AI-driven conversational interface for queries and interactions. Features include:
  - Chatbot responses powered by GPT-based models.
  - Persistent and context-aware chat history.
  - Interactive dynamic interface for seamless communication.

- **Gapfilling Module**: Analyze, gain insights, and summarize Swagger/OpenAPI specifications.
  - Upload and explore JSON or YAML specifications.
  - Automatically generate analyses for endpoints, authentication, and features.

- **Model Building Module**: Focus on metabolic pathway reconstruction tasks with the help of the Reconnaissance Agent.
  - Intelligent input interpretation and real-time responses for pathway construction tasks.
  - Session management with persistent dialog history.

- **Knowledge Base Module**: A tool to manage, edit, or delete informative snippets for expanding domain-specific knowledge.
  - Add new knowledge snippets.
  - Edit or delete existing knowledge descriptions.

---

## Built With

- [Streamlit](https://streamlit.io): Modern interface for rapid data-driven web applications.
- [Python](https://www.python.org): High-level programming language for smooth integration and processing.
- [Agno Framework](https://github.com): A framework for creating and managing AI-powered autonomous agents.
  - Incorporates SQLite for database management.
  - Uses the OpenAI GPT-4.1 Nano model for chat responses.

---

## 🗂 Project Organization

### Key Files
- `main.py`: Entry point for the Streamlit-based user interface and controls navigation between modules.
- `src/agents.py`: Contains the configuration for the primary orchestrator agent, including its instructions and Streamlit integration.

### Directory Structure
- `src/`: Contains source code for agents and related functionalities.
- `README.md`: This documentation describing project goals, features, and setup instructions.

---

## How It Works

### Metabolic Reconnaissance Agent
The AA-MR tool uses the `orchestrator_agent` configured in the `src/agents.py` to handle AI-driven tasks. This agent assists in identifying and reconstructing metabolic pathways by using its specialized capabilities to:
1. Analyze user-provided inputs (e.g., prompts, Swagger specs).
2. Interact with users in real-time through a friendly chatbot-like interface.
3. Manage a persistent database to store knowledge snippets and session history.

### Modules Overview
- **Interactive Chat**: Engage with the system directly by asking questions or making requests for analytical tasks.
- **Swagger Docs Analyzer**: Automatically analyzes API documentation and highlights critical information.
- **Knowledge Base Management**: Provides functionalities to store, update, or remove snippets to improve the working knowledge of the reconstruction process.

---

## Getting Started

### Prerequisites
- Python 3.8+
- Poetry (Dependency Manager)
- Streamlit library
- OpenAI GPT-4.1 API access
- Supported web browser for optimal user experience.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ivangrana/AA-MR.git
   cd AA-MR
   ```

2. Install dependencies using [Poetry](https://python-poetry.org/):
   ```bash
   poetry install
   ```

3. Set up your OpenAI API keys and configure the environment variables.

### Running AA-MR
Start the Streamlit app by running:
```bash
streamlit run main.py
```

Open in your browser at `http://localhost:8501/`.

---
- *Developed by Ivan Grana @ivangrana*
