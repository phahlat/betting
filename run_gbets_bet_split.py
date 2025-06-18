import players.gbets_player_bet_split as bet_split
import time
import os
import threading

if __name__ == "__main__":
    __WAIT_PERIOD = 60 * 30  # 30 minutes
    while True:
        try:
            while True:
                # set status for betting to continue
                with open("teams.canbet.data", "r") as __file:
                    __can_bet = __file.readline()
                    if __can_bet.strip() == "True":
                        print(f"\r[ {time.strftime('%Y-%m-%d %H:%M:%S')} ] CAN BET??? {__can_bet.strip()}", end="")
                        break
                    __file.close()
                print(f"\r[ {time.strftime('%Y-%m-%d %H:%M:%S')} ] CAN BET??? {__can_bet.strip()}", end="")
                time.sleep(2)
                    
            bet_split.bet_splitted_lists()
            print(
                f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ] Waiting for the next split round... in {__WAIT_PERIOD // 60} minutes."
            )
            
            # clear split
            with open("teams.split.data", "w") as __file:
                __file.close()
                
            # Sleep to avoid rapid looping
            time.sleep(__WAIT_PERIOD)
        except Exception as e:
            print(f"An error occurred: {e}")
            os.system("clear")  # Clear the console
            time.sleep(__WAIT_PERIOD)

# start processes for betting split and combinations
# track why max of 2 teams are bet in a combination of 5
