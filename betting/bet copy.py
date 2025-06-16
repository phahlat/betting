import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List
from datetime import datetime


def chunk_list(data: List[str], chunk_size: int) -> List[List[str]]:
    """Splits a list into chunks of specified size, keeping the remainder in the last chunk."""
    return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]


def bet_sima(driver: webdriver.Chrome, match_groups_list: list):
    __MINIMUM_TEAMS = 2
    __DRIVER_WAIT_PERIOD = 30
    __INTERACTIVE_ELEMENT_WAIT_PERIOD_3S = 3
    __INTERACTIVE_ELEMENT_WAIT_PERIOD_5S = 5
    __INTERACTIVE_ELEMENT_WAIT_PERIOD_10 = 10

    # Display the selected combinations
    for i, bets in enumerate(match_groups_list, 0):
        print(f"[ {datetime.now()} ] 🎯 Bet Option {i}:")
        try:
            chat_iframe = driver.find_element(
                By.XPATH, "//iframe[contains(@name, 'cx-webChatButton')]"
            )
            driver.execute_script("arguments[0].style.display = 'none';", chat_iframe)
            # Optionally, wait until it's not visible
            WebDriverWait(driver, 5).until(lambda d: not chat_iframe.is_displayed())
        except Exception:
            pass

        for __match in bets:
            print(f"[ {datetime.now()} ] {'** ' * 5}{__match}")

            # find __match row
            __match_selector = driver.find_element(
                By.XPATH,
                f"//div[contains(@class, 'event-row') and contains(., \"{__match.strip()}\")]",
            )
            # find double change column
            double_chance = __match_selector.find_element(By.XPATH, "./*[2]/*[2]")

            # find odd options
            double_chance_odds = double_chance.find_elements(
                By.CLASS_NAME, "event-outcomes-odd"
            )
            __home_odds = double_chance_odds[0]
            eith_win = double_chance_odds[1]
            __away_odds = double_chance_odds[2]

            # choose either can win
            # eith_win.click()
            # time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)

            # choose home win
            # __home_odds.click()
            # time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)

            # choose away wind
            # __away_odds.click()

            notifications = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'notification-row') and contains(normalize-space(.), 'Not enough credit on your balance.')]",
            )
            if notifications:
                exit(-1)

            time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)

        driver.find_element(By.CLASS_NAME, "buttons-payin").click()


def bet_gbets(driver: webdriver.Chrome, match_groups_list):
    # Display the selected combinations§
    __high_stake_matches_count = 2
    __low_stake, __high_stake = 1, 1.25
    __MINIMUM_TEAMS = 1
    __DRIVER_WAIT_PERIOD = 30
    __INTERACTIVE_ELEMENT_WAIT_PERIOD_3S = 3
    __INTERACTIVE_ELEMENT_WAIT_PERIOD_5S = 5

    import pprint

    for _ in match_groups_list:
        pprint.pprint(
            f"\n\n[ {datetime.now()} ] Groups Lists:: Group Length{len(match_groups_list)} :: List Length {len(_)}\n\n"
        )

    return
    # loop match groups
    __match_groups_list_length = len(match_groups_list)
    for __group_number, __teams_group in enumerate(match_groups_list, 0):
        __match_count = 0
        __bet_done = False

        # clear bets for next round
        __clear_bets = driver.find_elements(
            By.XPATH, "//span[@data-testid='delete-all-bets']"
        )
        if len(__clear_bets):
            try:
                WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                    EC.element_to_be_clickable(__clear_bets[0])
                ).click()
            except:
                pass

        # loop teams in a match group
        __teams_group_length = len(__teams_group)
        print(
            f"[ {datetime.now()} ] [ {datetime.now()} ] ½ ½ ½ Group Number: {__group_number}/{__match_groups_list_length:<10}: Matches Length: {len(__teams_group)} "
        )

        time.sleep(15)
        __team_wrapper = None
        for __team_number, __match in enumerate(__teams_group, 0):
            print(
                f"[ {datetime.now()} ] 🥅 🥅 🥅 {__team_number}/{__teams_group_length:<3} | Selected--: {__match_count:<10}\n"
            )
            try:
                __team_wrapper = driver.find_element(
                    By.XPATH,
                    f"//div[contains(@class, 'gamesWrapper')]//div[contains(@class, 'comp__teamName__wrapper') and contains(., \"{__match.split(":")[0]}\")]",
                )
                __second_parent = __team_wrapper.find_element(
                    By.XPATH, "./ancestor::*[2]"
                )
                __odds_parent = __second_parent.find_elements(
                    By.XPATH, "following-sibling::*[2]"
                )
                __match_odds = __odds_parent[0].find_elements(
                    By.XPATH, "./span[contains(@class, 'xOddButton--defaultHover')]"
                )

                # remove bets if no bet options selected
                if len(__match_odds) < 3:
                    # clear bets
                    __clear_bets = driver.find_elements(
                        By.XPATH, "//span[@data-testid='delete-all-bets']"
                    )
                    if len(__clear_bets):
                        try:
                            time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                            WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                                EC.element_to_be_clickable(__clear_bets[0])
                            ).click()
                        except:
                            pass

                    __match_count = 0
                    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    break

                __home_win = __match_odds[0]
                __draw_win = __match_odds[1]
                __away_win = __match_odds[2]

                __home_odds = float(__match_odds[0].text)
                __draw_odds = float(__match_odds[1].text)
                __away_odds = float(__match_odds[2].text)

                time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                if __away_odds - __home_odds > 0.5:
                    # choose home win
                    __bet_done = True
                    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(__home_win)
                    )
                    __home_win.click()
                    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    __match_count = __match_count + 1
                    print(
                        f"[ {datetime.now()} ] 🥅 🥅 🥅 {__team_number}/{__teams_group_length:<3} | {'[HOME]':<5} Odds: {__home_odds:<4}  | Selected--: {__match_count:<10} ƒ√| ODDS: {'⚽️ ⚽️':<5} H: {__home_odds} --- D: {__draw_odds} --- A: {__away_odds} | -- @{__match}"
                    )

                elif __home_odds - __away_odds > 0.5:
                    # choose away wind
                    __bet_done = True
                    __match_count = __match_count + 1
                    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(__away_win)
                    )
                    __away_win.click()
                    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    print(
                        f"🥅 🥅 🥅 {__team_number}/{__teams_group_length:<3} | {'[AWAY]':<4} Odds: {__away_odds:<4} | Selected--: {__match_count:<10} | ODDS: {'⚽️ ⚽️':<4} H: {__home_odds} --- D: {__draw_odds} --- A: {__away_odds} | -- @{__match}"
                    )

                else:
                    # choose either can win
                    __bet_done = True
                    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(__draw_win)
                    )
                    __draw_win.click()
                    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    __match_count = __match_count + 1
                    print(
                        f"[ {datetime.now()} ] 🥅 🥅 🥅 {__team_number}/{__teams_group_length:<3} | {'DRAW':<4} Odds: {__draw_odds:<4} | Selected--: {__match_count:<10} | ODDS: {'⚽️ ⚽️':<4} H: {__home_odds} --- D: {__draw_odds} --- A: {__away_odds} | -- @{__match}"
                    )

                    # time.sleep(60)
                time.sleep(10)
            except:
                print(
                    f"[ {datetime.now()} ] 🥅 🥅 🥅 {__team_number}/{__teams_group_length:<3} | SKIPPING | {'DRAW':<4} ------- @{__match}"
                )
                continue

        print(
            f"[ {datetime.now()} ] ‼️ -- ‼️ -- ‼️ BET ON? {__group_number}/{__match_groups_list_length:<10}: {__bet_done and __match_count >= __MINIMUM_TEAMS}"
        )

        if __bet_done and __match_count >= __MINIMUM_TEAMS:
            # input bet amount
            stake_input = driver.find_elements(
                By.XPATH, "//input[@placeholder='Stake']"
            )

            print(
                f"[ {datetime.now()} ] 🥅 🥅 🥅 Betting on Match Group: {__group_number}/{__match_groups_list_length:<10} | Number of Matches: {__match_count}"
            )

            stake = stake_input[0].get_attribute("value")
            if not (stake and stake.isdigit() and int(stake) == 1):
                stake_input[0].send_keys(
                    f"{__low_stake}"
                    if __match_count < __high_stake_matches_count
                    else f"{__high_stake}"
                )
                print(
                    f"[ {datetime.now()} ] ½ ½ ½ Group Number: {__group_number}/{__match_groups_list_length:<10}: 💰 Adding Stake: {__bet_done} | {f'{__low_stake}' if __match_count < __high_stake_matches_count else f'{__high_stake}'}"
                )
                time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)

            driver.find_element(By.XPATH, "//button[@data-testid='place-bet']").click()
            time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_5S)
            print(
                f"[ {datetime.now()} ] ½ ½ ½ Group Number: {__group_number}/{__match_groups_list_length:<10}: ✅ ✅ ✅ Bet Done: {__bet_done} ::: Match Count: {__match_count}"
            )
            print(f"[ {datetime.now()} ] ⓿ ⓿ ⓿ Reset Match Count")

        del __match_count
        del __bet_done


# TODO:
"""
1. Cashout every available M5+
"""
