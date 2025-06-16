import players.gbets_player_bet_split as bet_split
import time
import threading

if __name__ == "__main__":
    __WAIT_PERIOD = 60 * 30  # 30 minutes
    try:
        while True:
            bet_split.bet_splitted_lists()
            print(
                f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ] Waiting for the next split round...{__WAIT_PERIOD} seconds"
            )
            # Sleep to avoid rapid looping
            time.sleep(__WAIT_PERIOD)
    except:
        raise


# start processes for betting split and combinations
# track why max of 2 teams are bet in a combination of 5
