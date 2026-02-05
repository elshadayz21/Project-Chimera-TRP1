"""
WHAT THIS FILE DOES:
    Entrypoint for the Worker Service.
    It demonstrates how to execute tasks using the WorkerExecutor.

WHY IT EXISTS:
    To allows the service to be run as a standalone process.

HOW IT CONNECTS TO CHIMERA ARCHITECTURE:
    - Instantiates WorkerExecutor.
    - (Simulation) Receives tasks (from 'queue').
    - Processes them and prints results.
"""

from core.task_models import Task
from apps.worker.executor import WorkerExecutor

def main():
    print("🛠️  Starting Worker Service...")
    
    # 1. Instantiate the Executor
    worker = WorkerExecutor()
    
    # 2. Simulate pulling a task from queue
    print("📥 Polling Task Queue...")
    mock_task = Task(
        goal_id="mock-goal-123",
        type="fetch_trends",
        description="Fetch latest trends",
        input_data={"platform": "tiktok"}
    )
    print(f"   Received Task: {mock_task.id} ({mock_task.type})")
    
    # 3. Execute Task
    print("\n⚡ Executing Task...")
    result = worker.execute_task(mock_task)
    
    # 4. Report Result
    print(f"✅ Execution Completed in {result.execution_time_ms:.2f}ms")
    print(f"   Output Keys: {list(result.output_data.keys())}")
    print(f"   Status: {mock_task.status}")

if __name__ == "__main__":
    main()
