import os
import requests
import base64
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

print(f"🔹 JIRA_BASE_URL: {JIRA_BASE_URL}")
print(f"🔹 JIRA_EMAIL: {JIRA_EMAIL}")
print(f"🔹 JIRA_API_TOKEN: {JIRA_API_TOKEN}")

# Encode Basic Auth credentials
auth_string = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}"
encoded_auth = base64.b64encode(auth_string.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_auth}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def get_active_sprint(board_id):
    """Fetch the active sprint from the given Jira board, handling pagination."""
    start_at = 0  # Start with the first page
    max_results = 50  # Jira default pagination limit
    
    while True:  # Loop through all pages
        sprint_url = f"{JIRA_BASE_URL}/rest/agile/1.0/board/{board_id}/sprint?startAt={start_at}&maxResults={max_results}"
        response = requests.get(sprint_url, headers=headers)

        if response.status_code == 200:
            sprints = response.json().get("values", [])
            
            print(f"\n🔍 DEBUG: Retrieved {len(sprints)} Sprints (Page Start: {start_at})")  # Debug output
            
            for sprint in sprints:
                print(f"🟢 Sprint: {sprint['name']} - State: {sprint['state']}")  # Print sprint details
                if sprint["state"] == "active":
                    print(f"✅ Found Active Sprint: {sprint['name']} (ID: {sprint['id']})")
                    return sprint["id"]
            
            # If there are no more results, exit the loop
            if len(sprints) < max_results:
                break

            start_at += max_results  # Move to the next page

        else:
            print(f"❌ ERROR {response.status_code}: {response.text}")  # Debug error details
            break

    print("⚠️ No Active Sprint Found")
    return None

def get_current_sprint_issues(board_id):
    """Fetch issues from the active sprint."""
    sprint_id = get_active_sprint(board_id)
    if not sprint_id:
        return "No active sprint found."

    issues_url = f"{JIRA_BASE_URL}/rest/agile/1.0/sprint/{sprint_id}/issue"
    response = requests.get(issues_url, headers=headers)

    if response.status_code == 200:
        return response.json()["issues"]
    
    print(f"❌ ERROR {response.status_code}: {response.text}")  # Debugging output
    return "Failed to fetch issues."
