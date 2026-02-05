import pytest
from apps.worker.executor import WorkerExecutor
from core.task_models import Task, TaskStatus

def test_worker_execute_fetch_trends():
    worker = WorkerExecutor()
    task = Task(
        goal_id="g1",
        type="fetch_trends",
        description="fetch",
        input_data={"platform": "tiktok"}
    )
    
    result = worker.execute_task(task)
    
    assert task.status == TaskStatus.COMPLETED
    assert result.task_id == task.id
    assert "trends" in result.output_data
    assert len(result.output_data["trends"]) > 0

def test_worker_execute_generic():
    worker = WorkerExecutor()
    task = Task(
        goal_id="g1",
        type="unknown_type",
        description="do something"
    )
    
    result = worker.execute_task(task)
    
    assert task.status == TaskStatus.COMPLETED
    assert "message" in result.output_data
