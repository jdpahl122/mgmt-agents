import os
from dotenv import load_dotenv
from tools.jira_tools import get_current_sprint_issues
from tools.issue_analytics import analyze_issue_duration

# Load environment variables
load_dotenv()

class JiraAgent:
    def __init__(self):
        self.board_id = os.getenv("JIRA_BOARD_ID")

    def fetch_sprint_issues(self):
        """Retrieve Jira sprint issues."""
        issues = get_current_sprint_issues(self.board_id)
        return issues

    def analyze_sprint(self):
        """Analyze issue duration per assignee."""
        sprint_issues = self.fetch_sprint_issues()
        if isinstance(sprint_issues, str):  # Handle errors
            print(f"❌ Error: {sprint_issues}")
            return

        analysis = analyze_issue_duration(sprint_issues)
        print("\n📊 Issue Aging Per Assignee:")
        for assignee, data in analysis.items():
            print(f"- {assignee}: Avg {data['avg_days_open']:.1f} days open ({data['issue_count']} issues)")

# Example usage
if __name__ == "__main__":
    agent = JiraAgent()
    agent.analyze_sprint()
