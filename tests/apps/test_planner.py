import pytest
from apps.planner.service import PlannerService
from core.task_models import Goal

def test_planner_create_plan_trend():
    planner = PlannerService()
    goal = Goal(description="Find latest tiktok trends")
    
    tasks = planner.create_plan(goal)
    
    assert len(tasks) == 2
    assert tasks[0].type == "fetch_trends"
    assert tasks[0].input_data["platform"] == "tiktok"
    assert tasks[1].type == "analyze_trends"

def test_planner_create_plan_generic():
    planner = PlannerService()
    goal = Goal(description="Write a poem")
    
    tasks = planner.create_plan(goal)
    
    assert len(tasks) == 1
    assert tasks[0].type == "generic_research"
    assert tasks[0].goal_id == goal.id
