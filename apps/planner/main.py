"""
WHAT THIS FILE DOES:
    Entrypoint for the Planner Service.
    It demonstrates how to instantiate the Planner and generate a plan.

WHY IT EXISTS:
    To allows the service to be run as a standalone process (e.g., via Docker or CLI).

HOW IT CONNECTS TO CHIMERA ARCHITECTURE:
    - Instantiates PlannerService.
    - (Simulation) Creates a Goal.
    - (Simulation) Prints the resulting Plan.
"""

import sys
import os

# Add the project root to sys.path so we can import 'core'
# This assumes the script is run from anywhere, but the structure is fixed:
# project_root/apps/planner/main.py
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.task_models import Goal
from apps.planner.service import PlannerService

def main():
    print("🚀 Starting Planner Service...")
    
    # 1. Instantiate the Service
    planner = PlannerService()
    
    # 2. Receive a Goal (Mocking an event or API call)
    print("📝 Receiving new Goal...")
    goal = Goal(description="Fetch and analyze latest TikTok trends in the US.")
    print(f"   Goal ID: {goal.id}")
    print(f"   Description: {goal.description}")
    
    # 3. Create a Plan
    print("\n🧠 Generating Plan...")
    tasks = planner.create_plan(goal)
    
    # 4. Output the Plan
    print(f"✅ Plan created with {len(tasks)} tasks:")
    for i, task in enumerate(tasks, 1):
        print(f"   {i}. [{task.type}] {task.description}")

if __name__ == "__main__":
    main()
