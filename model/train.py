from pathlib import Path

import yaml
from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "model" / "config.yaml"


def load_config() -> dict:
    """
    Load the experiment configuration.
    """

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def build_model(config: dict) -> YOLO:
    """
    Create the YOLO model specified by the configuration.

    If pretrained is True, load pretrained weights.
    If pretrained is False, initialize the model from its
    architecture configuration.
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
    Train the configured YOLO model.
    """

    config = load_config()

    model = build_model(config)

    dataset = PROJECT_ROOT / config["dataset"]["data_yaml"]

    training = config["training"]

    model.train(
        data=str(dataset),
        imgsz=training["image_size"],
        batch=training["batch_size"],
        epochs=training["epochs"],
        workers=training["workers"],
        seed=training["seed"],
        project=str(
            PROJECT_ROOT / "research" / "runs"
        ),
        name="baseline",
    )


if __name__ == "__main__":
    train()