import os
from tools.jira_tools import get_current_sprint_issues
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
JIRA_BOARD_ID = os.getenv("JIRA_BOARD_ID")

def jira_agent():
    """Fetch active sprint issues from Jira."""
    if not JIRA_BOARD_ID:
        raise ValueError("❌ ERROR: Missing JIRA_BOARD_ID in environment variables")

    print(f"📥 Fetching Jira sprint issues for Board ID {JIRA_BOARD_ID}...")
    issues = get_current_sprint_issues(JIRA_BOARD_ID)
    
    if not issues:
        print("⚠️ No issues found in the sprint.")
    
    return issues
