import os
import requests
import base64
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

auth_string = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}"
encoded_auth = base64.b64encode(auth_string.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_auth}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

### **🔹 Get All Epics Under an Initiative**
def get_epics_for_initiative(initiative_id):
    """Fetch all Epics under a given Initiative (e.g., DENG-3584)."""
    jql_query = f"parent={initiative_id} AND issuetype=Epic"
    url = f"{JIRA_BASE_URL}/rest/api/3/search?jql={jql_query}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ ERROR {response.status_code}: {response.text}")
        return []

    epics = response.json().get("issues", [])
    return [epic["key"] for epic in epics]

### **🔹 Get Issues from a Specific Sprint that Belong to Initiative Epics**
def get_sprint_issues_for_initiative(sprint_id, initiative_id):
    """Fetches Stories, Tasks, and Bugs in the sprint tied to Epics under the Initiative."""
    epics = get_epics_for_initiative(initiative_id)

    if not epics:
        print(f"⚠️ No epics found for Initiative {initiative_id}.")
        return []

    epic_keys = ",".join(epics)
    jql_query = f"sprint={sprint_id} AND issuetype in (Story, Task, Bug) AND parent in ({epic_keys})"
    url = f"{JIRA_BASE_URL}/rest/api/3/search?jql={jql_query}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ ERROR {response.status_code}: {response.text}")
        return []

    issues = response.json().get("issues", [])
    issue_list = []

    for issue in issues:
        issue_data = {
            "id": issue["id"],
            "key": issue["key"],
            "summary": issue["fields"].get("summary", ""),
            "description": issue["fields"].get("description", ""),
            "status": issue["fields"]["status"]["name"],
            "assignee": issue["fields"]["assignee"]["displayName"] if issue["fields"].get("assignee") else "Unassigned",
            "created": issue["fields"].get("created", ""),
            "resolution_date": issue["fields"].get("resolutiondate", ""),
            "status_history": get_issue_status_transitions(issue["id"]),
        }
        issue_list.append(issue_data)

    return issue_list

### **🔹 Get Issue Status Transitions (Track Movement in Workflow)**
def get_issue_status_transitions(issue_id):
    """Fetches the status history of a Jira issue to track lifecycle transitions."""
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_id}?expand=changelog"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ ERROR {response.status_code}: {response.text}")
        return []

    changelog_entries = response.json().get("changelog", {}).get("histories", [])
    status_transitions = []

    for entry in changelog_entries:
        for item in entry.get("items", []):
            if item.get("field") == "status":
                status_transitions.append({
                    "from": item.get("fromString"),
                    "to": item.get("toString"),
                    "timestamp": entry.get("created")
                })

    return status_transitions
