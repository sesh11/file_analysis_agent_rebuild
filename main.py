from agents.analysis_agent import AnalysisAgent

def main():
    filename = input("enter filename:")
    user_query = input("what do you want to understand from the data?")
    context = input("Additional context about the data")

    agent = AnalysisAgent()

    answer = agent.analyze(filename, user_query, context)

    print("analysis results:")
    print(answer)

if __name__ == "__main__":
    main()



