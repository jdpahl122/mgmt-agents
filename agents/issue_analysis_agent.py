from tools.issue_analytics import analyze_issue_duration

def issue_analysis_agent(issues):
    """Finds issues that have been open for 15+ days."""
    
    print("📊 Analyzing issue durations...")
    
    analysis_results, long_open_issues = analyze_issue_duration(issues)  # ✅ Correct unpacking
    
    return long_open_issues  # ✅ Only return the long-open issues
