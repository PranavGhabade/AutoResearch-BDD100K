import json

from agent.experiment_manager import ExperimentManager
from agent.guardrails import validate_write
from agent.llm_client import GeminiLLM
from agent.tools import (
    list_files,
    read_file,
    run_command,
    write_file,
)


class ResearchAgent:
    def __init__(
        self,
        max_llm_calls: int = 3,
        llm=None,
    ):
        self.llm = llm or GeminiLLM()
        self.max_llm_calls = max_llm_calls
        self.llm_calls = 0

        self.experiment_manager = ExperimentManager()

    def _ask_llm(self, prompt: str) -> dict:
        """
        Ask the LLM for one structured decision.
        """

        if self.llm_calls >= self.max_llm_calls:
            raise RuntimeError(
                "LLM call limit reached."
            )

        self.llm_calls += 1

        response = self.llm.generate(prompt)

        try:
            decision = json.loads(response)

        except json.JSONDecodeError as exc:
            raise ValueError(
                "LLM returned invalid JSON:\n"
                f"{response}"
            ) from exc

        if not isinstance(decision, dict):
            raise ValueError(
                "LLM response must be a JSON object."
            )

        return decision

    def execute_action(
        self,
        decision: dict,
    ) -> str:
        """
        Validate and execute one agent action.
        """

        action = decision.get("action")

        if action == "list_files":
            path = decision.get(
                "path",
                ".",
            )

            return "\n".join(
                list_files(path)
            )

        if action == "read_file":
            path = decision.get("path")

            if not path:
                raise ValueError(
                    "read_file requires a path."
                )

            return read_file(path)

        if action == "write_file":
            path = decision.get("path")
            content = decision.get("content")

            if not path:
                raise ValueError(
                    "write_file requires a path."
                )

            if content is None:
                raise ValueError(
                    "write_file requires content."
                )

            validate_write(path)

            return write_file(
                path,
                content,
            )

        if action == "run_command":
            command = decision.get("command")

            if not command:
                raise ValueError(
                    "run_command requires a command."
                )

            return run_command(command)

        if action == "finish":
            return decision.get(
                "message",
                "Agent finished.",
            )

        raise ValueError(
            f"Unknown agent action: {action}"
        )

    def inspect_project(self) -> str:
        """
        Ask the LLM to inspect the project.
        """

        prompt = """
You are an ML research agent.

Your current task is to inspect the project.

Respond with ONLY valid JSON.

Allowed actions:

{
    "action": "list_files",
    "path": "."
}

or:

{
    "action": "read_file",
    "path": "README.md"
}

or:

{
    "action": "finish",
    "message": "Your conclusion"
}

Do not modify files.
Do not execute commands.

Start by listing the project files.
"""

        decision = self._ask_llm(prompt)

        return self.execute_action(decision)