#!/usr/bin/env bash
# запускать из корня репозитория c активным .venv
nohup python -m simple_tracker.simple_tracker.main > nohup.out 2>&1 &
echo $! > scripts/.tracker_pid
echo "Started. PID saved to scripts/.tracker_pid"
