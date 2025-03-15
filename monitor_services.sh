#!/bin/bash

# Function to check and restart a process
restart_if_not_running() {
    PROCESS_NAME=$1
    START_COMMAND=$2

    if ! pgrep -f "$PROCESS_NAME" > /dev/null; then
        echo "$(date): $PROCESS_NAME is not running! Restarting..."
        cd /home/quypham8633/Cloud-Based-Linux-Server/ && eval "$START_COMMAND &"
    else
        echo "$(date): $PROCESS_NAME is running."
    fi
}

# Check and restart agent.py
restart_if_not_running "agent.py" "python3 agent.py"

# Check and restart dashboard.py
restart_if_not_running "dashboard.py" "python3 dashboard.py"


