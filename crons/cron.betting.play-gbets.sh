#!/bin/bash
while true; do
    if ! pgrep -f run_gbets_bet_split.py >/dev/null; then
        cd /home/g0d/Workspace/Projects/betting/
        source venv/bin/activate
        python run_gbets_bet_split.py
    fi
    sleep 1

    if ! pgrep -f run_gbets_bet_combo.py >/dev/null; then
        cd /home/g0d/Workspace/Projects/betting/
        source venv/bin/activate
        python run_gbets_bet_combo.py
    fi
    sleep 1
done