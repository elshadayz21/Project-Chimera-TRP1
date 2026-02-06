"""
WHAT THIS FILE DOES:
    Entrypoint for the Judge Service.
    It demonstrates how to validate results using the JudgeValidator.

WHY IT EXISTS:
    To allows the service to be run as a standalone process.

HOW IT CONNECTS TO CHIMERA ARCHITECTURE:
    - Instantiates JudgeValidator.
    - (Simulation) Receives a Result.
    - Validates it and prints the verdict.
"""

import sys
import os

# Add the project root to sys.path so we can import 'core' and 'apps'
# This assumes the script is run from anywhere, but the structure is fixed:
# project_root/apps/judge/main.py
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.task_models import Result
from apps.judge.validator import JudgeValidator

def main():
    print("⚖️  Starting Judge Service...")
    
    # 1. Instantiate the Validator
    judge = JudgeValidator()
    
    # 2. Simulate receiving a result
    print("📥 Receiving Result for validation...")
    mock_result = Result(
        task_id="mock-task-123",
        output_data={
            "trends": [
                {"title": "Test Trend", "engagement_score": 0.95, "source_url": "http://x.com"}
            ]
        },
        execution_time_ms=150
    )
    print(f"   Result ID: {mock_result.id}")
    
    # 3. Validate
    print("\nmagistrate Assessing...")
    is_valid = judge.validate_result(mock_result)
    
    # 4. Verdict
    print(f"✅ Verdict: {'APPROVED' if is_valid else 'REJECTED'}")
    if is_valid:
        print(f"   Notes: {mock_result.validation_notes}")
    else:
        print(f"   Reason: {mock_result.validation_notes}")

if __name__ == "__main__":
    main()
