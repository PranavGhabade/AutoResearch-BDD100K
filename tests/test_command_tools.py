import pytest

from agent.tools import (
    is_command_allowed,
    run_command,
)


def test_python_command_allowed():
    assert is_command_allowed(
        "python --version"
    )


def test_pytest_command_allowed():
    assert is_command_allowed(
        "pytest tests -v"
    )


def test_git_command_blocked():
    assert not is_command_allowed(
        "git push origin main"
    )


def test_powershell_command_blocked():
    assert not is_command_allowed(
        "powershell Remove-Item test.txt"
    )


def test_remove_item_blocked():
    assert not is_command_allowed(
        "Remove-Item test.txt"
    )


def test_empty_command_blocked():
    assert not is_command_allowed("")


def test_run_python_command():
    result = run_command(
        "python --version"
    )

    assert "Python" in result


def test_blocked_command_raises_error():
    with pytest.raises(PermissionError):
        run_command(
            "git push origin main"
        )