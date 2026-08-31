import pytest

from agent.controller import ResearchAgent


class FakeLLM:
    def __init__(self, response: str):
        self.response = response

    def generate(self, prompt: str) -> str:
        return self.response


def test_list_files_action():
    llm = FakeLLM(
        '{"action": "list_files", "path": "agent"}'
    )

    agent = ResearchAgent(llm=llm)

    result = agent.inspect_project()

    normalized_result = result.replace(
        "\\",
        "/",
    )

    assert "agent/controller.py" in normalized_result
    assert "agent/llm_client.py" in normalized_result


def test_read_file_action():
    llm = FakeLLM(
        '{"action": "read_file", "path": "README.md"}'
    )

    agent = ResearchAgent(llm=llm)

    result = agent.inspect_project()

    assert isinstance(result, str)


def test_run_command_action():
    llm = FakeLLM(
        '{"action": "run_command", "command": "python --version"}'
    )

    agent = ResearchAgent(llm=llm)

    result = agent.inspect_project()

    assert "Python" in result
    assert "exit_code=0" in result


def test_blocked_command_action():
    llm = FakeLLM(
        '{"action": "run_command", "command": "git push origin main"}'
    )

    agent = ResearchAgent(llm=llm)

    with pytest.raises(PermissionError):
        agent.inspect_project()


def test_protected_file_cannot_be_modified():
    llm = FakeLLM(
        """
        {
            "action": "write_file",
            "path": "model/evaluate.py",
            "content": "malicious change"
        }
        """
    )

    agent = ResearchAgent(llm=llm)

    with pytest.raises(PermissionError):
        agent.inspect_project()