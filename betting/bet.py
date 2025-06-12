import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List
import pprint


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
    for i, bets in enumerate(match_groups_list, 1):
        print(f"🎯 Bet Option {i}:")
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
            print(f"{'** ' * 5}{__match}")

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


def bet_gbets(driver: webdriver.Chrome, match_groups_list: list):
    # Display the selected combinations
    __high_stake_matches_count = 2
    __low_stake, __high_stake = 1, 1.20
    __MINIMUM_TEAMS = 1
    __DRIVER_WAIT_PERIOD = 30
    __INTERACTIVE_ELEMENT_WAIT_PERIOD_3S = 2
    __INTERACTIVE_ELEMENT_WAIT_PERIOD_5S = 5

    # loop match groups
    __match_groups_list_length = len(match_groups_list)
    for __group_number, __teams_group in enumerate(match_groups_list, 1):
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
            f"½ ½ ½ Group Number: {__group_number}/{__match_groups_list_length:<10}: Matches Lenth: {len(__teams_group)} "
        )

        # time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
        __team_wrapper = None
        for __team_number, __match in enumerate(__teams_group, 1):
            try:
                __team_wrapper = driver.find_element(
                    By.XPATH,
                    f"//div[contains(@class, 'gamesWrapper')]//div[contains(@class, 'comp__teamName__wrapper') and contains(., \"{__match.split(":")[0]}\")]",
                )
                __second_parent = __team_wrapper.find_element(By.XPATH, "./ancestor::*[2]")
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
                __away_odds = float(__match_odds[1].text)
                __draw_odds = float(__match_odds[2].text)

                time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                if __away_odds - __home_odds > 0.5:
                    # choose home win
                    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(__home_win)
                    )
                    __home_win.click()
                    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    __match_count = __match_count + 1
                    __bet_done = True
                    print(
                        f"🥅 🥅 🥅 Match Number: {__team_number}/{__teams_group_length:<3} | {'[HOME]':<5} Odds: {__home_odds:<4} | ODDS: {'⚽️ ⚽️':<5} H: {__home_odds} --- D: {__draw_odds} --- A: {__away_odds} Selected--: {__match_count:<10}"
                    )

                elif __home_odds - __away_odds > 0.5:
                    # choose away wind
                    __match_count = __match_count + 1
                    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(__away_win)
                    )
                    __away_win.click()
                    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    __bet_done = True
                    print(
                        f"🥅 🥅 🥅 Match Number: {__team_number}/{__teams_group_length:<3} | {'[AWAY]':<4} Odds: {__away_odds:<4} | ODDS: {'⚽️ ⚽️':<4} H: {__home_odds} --- D: {__draw_odds} --- A: {__away_odds} | Selected--: {__match_count:<10}"
                    )

                else:
                    # choose either can win
                    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(__draw_win)
                    )
                    __draw_win.click()
                    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    __match_count = __match_count + 1
                    __bet_done = True
                    print(
                        f"🥅 🥅 🥅 Match Number: {__team_number}/{__teams_group_length:<3} | {'DRAW':<4} Odds: {__draw_odds:<4} | ODDS: {'⚽️ ⚽️':<4} H: {__home_odds} --- D: {__draw_odds} --- A: {__away_odds} Selected--: {__match_count:<10}"
                    )

                    # time.sleep(60)
                # time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
            except:
                continue

        print(
            f"🥅 🥅 🥅 BET ON? {__group_number}/{__match_groups_list_length:<10}: {__bet_done and __match_count >= __MINIMUM_TEAMS}"
        )
        
        # focus on team wrapper
        if not __team_wrapper:
            del __match_count
            continue
        driver.execute_script("arguments[0].focus();", __team_wrapper)
        
        if __bet_done and __match_count >= __MINIMUM_TEAMS:
            # input bet amount
            stake_input = driver.find_elements(
                By.XPATH, "//input[@placeholder='Stake']"
            )

            print(
                f"🥅 🥅 🥅 Betting on Match Group: {__group_number}/{__match_groups_list_length:<10}: || Number of Matches: {__match_count}"
            )
            
            stake = stake_input[0].get_attribute("value")
            if not (stake and stake.isdigit() and int(stake) == 1):
                stake_input[0].send_keys(
                    f"{__low_stake}"
                    if __match_count < __high_stake_matches_count
                    else f"{__high_stake}"
                )
                print(
                    f"½ ½ ½ Group Number: {__group_number}/{__match_groups_list_length:<10}: 💰 Adding Stake: {__bet_done} | {f'{__low_stake}' if __match_count < __high_stake_matches_count else f'{__high_stake}'}"
                )
                time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)

            driver.find_element(
                By.XPATH, "//button[@data-testid='place-bet']"
            ).click()
            time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_5S)
            print(
                f"½ ½ ½ Group Number: {__group_number}/{__match_groups_list_length:<10}: ✅ ✅ ✅ Bet Done: {__bet_done} ::: Match Count: {__match_count}"
            )
            print(f"⓿ ⓿ ⓿ Reset Match Count")

        del __match_count
        del __bet_done


# TODO:
"""
1. Cashout every available M5+
"""
