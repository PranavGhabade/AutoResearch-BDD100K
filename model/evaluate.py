from pathlib import Path

import yaml
from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "model" / "config.yaml"


def load_config() -> dict:
    """
    Load the experiment configuration.
    """

    with CONFIG_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        return yaml.safe_load(file)


def evaluate(model_path: str) -> dict:
    """
    Evaluate a trained YOLO model on the configured dataset.
    """

    config = load_config()

    model = YOLO(model_path)

    dataset = PROJECT_ROOT / config["dataset"]["data_yaml"]

    image_size = config["training"]["image_size"]

    results = model.val(
        data=str(dataset),
        imgsz=image_size,
        split="val",
    )

    metrics = {
        "map50": float(
            results.box.map50
        ),
        "map50_95": float(
            results.box.map
        ),
    }

    return metrics


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Evaluate a trained YOLO model."
    )

    parser.add_argument(
        "--model",
        required=True,
        help="Path to trained YOLO model weights.",
    )

    args = parser.parse_args()

    metrics = evaluate(args.model)

    print("\n===== Evaluation Results =====")
    print(f"mAP@0.5:      {metrics['map50']:.4f}")
    print(
        f"mAP@0.5:0.95: {metrics['map50_95']:.4f}"
    )
    print("==============================")