"""
WHAT THIS FILE DOES:
    Defines the core data structures (Pydantic models) shared across the Chimera ecosystem.
    It acts as the "contract" for data exchange between Planner, Worker, and Judge.

WHY IT EXISTS:
    To ensure strict type safety and consistent data validation across all autonomous agents.
    Without this, services would speak different languages.

HOW IT CONNECTS TO CHIMERA ARCHITECTURE:
    - Planner produces `Task` objects from a `Goal`.
    - Worker consumes `Task` objects and produces `Result` objects.
    - Judge consumes `Result` objects and validates them.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class TaskStatus(str, Enum):
    """
    Enum representing the lifecycle state of a Task.
    """
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Goal(BaseModel):
    """
    ROLE IN SWARM:
        Represents the high-level objective provided by a human or a superior agent.
        The Planner's job is to decompose this into executable Tasks.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str = Field(..., description="High-level description of what needs to be achieved.")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Contextual data for the goal.")

class Task(BaseModel):
    """
    ROLE IN SWARM:
        Atomic unit of work created by the Planner.
        It contains everything a Worker needs to know to execute a specific action.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    goal_id: str = Field(..., description="Reference to the parent Goal.")
    type: str = Field(..., description="The type of task (e.g., 'fetch_trends', 'generate_content').")
    description: str = Field(..., description="Detailed instructions for the worker.")
    input_data: Dict[str, Any] = Field(default_factory=dict, description="Parameters required for execution.")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def mark_in_progress(self):
        """
        WHY: To track lifecycle state changes.
        WHEN: Called by the Worker when execution begins.
        WHO CALLS: apps.worker.executor.WorkerExecutor
        """
        self.status = TaskStatus.IN_PROGRESS

class Result(BaseModel):
    """
    ROLE IN SWARM:
        The output produced by a Worker after executing a Task.
        It is the subject of validation by the Judge.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str = Field(..., description="Reference to the Task that generated this result.")
    output_data: Dict[str, Any] = Field(..., description="The actual data produced (e.g., trend list, text content).")
    execution_time_ms: float = Field(..., description="Time taken to execute the task.")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_valid: Optional[bool] = Field(default=None, description="Validation status set by the Judge.")
    validation_notes: Optional[str] = Field(default=None, description="Comments from the Judge.")

    def mark_valid(self, notes: str = ""):
        """
        WHY: To finalize the result as acceptable.
        WHEN: Called by the Judge after passing validation rules.
        WHO CALLS: apps.judge.validator.JudgeValidator
        """
        self.is_valid = True
        self.validation_notes = notes

    def mark_invalid(self, reason: str):
        """
        WHY: To reject the result and potentially trigger a retry.
        WHEN: Called by the Judge when validation fails.
        WHO CALLS: apps.judge.validator.JudgeValidator
        """
        self.is_valid = False
        self.validation_notes = reason
