from betting.cashout import gbets_cashout
import time
import os

if __name__ == "__main__":
    while True:
        try:
            gbets_cashout()
        except Exception as e:
            print(f"An error occurred: {e}")
            os.system("clear")
            raise
        time.sleep(60)
