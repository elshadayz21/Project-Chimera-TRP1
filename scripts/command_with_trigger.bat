@echo off
setlocal enabledelayedexpansion
set "CMD_STR=%*"
python "%~dp0log_triggers.py" --type passage --message "Command: %CMD_STR%" >nul 2>nul
%*
