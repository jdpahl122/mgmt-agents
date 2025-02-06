# Jira Sprint Analysis Orchestrator

This repository provides an automated workflow to analyze Jira sprint issues, identify long-open tasks, and use an LLM (DeepSeek 14B) via Ollama to investigate potential blockers.

The orchestrator runs multiple agents to:

1. Fetch active sprint issues from Jira
2. Analyze how long issues have been open
3. Identify issues that have been open for 15+ days
4. Send those issues to an LLM for analysis

## Installation and Setup

### 1. Clone the Repository
```bash
git clone git@github.com:jdpahl122/mgmt-agents.git
cd mgmt-agents
```

### 2. Install Dependencies
```bash
pipenv install
```

### 3. Configure your .env
```bash
# Jira API Configuration
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your_email@example.com
JIRA_API_TOKEN=your_api_token
JIRA_BOARD_ID=your_board_id

# Ollama Model Configuration
OLLAMA_MODEL=deepseek-r1:14b
```

Details on Each Variable:

* JIRA_BASE_URL: The base URL of your Jira instance.
* JIRA_EMAIL: Your Jira account email.
* JIRA_API_TOKEN: Your personal API token from Jira.
  * Generate one at: https://id.atlassian.com/manage/api-tokens.
* JIRA_BOARD_ID: The board ID where the sprint issues are located.
* OLLAMA_MODEL: The DeepSeek model being used. Use any model you like, but I tested with `deepseek-r1:14b` is installed in Ollama.

### 4. Install and Verify Ollama

Ensure Ollama is installed and the model is available:
```bash
ollama list
```

## Running the Orchestrator
Once everything is set up, run the orchestrator: 
```bash
pipenv shell
python -m orchestrator
```
This will: 
1. Fetch sprint issues from Jira from the active sprint.
2. Analyze how long issues have been open.
3. Identify issues open for more than 15 days.
4. Use DeepSeek 14B via Ollama to analyze why those issues are delayed.

## Agent Descriptions
1. Jira Agent (agents/jira_agent.py)
Fetches active sprint issues from Jira.
Reads the JIRA_BOARD_ID from .env.
Calls Jira's API to retrieve issue details.
2. Issue Analysis Agent (agents/issue_analysis_agent.py)
Analyzes sprint issues to track how long they have been open.
Identifies issues that have been open for 15+ days.
Returns a list of long-open issues for further investigation.
3. LLM Agent (agents/llm_agent.py)
Uses LangChain with Ollama to analyze long-open issues.
Runs the deepseek-r1:14b model locally via Ollama.
Provides insights on why issues might be delayed and suggests potential resolutions.
