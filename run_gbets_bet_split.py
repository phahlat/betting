import players.gbets_player_bet_split as bet_split
import time
import os
import threading

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

        bet_split.bet_splitted_lists()

        # clear split
        # with open("data/teams.split.data", "w") as __file:
        #     __file.close()

        # Sleep to avoid rapid looping
        print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ] Exit Split!")
        exit(0)
    except Exception as e:
        # raise
        print(f"An error occurred: {e}")
        os.system("clear")  # Clear the console
        exit(0)

# start processes for betting split and combinations
# track why max of 2 teams are bet in a combination of 5
