import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv
from tools.jira_tools import get_sprint_issues_for_initiative

load_dotenv()

def initiative_analysis_agent(initiative_id, sprint_id):
    """Analyzes sprint work in the context of an initiative and updates RAG status."""

    print(f"📊 Analyzing Initiative {initiative_id} in Sprint {sprint_id}...")

    # Fetch all sprint issues belonging to the initiative
    relevant_issues = get_sprint_issues_for_initiative(sprint_id, initiative_id)

    if not relevant_issues:
        print(f"⚠️ No issues found for Initiative {initiative_id} in Sprint {sprint_id}.")
        return "No relevant work found."

    # Format the issues for AI analysis
    issues_text = "\n".join([
        f"- {issue['key']}: {issue['summary']} (Status: {issue['status']}, Assignee: {issue['assignee']})"
        for issue in relevant_issues
    ])

    # Construct the prompt
    prompt = f"""
    **Initiative:** {initiative_id}

    The following work was completed in Sprint {sprint_id}:
    {issues_text}

    **Analysis Required:**
    1. Summarize the key themes of the work completed.
    2. Identify any blockers or unresolved issues.
    3. Evaluate overall progress and assign a RAG status:
       - 🟢 Green: On track
       - 🟠 Amber: At risk
       - 🔴 Red: Off track

    Provide a structured breakdown.
    """

    # Use LLM to analyze progress
    llm = Ollama(model=os.getenv("OLLAMA_MODEL"))
    response = llm.invoke(prompt)

    return response
