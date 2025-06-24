#!/bin/bash
while true; do
    if ! pgrep -f run_gbets_cashout.py >/dev/null; then
        cd /home/g0d/Workspace/Projects/betting/
        source venv/bin/activate
        python run_gbets_cashout.py
    fi
    sleep 2
done
