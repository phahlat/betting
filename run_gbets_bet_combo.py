import players.gbets_player_bet_combo as bet_combo
import time
import threading

if __name__ == "__main__":
    __WAIT_PERIOD = 60 * 30  # 30 minutes
    try:
        while True:
            bet_combo.bet_combo_lists()
            print(
                f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ] Waiting for the next combo round..."
            )
            time.sleep(__WAIT_PERIOD)
    except:
        raise


# start processes for betting split and combinations
# track why max of 2 teams are bet in a combination of 5
