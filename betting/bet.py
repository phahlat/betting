import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List
import pprint


def chunk_list(data: List[str], chunk_size: int) -> List[List[str]]:
    """Splits a list into chunks of specified size, keeping the remainder in the last chunk."""
    return [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]


def bet_sima(driver: webdriver.Chrome, matches: list):
    __MINIMUM_TEAMS = 2
    __DRIVER_WAIT_PERIOD = 30
    __INTERACTIVE_ELEMENT_WAIT_PERIOD_3S = 3
    __INTERACTIVE_ELEMENT_WAIT_PERIOD_5S = 5
    __INTERACTIVE_ELEMENT_WAIT_PERIOD_10 = 10

    # Display the selected combinations
    for i, bets in enumerate(matches, 1):
        print(f"🎯 Bet Option {i}:")
        try:
            chat_iframe = driver.find_element(
                By.XPATH, "//iframe[contains(@name, 'cx-webChatButton')]")
            driver.execute_script(
                "arguments[0].style.display = 'none';", chat_iframe)
            # Optionally, wait until it's not visible
            WebDriverWait(driver, 5).until(
                lambda d: not chat_iframe.is_displayed()
            )
        except Exception:
            pass

        for match in bets:
            print(f"{'** ' * 5}{match}")

            # find match row
            match_selector = driver.find_element(
                By.XPATH,
                f"//div[contains(@class, 'event-row') and contains(., \"{match.strip()}\")]"
            )
            # find double change column
            double_chance = match_selector.find_element(
                By.XPATH, "./*[2]/*[2]")

            # find odd options
            double_chance_odds = double_chance.find_elements(
                By.CLASS_NAME, "event-outcomes-odd")
            home_win = double_chance_odds[0]
            eith_win = double_chance_odds[1]
            away_win = double_chance_odds[2]

            # choose either can win
            # eith_win.click()
            # time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)

            # choose home win
            # home_win.click()
            # time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)

            # choose away wind
            # away_win.click()

            notifications = driver.find_elements(
                By.XPATH, "//div[contains(@class, 'notification-row') and contains(normalize-space(.), 'Not enough credit on your balance.')]")
            if notifications:
                exit(-1)

            time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)

        driver.find_element(By.CLASS_NAME, "buttons-payin").click()


def bet_gbets(driver: webdriver.Chrome, matches: list):
    # Display the selected combinations
    match_selector = []
    __MINIMUM_TEAMS = 1
    __DRIVER_WAIT_PERIOD = 30
    __INTERACTIVE_ELEMENT_WAIT_PERIOD_3S = 2
    __INTERACTIVE_ELEMENT_WAIT_PERIOD_5S = 4
    __INTERACTIVE_ELEMENT_WAIT_PERIOD_10 = 10

    for i, _ in enumerate(matches, 1):
        print(f"{'⛹ ⛹' * 5:<10}| Match Number: {i: 5} {_}")
    print()

    for i, teams in enumerate(matches, 1):
        __match_count = 0
        __bet_done = False

        # clear bets for next round
        __clear_bets = driver.find_elements(
            By.XPATH, "//span[@data-testid='delete-all-bets']")
        if len(__clear_bets):
            try:
                WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                    EC.element_to_be_clickable(__clear_bets[0])).click()
            except:
                pass

        for match in teams:
            # find match row
            match_selector = driver.find_elements(
                By.XPATH,
                f"//div[contains(@class, 'comp__teamName__wrapper') and contains(., \"{match.split(":")[0]}\")]"
            )
            time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)

            try:
                if len(match_selector) == 0:
                    continue

                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", match_selector[0])
                time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                match_selector[0].click()

                time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                x2_element = driver.find_element(
                    By.XPATH, "//*[normalize-space(text())='Draw']")  # -- X2

                # Get the parent match_selector
                parent = x2_element.find_element(By.XPATH, "./..")
                parent_siblings = parent.find_elements(
                    By.XPATH, "./preceding-sibling::* | ./following-sibling::*")
                time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)

                # remove bets if no bet options selected
                if len([parent, *parent_siblings]) < 3:
                    # clear bets
                    __clear_bets = driver.find_elements(
                        By.XPATH, "//span[@data-testid='delete-all-bets']")
                    if len(__clear_bets):
                        try:
                            WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                                EC.element_to_be_clickable(__clear_bets[0])).click()
                        except:
                            raise

                    __match_count = 0
                    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    break

                home_win = parent_siblings[0]
                away_win = parent_siblings[1]
                draw_win = parent

                __home_odds = float(
                    home_win.find_element(By.XPATH, "./*[2]").text)
                __draw_odds = float(
                    draw_win.find_element(By.XPATH, "./*[2]").text)
                __away_odds = float(
                    away_win.find_element(By.XPATH, "./*[2]").text)
                print(
                    f"Match Number: {i:<10} Match: {'⚽️':<5} H: {__home_odds} --- D: {__draw_odds} --- A: {__away_odds}")

                if __away_odds - __home_odds > 0.5:
                    # choose home win
                    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(home_win))
                    home_win.click()
                    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    __bet_done = True
                    __match_count = __match_count + 1
                    print(
                        f"Match Number: {i:<10} Bet: {'[HOME]':<5} Odds: {__home_odds:<8} Selected: {__match_count:<10} 🏆 Match: {match:<40}")

                elif __home_odds - __away_odds > 0.5:
                    # choose away wind
                    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(away_win))
                    away_win.click()
                    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    __bet_done = True
                    __match_count = __match_count + 1
                    print(
                        f"Match Number: {i:<10} Bet: {'[AWAY]':<5} Odds: {__away_odds:<8} Selected: {__match_count:<10} 🏆 Match: {match:<40}")

                else:
                    # choose either can win
                    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(draw_win))
                    draw_win.click()
                    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    __bet_done = True
                    __match_count = __match_count + 1
                    print(
                        f"Match Number: {i:<10} Bet: {'DRAW':<5} Odds: {__draw_odds:<8} Selected: {__match_count:<10} 🏆 Match: {match:<40}")

                driver.execute_script(
                    "arguments[0].focus();", match_selector[0])
                time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
            except:
                break

        print(f"Match Number: {i:<10}: 🎰 BET CHECK???: {__bet_done and __match_count >= __MINIMUM_TEAMS} ::: 🤘 BET STATUS: {__bet_done} | ℀ MATCH COUNT: {__match_count}")
        # input bet amount
        if __bet_done and __match_count >= __MINIMUM_TEAMS:
            stake_input = driver.find_elements(
                By.XPATH, "//input[@placeholder='Stake']")

            print(
                f"Match Number: {i:<10}: Betting [{i}]: 🎰 Bet State: {__bet_done} 🤼‍♂️: {__match_count}")

            if len(stake_input) == 0:
                __match_count = 0

            else:
                stake = stake_input[0].get_attribute("value")
                if not (stake and stake.isdigit() and int(stake) == 1):
                    stake_input[0].send_keys("1")
                    print(
                        f"Match Number: {i:<10}: 💰 Adding Stake: {__bet_done}")
                    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)

                driver.find_element(
                    By.XPATH, "//button[@data-testid='place-bet']").click()
                time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_5S)
                print(
                    f"Match Number: {i:<10}: ✅ ✅ ✅ Bet Done: {__bet_done} ::: Match Count: {__match_count}")
                print(f"♻️ ♻️ ♻️ Reset Match Count To 𝟎")

        del __match_count
        del __bet_done

def cashout_gbets(driver: webdriver.Chrome, matches: list):
    # Display the selected combinations
    match_selector = []
    __MINIMUM_TEAMS = 1
    __DRIVER_WAIT_PERIOD = 30
    __INTERACTIVE_ELEMENT_WAIT_PERIOD_3S = 2
    __INTERACTIVE_ELEMENT_WAIT_PERIOD_5S = 4
    __INTERACTIVE_ELEMENT_WAIT_PERIOD_10 = 10

    for i, _ in enumerate(matches, 1):
        print(f"{'________' * 5}| {i} {_}")
    print()

    for i, teams in enumerate(matches, 1):
        __match_count = 0
        __bet_done = False

        # clear bets for next round
        __clear_bets = driver.find_elements(
            By.XPATH, "//span[@data-testid='delete-all-bets']")
        if len(__clear_bets):
            try:
                WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                    EC.element_to_be_clickable(__clear_bets[0])).click()
            except:
                pass

        for match in teams:
            # find match row
            match_selector = driver.find_elements(
                By.XPATH,
                f"//div[contains(@class, 'comp__teamName__wrapper') and contains(., \"{match.split(":")[0]}\")]"
            )
            time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)

            try:
                if len(match_selector) == 0:
                    continue

                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", match_selector[0])
                time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                match_selector[0].click()

                time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                x2_element = driver.find_element(
                    By.XPATH, "//*[normalize-space(text())='Draw']")  # -- X2

                # Get the parent match_selector
                parent = x2_element.find_element(By.XPATH, "./..")
                parent_siblings = parent.find_elements(
                    By.XPATH, "./preceding-sibling::* | ./following-sibling::*")
                time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)

                # remove bets if no bet options selected
                if len([parent, *parent_siblings]) < 3:
                    # clear bets
                    __clear_bets = driver.find_elements(
                        By.XPATH, "//span[@data-testid='delete-all-bets']")
                    if len(__clear_bets):
                        try:
                            WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                                EC.element_to_be_clickable(__clear_bets[0])).click()
                        except:
                            raise

                    __match_count = 0
                    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    break

                home_win = parent_siblings[0]
                away_win = parent_siblings[1]
                draw_win = parent

                __home_odds = float(
                    home_win.find_element(By.XPATH, "./*[2]").text)
                __draw_odds = float(
                    draw_win.find_element(By.XPATH, "./*[2]").text)
                __away_odds = float(
                    away_win.find_element(By.XPATH, "./*[2]").text)
                print(
                    f"Match Number: {i:<10} Match: {'⚽️':<5} H: {__home_odds} --- D: {__draw_odds} --- A: {__away_odds}")

                if __away_odds - __home_odds > 0.5:
                    # choose home win
                    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(home_win))
                    home_win.click()
                    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    __bet_done = True
                    __match_count = __match_count + 1
                    print(
                        f"Match Number: {i:<10} Bet: {'[HOME]':<5} Odds: {__home_odds:<8} Selected: {__match_count:<10} 🏆 Match: {match:<40}")

                elif __home_odds - __away_odds > 0.5:
                    # choose away wind
                    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(away_win))
                    away_win.click()
                    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    __bet_done = True
                    __match_count = __match_count + 1
                    print(
                        f"Match Number: {i:<10} Bet: {'[AWAY]':<5} Odds: {__away_odds:<8} Selected: {__match_count:<10} 🏆 Match: {match:<40}")

                else:
                    # choose either can win
                    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(draw_win))
                    draw_win.click()
                    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    __bet_done = True
                    __match_count = __match_count + 1
                    print(
                        f"Match Number: {i:<10} Bet: {'DRAW':<5} Odds: {__draw_odds:<8} Selected: {__match_count:<10} 🏆 Match: {match:<40}")

                driver.execute_script(
                    "arguments[0].focus();", match_selector[0])
                time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
            except:
                break

        print(f"Match Number: {i:<10}: 🎰 BET CHECK???: {__bet_done and __match_count >= __MINIMUM_TEAMS} ::: 🤘 BET STATUS: {__bet_done} | ℀ MATCH COUNT: {__match_count}")
        # input bet amount
        if __bet_done and __match_count >= __MINIMUM_TEAMS:
            stake_input = driver.find_elements(
                By.XPATH, "//input[@placeholder='Stake']")

            print(
                f"Match Number: {i:<10}: Betting [{i}]: 🎰 Bet State: {__bet_done} 🤼‍♂️: {__match_count}")

            if len(stake_input) == 0:
                __match_count = 0

            else:
                stake = stake_input[0].get_attribute("value")
                if not (stake and stake.isdigit() and int(stake) == 1):
                    stake_input[0].send_keys("1")
                    print(
                        f"Match Number: {i:<10}: 💰 Adding Stake: {__bet_done}")
                    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)

                driver.find_element(
                    By.XPATH, "//button[@data-testid='place-bet']").click()
                time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_5S)
                print(
                    f"Match Number: {i:<10}: ✅ ✅ ✅ Bet Done: {__bet_done} ::: Match Count: {__match_count}")
                print(f"♻️ ♻️ ♻️ Reset Match Count To 𝟎")

        del __match_count
        del __bet_done


# TODO:
"""
1. Cashout every available M5+
"""
