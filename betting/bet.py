from threading import Thread
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List
from datetime import datetime

# Display the selected combinations§
HIGH_STAKE_MATCHES_COUNT = 2
LOW_STAKE, HIGH_STAKE = 1, 1
MINIMUM_TEAMS = 1
DRIVER_WAIT_PERIOD = 30
INTERACTIVE_ELEMENT_WAIT_PERIOD_3S = 3
INTERACTIVE_ELEMENT_WAIT_PERIOD_10S = 10


def chunk_list(data: List[str], chunk_size: int) -> List[List[str]]:
    """Splits a list into chunks of specified size, keeping the remainder in the last chunk."""
    return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]


def remove_suspended(driver):
    # Find the span and go up 3 ancestors
    try:
        __suspended_bets_third_parent = driver.find_elements(
            By.XPATH, "//span[normalize-space(text())='Suspended']/ancestor::*[3]"
        )

        if len(__suspended_bets_third_parent) == 0:
            # print(f"⏳ ⏳ ⏳ --- {datetime.now()} - No suspended bets found.")
            pass

        else:
            print(
                f"⏳ ⏳ ⏳ --- {datetime.now()} - Found suspended bets: {len(__suspended_bets_third_parent)}"
            )
            for __parent in __suspended_bets_third_parent:
                print(f"{__parent.get_attribute('class')}")
                __delete_bet = __parent.find_elements(
                    By.XPATH, ".//span[contains(@class, 'betslip__bet-delete')]"
                )
                if len(__delete_bet) == 0:
                    print(
                        f"⏳ ⏳ ⏳ --- {datetime.now()} - No delete button found for suspended bet. {__delete_bet.get_attribute('class')}"
                    )
                    continue
                else:
                    print(f"⏳ ⏳ ⏳ --- {datetime.now()} - Deleting suspended bet.")
                    __delete_bet[0].click()
    except Exception as e:
        return

    time.sleep(INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)


def bet_gbets(driver, match_groups_list, browser_type="CHROME"):
    time.sleep(10)
    
    # loop match groups
    __match_groups_list_length = len(match_groups_list)
    for __group_number, __teams_group in enumerate(match_groups_list, 0):
        __match_count = 0
        __bet_done = False

        # loop teams in a match group
        __teams_group_length = len(__teams_group)
        print(
            f"{browser_type} --- [ {datetime.now()} ] 🎳 🎳 🎳 Group Number: {__group_number}/{__match_groups_list_length:<3}: Matches Length: {len(__teams_group)} "
        )

        __team_wrapper = None
        for __team_number, __match in enumerate(__teams_group, 0):
            # reset variables
            __clicked_element = None
            print(
                f"{browser_type} --- [ {datetime.now()} ] 🏁 🏁 🏁 TRYING BET ON MATCH: {__team_number}/{__teams_group_length:<3} | {__match}"
            )

            try:
                # FIND TEAM
                __team_wrapper = driver.find_element(
                    By.XPATH,
                    f"//div[contains(@class, 'gamesWrapper')]//div[contains(@class, 'comp__teamName__wrapper') and contains(., \"{__match.split(":")[0]}\")]",
                )

                # SCROLL TO TEAM
                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});",
                    __team_wrapper,
                )

                # FIND ODDS
                __second_parent = __team_wrapper.find_element(
                    By.XPATH, "./ancestor::*[2]"
                )
                __odds_parent = __second_parent.find_elements(
                    By.XPATH, "following-sibling::*[2]"
                )
                __match_odds = __odds_parent[0].find_elements(
                    By.XPATH, "./span[contains(@class, 'xOddButton--defaultHover')]"
                )

                __home_win = __match_odds[0]
                __draw_win = __match_odds[1]
                __away_win = __match_odds[2]

                __home_odds = float(__match_odds[0].text)
                __draw_odds = float(__match_odds[1].text)
                __away_odds = float(__match_odds[2].text)

                print(
                    f"{browser_type} --- [ {datetime.now()} ] 🏁 🏁 🏁 TEAM: {__team_number}/{__teams_group_length:<3} | Odds: [HOME]: {__home_odds:<4} | [DRAW]: {__draw_odds:<4} | [AWAY]: {__away_odds:<4}"
                )

                time.sleep(INTERACTIVE_ELEMENT_WAIT_PERIOD_10S)
                if __away_odds - __home_odds > 0.5:
                    # choose home win
                    __bet_done = True
                    WebDriverWait(driver, DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(__home_win)
                    )

                    __clicked_element = __home_win
                    __home_win.click()

                    time.sleep(INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    __match_count = __match_count + 1
                    print(
                        f"{browser_type} --- [ {datetime.now()} ] 🏁 🏁 🏁 TEAM: {__team_number}/{__teams_group_length:<3} | {'[HOME]':<5} Odds: {__home_odds:<4}  | Selected--: {__match_count:<3}"
                    )

                elif __home_odds - __away_odds > 0.5:
                    # choose away wind
                    __bet_done = True
                    __match_count = __match_count + 1

                    WebDriverWait(driver, DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(__away_win)
                    )

                    __clicked_element = __away_win
                    __away_win.click()
                    time.sleep(INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    print(
                        f"{browser_type} --- [ {datetime.now()} ] 🏁 🏁 🏁 TEAM: {__team_number}/{__teams_group_length:<3} | {'[AWAY]':<4} Odds: {__away_odds:<4} | Selected--: {__match_count:<3}"
                    )

                else:
                    # choose either can win
                    __bet_done = True
                    __match_count = __match_count + 1
                    WebDriverWait(driver, DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(__draw_win)
                    )

                    __clicked_element = __draw_win
                    __draw_win.click()
                    time.sleep(INTERACTIVE_ELEMENT_WAIT_PERIOD_3S)
                    print(
                        f"{browser_type} --- [ {datetime.now()} ] 🏁 🏁 🏁 TEAM: {__team_number}/{__teams_group_length:<3} | {'DRAW':<4} Odds: {__draw_odds:<4} | Selected--: {__match_count:<3}"
                    )

                # time.sleep(10)
            except:
                print(
                    f"{browser_type} --- [ {datetime.now()} ] 🔜  🔜  🔜 {__team_number}/{__teams_group_length:<3} | SKIPPING --- @{__match}"
                )
                __clicked_element.click() if __clicked_element else None
                del __clicked_element
                continue

        print(
            f"\n{'- -' * 50}\n{browser_type} --- [ {datetime.now()} ] Bet on Match Group ❓ {__group_number}/{__match_groups_list_length:<3}: {__bet_done and __match_count > MINIMUM_TEAMS} | Matches Count: {__match_count}"
        )

        if __bet_done and __match_count > MINIMUM_TEAMS:
            __stake_value = f"{f'{LOW_STAKE}' if __match_count <
                               HIGH_STAKE_MATCHES_COUNT else f'{HIGH_STAKE}'}"

            print(
                f"{browser_type} --- [ {datetime.now()} ] Set Stake + Bet on Match: {__group_number}/{__match_groups_list_length:<3} | Matches Count: {__match_count} | Stake: {__stake_value}"
            )

            # input bet amount
            __stake_input = driver.find_elements(
                By.XPATH, "//input[@placeholder='Stake']"
            )
            if len(__stake_input) == 0:
                print(
                    f"{browser_type} --- [ {datetime.now()} ] ❌ ❌ ❌ ATTENTION -- NO STAKE INPUT FOUND: {__group_number}/{__match_groups_list_length:<3}"
                )
            else:
                # set __stake
                __stake = __stake_input[0].get_attribute("value")
                if not (__stake and __stake.isdigit() and int(__stake) == 1):

                    __stake_input[0].send_keys(__stake_value)
                    time.sleep(INTERACTIVE_ELEMENT_WAIT_PERIOD_10S)
                
                # remove suspended bets
                remove_suspended(driver)
                
                # click place bet
                driver.find_element(
                    By.XPATH, "//button[@data-testid='place-bet']"
                ).click()
                time.sleep(INTERACTIVE_ELEMENT_WAIT_PERIOD_10S)

                # wait for bet confirmation
                __empty_bets = driver.find_elements(
                    By.XPATH, "//div[contains(@class, 'emptyBox-title')]"
                )

                if len(__empty_bets) == 0:
                    # remove bets if no bet options selected
                    __clear_bets = driver.find_elements(
                        By.XPATH, "//span[@data-testid='delete-all-bets']"
                    )

                    # clear bets if failed to place bet
                    if len(__clear_bets) > 0:
                        print(
                            f"{browser_type} --- [ {datetime.now()} ] 🧹 🧹 🧹 Clearing Bets"
                        )

                        try:
                            WebDriverWait(driver, DRIVER_WAIT_PERIOD).until(
                                EC.element_to_be_clickable(__clear_bets[0])
                            ).click()
                        except:
                            pass

                        time.sleep(INTERACTIVE_ELEMENT_WAIT_PERIOD_10S)
                else:
                    print(
                        f"{browser_type} --- [ {datetime.now()} ] ✅ ✅ ✅ Group Number: {__group_number}/{__match_groups_list_length:<3} | Bet Done: {__bet_done} | Match Count: {__match_count}"
                    )

            print(f"{browser_type} --- [ {datetime.now()} ] ⓿ ⓿ ⓿ Reset Match Count")

        del __match_count
        del __bet_done


# TODO:
"""
1. Cashout every available M5+
"""
