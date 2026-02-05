"""
WHAT THIS FILE DOES:
    Verifies the end-to-end flow of the Chimera Swarm Architecture.
    It simulates the lifecycle of a Goal as it passes through the Planner, Worker, and Judge.

WHY IT EXISTS:
    To ensure all components (Planner, Worker, Judge) interact correctly using the shared
    Core Models. It serves as an integration test.

HOW IT CONNECTS TO CHIMERA ARCHITECTURE:
    1. Planner: Goal -> Tasks
    2. Worker: Task -> Result
    3. Judge: Result -> Verdict
"""

import sys
import os

# Ensure project root is in path
sys.path.append(os.getcwd())

from core.task_models import Goal
from apps.planner.service import PlannerService
from apps.worker.executor import WorkerExecutor
from apps.judge.validator import JudgeValidator

def verify_swarm():
    print("🧪 Starting Swarm Verification...\n")

    # 1. Initialize Agents
    planner = PlannerService()
    worker = WorkerExecutor()
    judge = JudgeValidator()

    # 2. Define a Goal
    goal = Goal(description="Fetch and analyze latest TikTok trends in the US regarding AI Agents.")
    print(f"1️⃣  GOAL CREATED: {goal.description}")

    # 3. Plan
    tasks = planner.create_plan(goal)
    print(f"2️⃣  PLANNER: Created {len(tasks)} tasks.")
    
    for task in tasks:
        print(f"\n   👉 Processing Task: {task.type}")
        
        # 4. Work
        result = worker.execute_task(task)
        print(f"      3️⃣  WORKER: Executed in {result.execution_time_ms:.2f}ms")
        
        # 5. Judge
        is_valid = judge.validate_result(result)
        status = "✅ APPROVED" if is_valid else "❌ REJECTED"
        print(f"      4️⃣  JUDGE: {status}")
        
        if not is_valid:
            print(f"         Reason: {result.validation_notes}")

    print("\n✨ Verification Complete!")

if __name__ == "__main__":
    verify_swarm()
