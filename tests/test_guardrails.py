import pytest

from agent.guardrails import validate_write, is_path_allowed


def test_allowed_model_file():
    assert is_path_allowed("model/train.py")


def test_allowed_experiment_file():
    assert is_path_allowed("research/experiments/experiment_01.py")


def test_protected_evaluation_file():
    assert not is_path_allowed("model/evaluate.py")


def test_protected_results_directory():
    assert not is_path_allowed("research/results/result.json")


def test_outside_project_is_blocked():
    assert not is_path_allowed("../secret.txt")


def test_validate_write_rejects_protected_file():
    with pytest.raises(PermissionError):
        validate_write("model/evaluate.py")