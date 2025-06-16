import players.gbets_player_get_teams as gbets_player_get_teams
import time
import threading

if __name__ == "__main__":
    try:
        __WAIT_PERIOD = 60 * 30  # 30 minutes
        while True:
            with open("teams.dat", "w") as __file:
                __file.close()
                
            gbets_player_get_teams.get_teams()
            print(
                f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ] Waiting for the next round..."
            )
            time.sleep(__WAIT_PERIOD)  # Sleep to avoid rapid looping
    except:
        raise


# start processes for betting split and combinations
# track why max of 2 teams are bet in a combination of 5
