from agents.initiative_analysis_agent import initiative_analysis_agent

INITIATIVE_ID = "DENG-3580"  # Change this to your initiative ID
SPRINT_ID = 19896  # Change this to your sprint ID

if __name__ == "__main__":
    print("\n🚀 Running Initiative Sprint Analysis...")
    result = initiative_analysis_agent(INITIATIVE_ID, SPRINT_ID)
    print("\n✅ Analysis Complete!")
    print(result)
