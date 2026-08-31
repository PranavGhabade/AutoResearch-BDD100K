from pathlib import Path
import shlex
import subprocess


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def read_file(file_path: str) -> str:
    """
    Read a text file inside the project directory.
    """

    path = (PROJECT_ROOT / file_path).resolve()

    if not path.is_relative_to(PROJECT_ROOT):
        raise PermissionError(
            "Access outside the project directory is not allowed."
        )

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Not a file: {file_path}"
        )

    return path.read_text(
        encoding="utf-8"
    )


def write_file(
    file_path: str,
    content: str,
) -> str:
    """
    Write a text file inside the project directory.
    """

    path = (PROJECT_ROOT / file_path).resolve()

    if not path.is_relative_to(PROJECT_ROOT):
        raise PermissionError(
            "Access outside the project directory is not allowed."
        )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        content,
        encoding="utf-8",
    )

    return f"Successfully wrote {file_path}"


def list_files(
    directory: str = ".",
) -> list[str]:
    """
    List project files while ignoring virtual environments,
    cache directories, and Git metadata.
    """

    path = (PROJECT_ROOT / directory).resolve()

    if not path.is_relative_to(PROJECT_ROOT):
        raise PermissionError(
            "Access outside the project directory is not allowed."
        )

    if not path.exists():
        raise FileNotFoundError(
            f"Directory not found: {directory}"
        )

    if not path.is_dir():
        raise ValueError(
            f"Not a directory: {directory}"
        )

    ignored_directories = {
        ".venv",
        ".git",
        "__pycache__",
    }

    files = []

    for file in path.rglob("*"):
        if not file.is_file():
            continue

        relative_path = file.relative_to(
            PROJECT_ROOT
        )

        if any(
            part in ignored_directories
            for part in relative_path.parts
        ):
            continue

        files.append(
            relative_path.as_posix()
        )

    return files


def is_command_allowed(command: str) -> bool:
    """
    Check whether a command is allowed to run.

    The research agent should only be able to run
    commands required for testing and ML experiments.
    """

    try:
        parts = shlex.split(
            command,
            posix=False,
        )
    except ValueError:
        return False

    if not parts:
        return False

    command_name = parts[0].lower()

    allowed_commands = {
        "python",
        "python.exe",
        "pytest",
        "pytest.exe",
    }

    if command_name not in allowed_commands:
        return False

    blocked_tokens = {
        "del",
        "erase",
        "format",
        "shutdown",
        "restart-computer",
        "remove-item",
        "rmdir",
        "rd",
        "git",
        "powershell",
        "cmd",
        "curl",
        "wget",
    }

    normalized_command = command.lower()

    for token in blocked_tokens:
        if token in normalized_command:
            return False

    return True


def run_command(
    command: str,
    timeout: int = 300,
) -> str:
    """
    Execute an approved command from the project root.
    """

    if not is_command_allowed(command):
        raise PermissionError(
            f"Command is not allowed: {command}"
        )

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    output = result.stdout

    if result.stderr:
        output += (
            "\n[stderr]\n"
            + result.stderr
        )

    output += (
        f"\n[exit_code={result.returncode}]"
    )

    return output