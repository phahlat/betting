from betting.cashout import gbets_cashout
import time
import os

if __name__ == "__main__":
    __WAIT_PERIOD = 60 * 7
    while True:
        try:
            gbets_cashout()
            print(
                f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ] Waiting for the next cashout round... in {__WAIT_PERIOD // 60} minutes."
            )

            time.sleep(__WAIT_PERIOD)
        except Exception as e:
            # raise
            print(f"An error occurred: {e}")
            os.system("clear")
            # raise
