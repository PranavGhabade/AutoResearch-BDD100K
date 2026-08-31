import json
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class ExperimentManager:
    RESULTS_DIR = PROJECT_ROOT / "research" / "results"

    def __init__(self):
        self.RESULTS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    def create_experiment_id(self) -> str:
        """
        Create a unique experiment identifier.
        """

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        return f"experiment_{timestamp}"

    def save_result(
        self,
        experiment_id: str,
        metrics: dict,
        status: str,
        description: str = "",
    ) -> Path:
        """
        Save experiment metadata and metrics.
        """

        result = {
            "experiment_id": experiment_id,
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "description": description,
            "metrics": metrics,
        }

        output_path = (
            self.RESULTS_DIR
            / f"{experiment_id}.json"
        )

        output_path.write_text(
            json.dumps(
                result,
                indent=4,
            ),
            encoding="utf-8",
        )

        return output_path

    def load_results(self) -> list[dict]:
        """
        Load all previously recorded experiment results.
        """

        results = []

        for file in self.RESULTS_DIR.glob("*.json"):
            try:
                data = json.loads(
                    file.read_text(
                        encoding="utf-8"
                    )
                )

                results.append(data)

            except json.JSONDecodeError:
                continue

        return results

    def get_best_result(
        self,
        metric: str,
    ) -> dict | None:
        """
        Return the experiment with the highest
        value for the specified metric.
        """

        results = self.load_results()

        valid_results = [
            result
            for result in results
            if metric in result.get("metrics", {})
        ]

        if not valid_results:
            return None

        return max(
            valid_results,
            key=lambda result: result["metrics"][metric],
        )