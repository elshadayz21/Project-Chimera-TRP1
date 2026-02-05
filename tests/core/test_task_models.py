import pytest
from core.task_models import Goal, Task, Result, TaskStatus
import uuid

def test_goal_creation():
    goal = Goal(description="Test Goal")
    assert goal.id is not None
    assert goal.description == "Test Goal"
    assert goal.created_at is not None

def test_task_creation():
    goal_id = str(uuid.uuid4())
    task = Task(
        goal_id=goal_id,
        type="test_type",
        description="Test Task",
        input_data={"foo": "bar"}
    )
    assert task.goal_id == goal_id
    assert task.status == TaskStatus.PENDING
    assert task.input_data["foo"] == "bar"

def test_task_state_transition():
    task = Task(
        goal_id="g1",
        type="t1",
        description="d1"
    )
    assert task.status == TaskStatus.PENDING
    task.mark_in_progress()
    assert task.status == TaskStatus.IN_PROGRESS

def test_result_creation():
    result = Result(
        task_id="t1",
        output_data={"out": 1},
        execution_time_ms=100.0
    )
    assert result.is_valid is None
    
    result.mark_valid("Good")
    assert result.is_valid is True
    assert result.validation_notes == "Good"

    result.mark_invalid("Bad")
    assert result.is_valid is False
    assert result.validation_notes == "Bad"
