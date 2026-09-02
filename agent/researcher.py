from __future__ import annotations

import json
import shutil
from pathlib import Path

from agent.controller import ResearchAgent
from agent.experiment_manager import ExperimentManager
from agent.guardrails import validate_write
from agent.tools import read_file, run_command, write_file


PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXPERIMENT_DIR = PROJECT_ROOT / "research" / "experiments"
BACKUP_DIR = PROJECT_ROOT / "research" / ".backup"


class AutonomousResearcher:
    """
    Execute exactly one autonomous research experiment.

    Flow:
        inspect -> propose -> modify -> train -> evaluate
        -> compare -> keep/revert
    """

    def __init__(self, llm=None):
        self.agent = ResearchAgent(llm=llm)
        self.experiment_manager = ExperimentManager()

    def get_best_metric(self, metric: str = "map50_95") -> float | None:
        """
        Return the best metric from previously recorded experiments.
        """

        best = self.experiment_manager.get_best_result(metric)

        if best is None:
            return None

        return best["metrics"][metric]

    def inspect(self) -> str:
        """
        Inspect the project before proposing an experiment.
        """

        files = self.agent.execute_action(
            {
                "action": "list_files",
                "path": "model",
            }
        )

        config = read_file("model/config.yaml")
        train_code = read_file("model/train.py")

        return (
            "PROJECT FILES:\n"
            f"{files}\n\n"
            "CONFIG:\n"
            f"{config}\n\n"
            "TRAINING CODE:\n"
            f"{train_code}"
        )

    def propose_experiment(
        self,
        project_context: str,
    ) -> dict:
        """
        Ask the LLM to propose exactly one experiment.
        """

        prompt = f"""
You are an ML research agent working on an object detection project.

Your task is to propose EXACTLY ONE small, testable experiment.

Project context:

{project_context}

Rules:

1. Propose exactly one experiment.
2. Modify only files allowed by the project guardrails.
3. Do not modify evaluation code.
4. Do not modify dataset annotations or images.
5. Do not modify agent infrastructure.
6. The experiment must be related to model training.
7. The change must be reversible.
8. Do not propose multiple alternatives.
9. Return ONLY valid JSON.

Required JSON format:

{{
    "hypothesis": "short explanation",
    "file": "path/to/file",
    "change": "specific change to make",
    "content": "complete replacement content for the file"
}}

The "content" field must contain the COMPLETE contents of the modified file,
not a patch and not a partial snippet.
"""

        decision = self.agent._ask_llm(prompt)

        required = {
            "hypothesis",
            "file",
            "change",
            "content",
        }

        missing = required - decision.keys()

        if missing:
            raise ValueError(
                f"Experiment proposal missing fields: {sorted(missing)}"
            )

        return decision

    def backup_file(self, file_path: str) -> Path:
        """
        Back up a file before modifying it.
        """

        source = (PROJECT_ROOT / file_path).resolve()

        if not source.is_relative_to(PROJECT_ROOT):
            raise PermissionError(
                "Cannot back up a file outside the project."
            )

        if not source.exists():
            raise FileNotFoundError(
                f"Cannot back up missing file: {file_path}"
            )

        BACKUP_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        backup = BACKUP_DIR / source.name

        shutil.copy2(
            source,
            backup,
        )

        return backup

    def restore_file(
        self,
        file_path: str,
        backup_path: Path,
    ) -> None:
        """
        Restore a file after a failed experiment.
        """

        destination = (PROJECT_ROOT / file_path).resolve()

        shutil.copy2(
            backup_path,
            destination,
        )

    def apply_change(
        self,
        file_path: str,
        content: str,
    ) -> None:
        """
        Validate and apply the proposed modification.
        """

        validate_write(file_path) 

        write_file(
            file_path,
            content,
        )

    def run_training(self) -> str:
        """
        Run the configured training pipeline.
        """

        return run_command(
            "python model/train.py"
        )

    def evaluate(self, model_path: str) -> dict:
        """
        Evaluate the produced model.
        """

        output = run_command(
            f'python model/evaluate.py --model "{model_path}"'
        )

        metrics = self._parse_metrics(output)

        return metrics

    @staticmethod
    def _parse_metrics(output: str) -> dict:
        """
        Extract evaluation metrics from evaluate.py output.
        """

        map50 = None
        map50_95 = None

        for line in output.splitlines():

            if "mAP@0.5:" in line and "0.95" not in line:
                map50 = float(
                    line.split(":")[-1].strip()
                )

            elif "mAP@0.5:0.95:" in line:
                map50_95 = float(
                    line.split(":")[-1].strip()
                )

        if map50 is None or map50_95 is None:
            raise ValueError(
                "Could not parse evaluation metrics.\n"
                f"Evaluation output:\n{output}"
            )

        return {
            "map50": map50,
            "map50_95": map50_95,
        }

    def decide(
        self,
        new_metric: float,
        best_metric: float,
    ) -> str:
        """
        Decide whether to keep or revert the experiment.
        """

        if new_metric > best_metric:
            return "KEEP"

        return "REVERT"

    def run_one_experiment(
        self,
        baseline_metric: float,
        model_path: str,
    ) -> dict:
        """
        Execute exactly one autonomous experiment.
        """

        print("=" * 60)
        print("AutoResearch: One Experiment")
        print("=" * 60)

        print("\n[1/7] Inspecting project...")

        context = self.inspect()

        print("[2/7] Asking researcher for one experiment...")

        proposal = self.propose_experiment(context)

        print("\nHypothesis:")
        print(proposal["hypothesis"])

        print("\nProposed change:")
        print(proposal["change"])

        file_path = proposal["file"]

        print(
            f"\n[3/7] Validating proposed file: {file_path}"
        )

        validate_write(file_path)

        print("[4/7] Creating backup...")

        backup_path = self.backup_file(file_path)

        experiment_id = (
            self.experiment_manager.create_experiment_id()
        )

        try:

            print("[5/7] Applying experiment...")

            self.apply_change(
                file_path,
                proposal["content"],
            )

            print("[6/7] Running training...")

            training_output = self.run_training()

            print(training_output)

            print("[7/7] Evaluating experiment...")

            metrics = self.evaluate(model_path)

            new_metric = metrics["map50_95"]

            decision = self.decide(
                new_metric,
                baseline_metric,
            )

            if decision == "KEEP":

                status = "kept"

                description = (
                    f"{proposal['hypothesis']}\n"
                    f"Change: {proposal['change']}\n"
                    f"Previous best mAP@0.5:0.95: {baseline_metric:.4f}\n"
                    f"New mAP@0.5:0.95: {new_metric:.4f}\n"
                    f"Decision: {decision}"
                )

                result_path = (
                    self.experiment_manager.save_result(
                        experiment_id=experiment_id,
                        metrics=metrics,
                        status=status,
                        description=description,
                    )
                )

                print("\nDecision: KEEP")
                print(
                    f"Previous best mAP@0.5:0.95: "
                    f"{baseline_metric:.4f}"
                )
                print(
                    f"New mAP@0.5:0.95: "
                    f"{new_metric:.4f}"
                )
                print(
                    f"Result saved to: {result_path}"
                )

                return {
                    "experiment_id": experiment_id,
                    "decision": decision,
                    "metrics": metrics,
                    "result": str(result_path),
                }

            self.restore_file(
                file_path,
                backup_path,
            )

            result_path = (
                self.experiment_manager.save_result(
                    experiment_id=experiment_id,
                    metrics=metrics,
                    status="reverted",
                    description=(
                        f"{proposal['hypothesis']}\n"
                        f"Change: {proposal['change']}\n"
                        f"Previous best mAP@0.5:0.95: {baseline_metric:.4f}\n"
                        f"New mAP@0.5:0.95: {new_metric:.4f}\n"
                        f"Decision: {decision}"
                    ),
                )
            )

            print("\nDecision: REVERT")
            print(
                f"Previous best mAP@0.5:0.95: "
                f"{baseline_metric:.4f}"
            )
            print(
                f"New mAP@0.5:0.95: "
                f"{new_metric:.4f}"
            )
            print(
                f"Result saved to: {result_path}"
            )

            return {
                "experiment_id": experiment_id,
                "decision": decision,
                "metrics": metrics,
                "result": str(result_path),
            }

        except Exception:

            self.restore_file(
                file_path,
                backup_path,
            )

            raise


def main() -> None:
    """
    Entry point for one autonomous research experiment.

    Milestone 3 intentionally requires the current best metric
    and model path as command-line arguments.
    """

    import argparse

    parser = argparse.ArgumentParser(
        description="Run one autonomous research experiment."
    )

    parser.add_argument(
        "--baseline-metric",
        type=float,
        required=True,
        help="Current best mAP@0.5:0.95.",
    )

    parser.add_argument(
        "--model",
        required=True,
        help="Path to the model weights used for evaluation.",
    )

    args = parser.parse_args()

    researcher = AutonomousResearcher()

    result = researcher.run_one_experiment(
        baseline_metric=args.baseline_metric,
        model_path=args.model,
    )

    print("\n===== Experiment Summary =====")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()