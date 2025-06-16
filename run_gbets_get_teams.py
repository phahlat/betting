import players.gbets_player_get_teams as gbets_player_get_teams
import time
import threading

if __name__ == "__main__":
    try:
        while True:
            gbets_player_get_teams.get_teams()
            print(
                f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ] Waiting for the next round..."
            )
            time.sleep(900 * 2)  # Sleep to avoid rapid looping
    except:
        raise


# start processes for betting split and combinations
# track why max of 2 teams are bet in a combination of 5
