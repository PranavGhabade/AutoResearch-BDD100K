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
        model_path="cpu_test/research/cpu_test_runs/yolov8n_cpu_test/weights/best.pt",
        max_experiments=3,
    )

    print("\n===== Autonomous Research Summary =====")

    for result in results:
        print(result)


if __name__ == "__main__":
    main()