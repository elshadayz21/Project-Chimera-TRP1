@echo off
REM Simple launcher for Project Chimera Frontend
REM This script runs the Streamlit app with proper Python module invocation

echo Starting Project Chimera Swarm Control...
echo.
echo The web interface will open at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

python -m streamlit run apps\frontend\app.py

pause
