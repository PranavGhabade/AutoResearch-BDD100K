from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Files/directories the research agent is allowed to modify.
ALLOWED_WRITE_DIRECTORIES = {
    "model",
    "research/experiments",
}


# Files/directories that must never be modified by the agent.
PROTECTED_PATHS = {
    "agent/guardrails.py",
    "model/evaluate.py",
    "research/results",
}


def is_path_allowed(file_path: str) -> bool:
    """
    Check whether a path is inside the project and allowed to be modified.
    """

    path = (PROJECT_ROOT / file_path).resolve()

    if not path.is_relative_to(PROJECT_ROOT):
        return False

    relative_path = str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")

    if relative_path in PROTECTED_PATHS:
        return False

    for directory in ALLOWED_WRITE_DIRECTORIES:
        directory_path = PROJECT_ROOT / directory

        if path.is_relative_to(directory_path.resolve()):
            return True

    return False


def validate_write(file_path: str) -> None:
    """
    Raise an error if the agent attempts to modify a protected path.
    """

    if not is_path_allowed(file_path):
        raise PermissionError(
            f"Agent is not allowed to modify: {file_path}"
        )