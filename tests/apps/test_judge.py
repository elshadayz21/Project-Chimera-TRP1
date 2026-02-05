import pytest
from apps.judge.validator import JudgeValidator
from core.task_models import Result

def test_judge_validate_trends_valid():
    judge = JudgeValidator()
    result = Result(
        task_id="t1",
        output_data={
            "trends": [
                {"title": "t1", "engagement_score": 0.5, "source_url": "u1"}
            ]
        },
        execution_time_ms=10
    )
    
    is_valid = judge.validate_result(result)
    assert is_valid is True
    assert result.is_valid is True

def test_judge_validate_trends_invalid_score():
    judge = JudgeValidator()
    result = Result(
        task_id="t1",
        output_data={
            "trends": [
                {"title": "t1", "engagement_score": 1.5, "source_url": "u1"}
            ]
        },
        execution_time_ms=10
    )
    
    is_valid = judge.validate_result(result)
    assert is_valid is False
    assert "out of range" in result.validation_notes

def test_judge_validate_trends_empty():
    judge = JudgeValidator()
    result = Result(
        task_id="t1",
        output_data={"trends": []},
        execution_time_ms=10
    )
    
    is_valid = judge.validate_result(result)
    assert is_valid is False
    assert "empty" in result.validation_notes
