import players.gbets_player_get_teams as gbets_player_get_teams
import time
import threading

if __name__ == "__main__":
    try:
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
        print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ] Exit Get Teams!")

        # set status for betting to continue
        with open("data/teams.canbet.data", "w") as __file:
            print("True", file=__file)
            __file.close()

        exit(0)
    except Exception as _e:
        # raise
        print(f"Get Teams Exception:: {_e}")
