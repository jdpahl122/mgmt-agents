import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_ACCESS_TOKEN = os.getenv("JIRA_ACCESS_TOKEN")

def get_active_sprint(board_id):
    """Fetch the current active sprint for the given Jira board."""
    headers = {
        "Authorization": f"Bearer {JIRA_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    sprint_url = f"{JIRA_BASE_URL}/rest/agile/1.0/board/{board_id}/sprint"
    response = requests.get(sprint_url, headers=headers)
    
    if response.status_code == 200:
        sprints = response.json()["values"]
        for sprint in sprints:
            if sprint["state"] == "active":
                return sprint["id"]
    return None

def get_current_sprint_issues(board_id):
    """Fetch issues from the active sprint."""
    sprint_id = get_active_sprint(board_id)
    if not sprint_id:
        return "No active sprint found."
    
    issues_url = f"{JIRA_BASE_URL}/rest/agile/1.0/sprint/{sprint_id}/issue"
    headers = {
        "Authorization": f"Bearer {JIRA_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(issues_url, headers=headers)

    if response.status_code == 200:
        return response.json()["issues"]
    return "Failed to fetch issues."
