import players.gbets_player as gbets_player
import time
import threading

if __name__ == "__main__":
    try:
        while True:
            gbets_player.cashout()
    except:
        raise
        