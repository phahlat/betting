import players.gbets_player_get_teams as gbets_player_get_teams
import time
import threading

if __name__ == "__main__":
    try:
        __WAIT_PERIOD = 60 * 30  # 30 minutes
        while True:
            # clear split
            print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ] 🎬 🎬 🎬 --- START GET TEAMS")
            
            # set status for betting to pause
            with open("data/teams.canbet.data", "w") as __file:
                print("False", file=__file)
                __file.close()
            
            with open("data/teams.split.data", "w") as __file:
                __file.close()
            
            # clear combo
            with open("data/teams.combo.data", "w") as __file:
                __file.close()
                
            gbets_player_get_teams.get_teams()
            print(
                f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ] Waiting for the next round... in {__WAIT_PERIOD // 60} minutes."
            )
            
            # set status for betting to continue
            with open("data/teams.canbet.data", "w") as __file:
                print("True", file=__file)
                __file.close()
                
            time.sleep(__WAIT_PERIOD)  # Sleep to avoid rapid looping
    except:
        raise