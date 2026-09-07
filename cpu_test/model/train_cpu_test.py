from pathlib import Path

import yaml
from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "model" / "cpu_test_config.yaml"


def load_config() -> dict:
    """
    Load the CPU test configuration.
    """

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def build_model(config: dict) -> YOLO:
    """
    Create the YOLO model specified by the CPU test configuration.
    """

    model_name = config["model"]["name"]
    pretrained = config["model"]["pretrained"]

    if pretrained:
        model_file = f"{model_name}.pt"
        return YOLO(model_file)

    model_file = f"{model_name}.yaml"
    return YOLO(model_file)


def train() -> None:
    """
    Run the CPU test training.
    """

    config = load_config()

    model = build_model(config)

    dataset = PROJECT_ROOT / config["dataset"]["data_yaml"]

    training = config["training"]
    output = config["output"]

    model.train(
        data=str(dataset),
        imgsz=training["image_size"],
        batch=training["batch_size"],
        epochs=training["epochs"],
        workers=training["workers"],
        seed=training["seed"],
        device="cpu",
        project=str(
            PROJECT_ROOT / output["directory"]
        ),
        name="yolov8n_cpu_test",
    )


if __name__ == "__main__":
    train()
    