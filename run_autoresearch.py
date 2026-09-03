from agent.researcher import AutonomousResearcher


def main() -> None:
    researcher = AutonomousResearcher()

    best_metric = researcher.get_best_metric()

    if best_metric is None:
        raise RuntimeError(
            "No baseline or previous experiment found."
        )

    results = researcher.run_research_loop(
        baseline_metric=best_metric,
        model_path="research/runs/baseline/weights/best.pt",
        max_experiments=3,
    )

    print("\n===== Autonomous Research Summary =====")

    for result in results:
        print(result)


if __name__ == "__main__":
    main()