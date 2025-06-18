import players.gbets_player_bet_combo as bet_combo
import time
import threading
import os

if __name__ == "__main__":
    __WAIT_PERIOD = 60 * 30  # 30 minutes
    while True:
        try:
            bet_combo.bet_combo_lists()
            print(
                f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ] Waiting for the next combo round... in {__WAIT_PERIOD // 60} minutes."
            )
            
            # clear combo
            with open("teams.combo.data", "w") as __file:
                __file.close()
                
            time.sleep(__WAIT_PERIOD)
        except Exception as e:
            print(f"An error occurred: {e}")
            os.system("clear")  # Clear the console
            time.sleep(__WAIT_PERIOD)


# start processes for betting split and combinations
# track why max of 2 teams are bet in a combination of 5
