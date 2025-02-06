from agents.jira_agent import jira_agent
from agents.issue_analysis_agent import issue_analysis_agent
from agents.llm_agent import llm_agent

def orchestrate_agents():
    """Orchestrates multiple agents to analyze long-open Jira issues."""
    
    print("🚀 Running Agent Orchestration...")
    
    # Step 1: Fetch Jira Sprint Issues
    sprint_issues = jira_agent()
    
    if not sprint_issues:
        print("⚠️ No issues found.")
        return

    # Step 2: Analyze Long-Open Issues
    long_open_issues = issue_analysis_agent(sprint_issues)  # ✅ No unpacking issue

    if not long_open_issues:
        print("✅ No long-open issues found. Sprint is on track!")
        return

    # Step 3: Use LLM to Analyze Delayed Issues
    print("\n🔎 Escalating Long-Open Issues to LLM...")
    
    for issue in long_open_issues:
        print(f"\n🤖 LLM Analysis for {issue['key']} ({issue['days_open']} days open)")
        analysis = llm_agent(issue)
        print(f"🔍 AI Response:\n{analysis}\n")

# Run Orchestration
if __name__ == "__main__":
    orchestrate_agents()
