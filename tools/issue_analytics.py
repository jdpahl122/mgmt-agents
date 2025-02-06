from datetime import datetime
from collections import defaultdict

def analyze_issue_duration(issues, threshold=15):
    """Identify issues that remain open beyond the given threshold."""
    
    today = datetime.utcnow()
    assignee_durations = defaultdict(list)
    long_open_issues = []

    for issue in issues:
        assignee = issue["fields"]["assignee"]["displayName"] if issue["fields"]["assignee"] else "Unassigned"
        created_date = datetime.strptime(issue["fields"]["created"][:10], "%Y-%m-%d")
        resolution_date = issue["fields"].get("resolutiondate")

        if resolution_date:
            resolved_date = datetime.strptime(resolution_date[:10], "%Y-%m-%d")
        else:
            resolved_date = today  # Still open, count time until today

        days_open = (resolved_date - created_date).days
        assignee_durations[assignee].append(days_open)

        # Collect long-open issues
        if days_open >= threshold:
            long_open_issues.append({
                "key": issue["key"],
                "summary": issue["fields"]["summary"],
                "assignee": assignee,
                "days_open": days_open,
                "status": issue["fields"]["status"]["name"]
            })

    # Compute average time per assignee
    results = {}
    for assignee, durations in assignee_durations.items():
        avg_duration = sum(durations) / len(durations)
        results[assignee] = {"avg_days_open": avg_duration, "issue_count": len(durations)}

    return results, long_open_issues  # ✅ Ensure two values are returned
