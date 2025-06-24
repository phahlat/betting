import players.gbets_player_bet_combo as bet_combo
import time
import threading
import os

if __name__ == "__main__":
    try:
        while True:
            with open("data/teams.canbet.data", "r") as __file:
                __can_bet = __file.readline()
                if __can_bet.strip() == "True":
                    break

                print(
                    f"\r[ {time.strftime('%Y-%m-%d %H:%M:%S')} ] CAN BET??? {__can_bet.strip() + ' ' * 10}",
                    end="",
                )
                __file.close()
                time.sleep(5)

        bet_combo.bet_combo_lists()

        # clear combo
        with open("data/teams.combo.data", "w") as __file:
            __file.close()

        print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ] Exit Combo!")
        exit(0)
    except Exception as e:
        os.system("clear")  # Clear the console
        print(f"An error occurred: {e}")
        exit(0)


# start processes for betting split and combinations
# track why max of 2 teams are bet in a combination of 5
