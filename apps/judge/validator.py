"""
WHAT THIS FILE DOES:
    Implements the Judge Validator logic.
    The Judge is the "Critic" or "Quality Assurance" layer. It ensures that the work
    performed by the Worker meets the requirements set by the Planner (or the Spec).

WHY IT EXISTS:
    To prevent hallucinated, incomplete, or incorrect data from propagating through the system.
    It enforces the "Contract Tests" at runtime.

HOW IT CONNECTS TO CHIMERA ARCHITECTURE:
    - Input: core.task_models.Result
    - Output: Boolean (Valid/Invalid) + Feedback
    - Upstream: Receives Results from Worker.
    - Downstream: Approves completion or triggers feedback loop to Planner/Worker.
"""

from typing import Dict, Any, Optional
from core.task_models import Result

class JudgeValidator:
    """
    ROLE IN SWARM:
        The "Conscience" and "Quality Control".
        It uses deterministic checks and (future) LLM evaluation to grade work.
    """

    def validate_result(self, result: Result, criteria: Optional[Dict[str, Any]] = None) -> bool:
        """
        WHY: To assess whether the result is acceptable.
        WHEN: Called immediately after a Worker produces a Result.
        WHO CALLS: apps.judge.main (Entrypoint)
        """
        if criteria is None:
            criteria = {}

        # 1. Basic structural validation
        if not result.output_data:
            result.mark_invalid("Result output is empty.")
            return False

        if "error" in result.output_data:
             result.mark_invalid(f"Worker reported error: {result.output_data['error']}")
             return False

        # 2. Specific validation logic based on content
        # In a real system, we might look up the Task type to know which rules to apply.
        # Here we infer from data structure for the skeleton.
        
        is_trend_result = "trends" in result.output_data
        
        if is_trend_result:
            return self._validate_trends(result)
            
        # Default pass for generic tasks if no error
        result.mark_valid("Generic task completed successfully.")
        return True

    def _validate_trends(self, result: Result) -> bool:
        """
        Validates trend fetch results against the schema constraints.
        """
        trends = result.output_data.get("trends", [])
        
        if not isinstance(trends, list):
            result.mark_invalid("Trends must be a list.")
            return False
            
        if len(trends) == 0:
            result.mark_invalid("Trend list is empty.")
            return False

        for trend in trends:
            # Check for required fields
            if "engagement_score" not in trend:
                result.mark_invalid("Missing engagement_score in trend.")
                return False
            
            # Check value constraints
            score = trend["engagement_score"]
            if not (0 <= score <= 1):
                result.mark_invalid(f"Engagement score {score} out of range [0,1].")
                return False

        result.mark_valid(f"Validated {len(trends)} trends successfully.")
        return True
