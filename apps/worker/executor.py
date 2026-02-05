"""
WHAT THIS FILE DOES:
    Implements the Worker Executor logic.
    The Worker is the "Hands" of the system, performing the actual actions defined by the Task.

WHY IT EXISTS:
    To execute unit tasks reliably and report results.
    It isolates execution complexity (API calls, data processing) from decision making.

HOW IT CONNECTS TO CHIMERA ARCHITECTURE:
    - Input: core.task_models.Task
    - Output: core.task_models.Result
    - Upstream: Receives Tasks from Planner (via queue).
    - Downstream: Sends Results to Judge.
"""

import time
from datetime import datetime
from typing import Dict, Any

from core.task_models import Task, Result, TaskStatus

class WorkerExecutor:
    """
    ROLE IN SWARM:
        The "Hands" or "Agent" that performs work.
        It routes tasks to specific handlers (skills) based on task type.
    """

    def execute_task(self, task: Task) -> Result:
        """
        WHY: To perform the actual work described in the task.
        WHEN: Called when a task is picked up from the queue.
        WHO CALLS: apps.worker.main (Entrypoint)
        """
        task.mark_in_progress()
        start_time = time.time()
        
        try:
            # Routing logic to find the right skill/function
            if task.type == "fetch_trends":
                output = self._handle_fetch_trends(task.input_data)
            elif task.type == "analyze_trends":
                output = self._handle_analyze_trends(task.input_data)
            else:
                output = self._handle_generic_task(task)
            
            task.status = TaskStatus.COMPLETED
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            output = {"error": str(e)}

        execution_time = (time.time() - start_time) * 1000 # ms

        return Result(
            task_id=task.id,
            output_data=output,
            execution_time_ms=execution_time
        )

    def _handle_fetch_trends(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Specific handler for trend fetching.
        In a real app, this would call the 'TrendFetchSkill'.
        """
        # Mocking the Trend Fetch behavior based on specs/api/trend_fetch.yaml
        return {
            "trends": [
                {
                    "title": "AI Agents 101",
                    "engagement_score": 0.95,
                    "source_url": "https://tiktok.com/@ai/123"
                },
                {
                    "title": "Python vs Rust",
                    "engagement_score": 0.82,
                    "source_url": "https://youtube.com/watch?v=abc"
                }
            ]
        }

    def _handle_analyze_trends(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        handler for analysis
        """
        return {"analysis_report": "High engagement detected for AI topics."}

    def _handle_generic_task(self, task: Task) -> Dict[str, Any]:
        """
        Fallback handler.
        """
        return {"message": f"Executed generic task: {task.description}"}
