from langchain.llms import Ollama

def llm_agent(issue_details):
    """Analyzes long-open Jira issues using LangChain's Ollama integration."""
    
    llm = Ollama(model="deepseek-r1:14b")

    prompt = f"""
    The following Jira issue has been open for {issue_details['days_open']} days:
    - Issue Key: {issue_details['key']}
    - Summary: {issue_details['summary']}
    - Assignee: {issue_details['assignee']}
    - Current Status: {issue_details['status']}
    
    Based on this information, analyze why this issue might be taking longer than expected.
    Suggest possible resolutions or next steps.
    """

    response = llm.invoke(prompt)
    return response
