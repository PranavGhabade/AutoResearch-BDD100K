from agent.controller import ResearchAgent


def main():
    agent = ResearchAgent(max_llm_calls=3)

    result = agent.inspect_project()

    print("\n===== AGENT RESPONSE =====\n")
    print(result)

    print("\n===========================\n")
    print(f"LLM calls used: {agent.llm_calls}")


if __name__ == "__main__":
    main()