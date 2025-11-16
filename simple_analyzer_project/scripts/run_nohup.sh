#!/usr/bin/env bash
# запускать из корня репозитория с активным .venv
nohup python -m simple_analyzer_project.simple_analyzer.main > simple_analyzer_project/nohup.out 2>&1 &
echo $! > simple_analyzer_project/scripts/.analyzer_pid
echo "Started. PID saved to simple_analyzer_project/scripts/.analyzer_pid"
