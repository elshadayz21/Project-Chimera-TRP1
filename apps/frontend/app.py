"""
WHAT THIS FILE DOES:
    Provides a Simple Web UI (Frontend) for the Chimera Swarm.
    It allows users to interact with the backend agents without writing code.

WHY IT EXISTS:
    To demonstrate the "Planner -> Worker -> Judge" loop visually.
    It enables testing input variations and seeing immediate results.

HOW IT CONNECTS TO CHIMERA ARCHITECTURE:
    - Imports PlannerService, WorkerExecutor, JudgeValidator.
    - Captures user input (Goal).
    - Orchestrates the full execution flow.
    - Displays outputs from each stage.
"""

import streamlit as st
import sys
import os
import time

# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------
# Fix import path to allow running from any directory
# This ensures 'core', 'apps' are importable
current_dir = os.path.dirname(os.path.abspath(__file__)) # .../apps/frontend
root_dir = os.path.dirname(os.path.dirname(current_dir)) # .../Project-Chimera-TRP1
sys.path.append(root_dir)

from core.task_models import Goal, Task, Result
from apps.planner.service import PlannerService
from apps.worker.executor import WorkerExecutor
from apps.judge.validator import JudgeValidator

# ------------------------------------------------------------------
# UI LAYOUT
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Project Chimera | Swarm Control",
    page_icon="🦁",
    layout="wide"
)

st.title("🦁 Project Chimera Swarm Control")
st.markdown("### Spec-Driven Autonomous Agent Infrastructure")

# Sidebar for Info
with st.sidebar:
    st.header("Architecture Mode")
    st.info("""
    **Planner**: Decomposes goals.
    
    **Worker**: Executes tasks.
    
    **Judge**: Validates output.
    """)
    st.divider()
    model_choice = st.selectbox("LLM Model (Simulation)", ["mock-model", "gpt-4", "claude-3-opus"])
    st.caption("Currently using Mock Logic.")

# ------------------------------------------------------------------
# INPUT SECTION
# ------------------------------------------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    goal_text = st.text_area(
        "Enter your Goal:",
        value="Fetch and analyze latest TikTok trends in the US regarding AI Agents.",
        height=100
    )

with col2:
    st.write("## ")
    run_btn = st.button("🚀 EXECUTE SWARM", type="primary", use_container_width=True)

# ------------------------------------------------------------------
# EXECUTION LOGIC
# ------------------------------------------------------------------
if run_btn and goal_text:
    st.divider()
    
    # containers for each stage
    planner_container = st.container()
    worker_container = st.container()
    
    # 1. PLANNER
    with planner_container:
        st.subheader("1. 🧠 Planner Agent")
        with st.spinner("Analyzing goal..."):
            time.sleep(0.5) # UX Loading
            planner = PlannerService()
            goal = Goal(description=goal_text)
            tasks = planner.create_plan(goal)
            
        st.success(f"Goal decomposed into **{len(tasks)} tasks**.")
        
        # Visualize Plan
        for i, task in enumerate(tasks, 1):
            with st.expander(f"Task {i}: {task.type}", expanded=True):
                st.write(task.description)
                st.caption(f"Input: {task.input_data}")

    # 2. WORKER & JUDGE LOOP
    with worker_container:
        st.subheader("2. 🛠️ Worker & ⚖️ Judge Execution")
        
        worker = WorkerExecutor()
        judge = JudgeValidator()
        
        progress_bar = st.progress(0)
        
        for i, task in enumerate(tasks):
            col_worker, col_judge = st.columns(2)
            
            # WORKER STEP
            with col_worker:
                with st.spinner(f"Executing Task {i+1}..."):
                    time.sleep(0.8) # UX simulation
                    result = worker.execute_task(task)
                
                st.markdown(f"**✅ Task {i+1} Complete**")
                st.json(result.output_data)
                st.caption(f"Time: {result.execution_time_ms:.2f}ms")

            # JUDGE STEP
            with col_judge:
                with st.spinner("Validating..."):
                    time.sleep(0.2)
                    is_valid = judge.validate_result(result)
                
                if is_valid:
                    st.success("✅ **APPROVED**")
                    st.write(result.validation_notes)
                else:
                    st.error("❌ **REJECTED**")
                    st.error(result.validation_notes)
            
            st.divider()
            progress_bar.progress((i + 1) / len(tasks))

    st.balloons()
