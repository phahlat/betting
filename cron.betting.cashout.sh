#!/bin/bash
while true; do
    if ! pgrep -f run_gbets_cashout.py >/dev/null; then
        cd /Users/g0d/Workspace/projects/betting;
        source venv/bin/activate;
        python run_gbets_cashout.py;
    fi
    sleep 1
done