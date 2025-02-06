from tools.jira_tools import get_current_sprint_issues
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class JiraAgent:
    def __init__(self):
        self.board_id = os.getenv("JIRA_BOARD_ID")

    def fetch_sprint_issues(self):
        """Calls the tool function to retrieve Jira sprint issues."""
        issues = get_current_sprint_issues(self.board_id)
        return issues

# Example usage
if __name__ == "__main__":
    agent = JiraAgent()
    sprint_issues = agent.fetch_sprint_issues()
    print(sprint_issues)
