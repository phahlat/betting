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
INTERACTIVE_ELEMENT_WAIT_PERIOD = 10


def chunk_list(data: List[str], chunk_size: int) -> List[List[str]]:
    """Splits a list into chunks of specified size, keeping the remainder in the last chunk."""
    return [data[i: i + chunk_size] for i in range(0, len(data), chunk_size)]


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
                __delete_bet = __parent.find_elements(
                    By.XPATH, ".//span[contains(@class, 'betslip__bet-delete')]"
                )
                if len(__delete_bet) == 0:
                    print(
                        f"⏳ ⏳ ⏳ --- {datetime.now()} - No delete button found for suspended bet. {__delete_bet.get_attribute('class')}"
                    )
                    continue

                else:
                    print(
                        f"⏳ ⏳ ⏳ --- {datetime.now()} - Deleting suspended bet.")
                    __delete_bet[0].click()

    except Exception as e:
        # raise
        pass

    time.sleep(INTERACTIVE_ELEMENT_WAIT_PERIOD)


def bet_gbets(driver, match_groups_list, browser_type="CHROME"):
    time.sleep(10)

    # loop match groups
    __match_groups_list_length = len(match_groups_list)
    for __group_number, __teams_group in enumerate(match_groups_list, 0):
        print(
            f"\n{browser_type} --- [ {datetime.now()} ] 🎳 🎳 🎳 GROUP NUMBER: {__group_number+1}/{__match_groups_list_length:<3}: Matches Length: {len(__teams_group)} "
        )

        __match_count = 0
        __home_leading = False
        __away_leading = False
        __bet_done = False
        __match_not_started = False

        # loop teams in a match group
        __teams_group_length = len(__teams_group)
        if __teams_group_length == 0:
            continue

        __team_wrapper = None
        for __team_number, __match in enumerate(__teams_group, 0):
            # reset variables
            __team_one, __team_two = __match.split(":")
            __clicked_element = None

            try:
                # FIND TEAM
                print(
                    f"{browser_type} --- [ {datetime.now()} ] 🎳 🎳 🎳  | TEAM: {__team_number+1}/{__teams_group_length:<3} | find team:: {__team_one.strip()} vs {__team_two.strip()}"
                )
                __team_wrapper = driver.find_element(
                    By.XPATH,
                    f"//div[contains(@class, 'gamesWrapper')]//div[contains(@class, 'comp__teamName__wrapper') and contains(., \"{__team_one.strip()}\")]",
                )

                # SCROLL TO TEAM
                try:
                    print(
                        f"{browser_type} --- [ {datetime.now()} ] 🎳 🎳 🎳 | TEAM: {__team_number+1}/{__teams_group_length:<3} | bring team into view:: {__team_one.strip()} vs {__team_two.strip()}"
                    )
                    driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});",
                        __team_wrapper,
                    )
                except:
                    # raise
                    pass

                # Match Result Odds
                print(
                    f"{browser_type} --- [ {datetime.now()} ] 🎳 🎳 🎳 | TEAM: {__team_number+1}/{__teams_group_length:<3} | find team odds:: {__team_one.strip()} vs {__team_two.strip()}"
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

                # if match result no odds
                if len(__match_odds) == 0:
                    print(
                        f"{browser_type} --- [ {datetime.now()} ] 🔜  🔜  🔜 GROUP NUMBER: {__group_number+1} | TEAM: {__team_number+1}/{__teams_group_length:<3} | NO MATCH RESULTS ODDS --- @{__match}\n\n"
                    )
                    time.sleep(5)
                    continue

                __home_win = __match_odds[0]
                __draw_win = __match_odds[1]
                __away_win = __match_odds[2]

                __home_odds = float(__match_odds[0].text)
                __draw_odds = float(__match_odds[1].text)
                __away_odds = float(__match_odds[2].text)

                print(
                    f"{browser_type} --- [ {datetime.now()} ] 🎳 🎳 🎳 | TEAM: {__team_number+1}/{__teams_group_length:<3} | find team goals:: {__team_one.strip()} vs {__team_two.strip()}"
                )
                __third_ancestor = __team_wrapper.find_element(
                    By.XPATH, "./ancestor::*[3]"
                )
                __match_status = __third_ancestor.find_element(
                    By.XPATH, "./ancestor::*[1]"
                ).find_element(By.CSS_SELECTOR, "div.custom__row")
                __statistics = __third_ancestor.find_elements(
                    By.CLASS_NAME, "statistics"
                )[0].text.split(",")
                __goals, _, __current_time = None, None, None

                if str("1st half").lower() in str(__match_status.text).lower():
                    __goals = __statistics[0].split(":")
                    __current_time = __statistics[-1].replace(
                        "`", "").split(" ")[-1]

                    __goals = __statistics[0].split(":")
                    if int(__goals[0]) - int(__goals[1]) >= 2:
                        __home_leading = True

                    elif int(__goals[1]) - int(__goals[0]) >= 2:
                        __away_leading = True

                    print(
                        f"{browser_type} --- [ {datetime.now()} ] ⏰ ⏰ ⏰ FIRST HALF | {__team_one} vs {__team_two} | Odds: H: {__home_odds:<4} A: {__away_odds:<4} | GOALS: {__goals}"
                    )

                elif str("half time").lower() in str(__match_status.text).lower():
                    __goals = __statistics[0].split(":")
                    if int(__goals[0]) - int(__goals[1]) >= 2:
                        __home_leading = True

                    elif int(__goals[1]) - int(__goals[0]) >= 2:
                        __away_leading = True

                    print(
                        f"{browser_type} --- [ {datetime.now()} ] ⏰ ⏰ ⏰ HALF TIME | {__team_one} vs {__team_two} | Odds: H: {__home_odds:<4} A: {__away_odds:<4} | GOALS: {__goals}"
                    )

                elif (
                    str("2nd half").lower() in str(__match_status.text).lower()
                    or str("3rd half").lower() in str(__match_status.text).lower()
                    or str("4th half").lower() in str(__match_status.text).lower()
                ):
                    __goals = __statistics[0].split(":")
                    __current_time = __statistics[-1].replace(
                        "`", "").split(" ")[-1]

                    # Goal Difference
                    if (
                        int(__goals[0]) - int(__goals[1]) >= 1
                        and int(__current_time) > 65
                    ):
                        __home_leading = True

                    elif (
                        int(__goals[1]) - int(__goals[0]) >= 1
                        and int(__current_time) > 65
                    ):
                        __away_leading = True
                        print(
                            f"{browser_type} --- [ {datetime.now()} ] ⏰ ⏰ ⏰ 2nd/3rd/4th HALF | {__team_one} vs {__team_two} | Odds: H: {__home_odds:<4} A: {__away_odds:<4} | GOALS: {__goals}"
                        )

                elif str("not started").lower() in str(__match_status.text).lower():
                    __match_not_started = True
                    __goals = __statistics[0].split(":")

                time.sleep(INTERACTIVE_ELEMENT_WAIT_PERIOD)
                print(
                    f"{browser_type} --- [ {datetime.now()} ] 🎳 🎳 🎳 | TEAM: {__team_number+1}/{__teams_group_length:<3} | vetting on winning chances:: {__team_one.strip()} vs {__team_two.strip()}"
                )
                if __home_leading and __away_odds - __home_odds >= 0.5:
                    # choose home win
                    __bet_done = True
                    WebDriverWait(driver, DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(__home_win)
                    )

                    __clicked_element = __home_win
                    __home_win.click()

                    time.sleep(INTERACTIVE_ELEMENT_WAIT_PERIOD)
                    __match_count = __match_count + 1

                    print(
                        f"{browser_type} --- [ {datetime.now()} ] 🏁 🏁 🏁 GROUP NUMBER: {__group_number+1} | TEAM: {__team_number+1}/{__teams_group_length:<3} | {'[HOME LEADING]':<5} Odds: {__home_odds:<4}  | Selected--: {__match_count:<3}"
                    )

                elif __away_leading and __home_odds - __away_odds >= 0.5:
                    # choose away win
                    __bet_done = True
                    __match_count = __match_count + 1

                    WebDriverWait(driver, DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(__away_win)
                    )

                    __clicked_element = __away_win
                    __away_win.click()
                    time.sleep(INTERACTIVE_ELEMENT_WAIT_PERIOD)
                    print(
                        f"{browser_type} --- [ {datetime.now()} ] 🏁 🏁 🏁 GROUP NUMBER: {__group_number+1} | TEAM: {__team_number+1}/{__teams_group_length:<3} | {'[AWAY LEADING]':<4} Odds: {__away_odds:<4} | Selected--: {__match_count:<3}"
                    )

                # none is leading
                elif not __home_leading or not __away_leading:
                    # odds are for home to win
                    if __away_odds - __home_odds >= 1:
                        # choose home win
                        __bet_done = True
                        WebDriverWait(driver, DRIVER_WAIT_PERIOD).until(
                            EC.element_to_be_clickable(__home_win)
                        )

                        __clicked_element = __home_win
                        __home_win.click()
                        print(
                            f"{browser_type} --- [ {datetime.now()} ] 🏁 🏁 🏁 GROUP NUMBER: {__group_number+1} | TEAM: {__team_number+1}/{__teams_group_length:<3} | {'[NO LEAD: HOME FAVORED]':<4} Odds: {__away_odds:<4} | Selected--: {__match_count:<3}"
                        )

                    # odds are for away
                    elif __home_odds - __away_odds >= 1:
                        # choose away wind
                        __bet_done = True
                        __match_count = __match_count + 1

                        WebDriverWait(driver, DRIVER_WAIT_PERIOD).until(
                            EC.element_to_be_clickable(__away_win)
                        )

                        __clicked_element = __away_win
                        __away_win.click()
                        time.sleep(INTERACTIVE_ELEMENT_WAIT_PERIOD)
                        print(
                            f"{browser_type} --- [ {datetime.now()} ] 🏁 🏁 🏁 GROUP NUMBER: {__group_number+1} | TEAM: {__team_number+1}/{__teams_group_length:<3} | {'[NO LEAD: AWAY FAVORED]':<4} Odds: {__away_odds:<4} | Selected--: {__match_count:<3}"
                        )

                    else:
                        # bet either could win
                        # __team_wrapper.click()
                        __match_count = __match_count + 1
                        WebDriverWait(driver, DRIVER_WAIT_PERIOD).until(
                            EC.element_to_be_clickable(__draw_win)
                        )

                        __clicked_element = __draw_win
                        __draw_win.click()
                        time.sleep(INTERACTIVE_ELEMENT_WAIT_PERIOD)
                        print(
                            f"{browser_type} --- [ {datetime.now()} ] 🏁 🏁 🏁 GROUP NUMBER: {__group_number+1} | TEAM: {__team_number+1}/{__teams_group_length:<3} | {'DRAW/DOUBLE CHANCE':<4} Odds: {__draw_odds:<4} | Selected--: {__match_count:<3}"
                        )

                time.sleep(5)
            except Exception as _e:
                # raise
                print(
                    f"{browser_type} --- [ {datetime.now()} ] 🎳 🎳 🎳 Errored on betting:: {__team_one.strip()} vs {__team_two.strip()}"
                )
                print(
                    f"{browser_type} --- [ {datetime.now()} ] 🔜  🔜  🔜 SKIP GROUP NUMBER: {__group_number+1} | TEAM: {__team_number+1}/{__teams_group_length:<3} | SKIPPING --- @{__match}\n\n"
                )
                __clicked_element.click() if __clicked_element else None
                del __clicked_element

        if __bet_done and __match_count > MINIMUM_TEAMS:
            __stake_value = f"{f'{LOW_STAKE}' if __match_count <
                               HIGH_STAKE_MATCHES_COUNT else f'{HIGH_STAKE}'}"

            print(
                f"{browser_type} --- [ {datetime.now()} ] Set Stake + Bet on MATCH GROUP: {__group_number+1}/{__match_groups_list_length:<3} | Matches Count: {__match_count} | Stake: {__stake_value}"
            )

            # input bet amount
            __stake_input = driver.find_elements(
                By.XPATH, "//input[@placeholder='Stake']"
            )
            if len(__stake_input) == 0:
                print(
                    f"{browser_type} --- [ {datetime.now()} ] ❌ ❌ ❌ ATTENTION -- NO STAKE INPUT FOUND: {__group_number+1}/{__match_groups_list_length:<3}"
                )
            else:
                # set __stake
                __stake = __stake_input[0].get_attribute("value")
                if not (__stake and __stake.isdigit() and int(__stake) == 1):

                    __stake_input[0].send_keys(__stake_value)
                    time.sleep(INTERACTIVE_ELEMENT_WAIT_PERIOD)

                # remove suspended bets
                remove_suspended(driver)

                # click place bet
                __place_bet = driver.find_element(
                    By.XPATH, "//button[@data-testid='place-bet']"
                )
                # SCROLL TO TEAM
                # try:
                #     driver.execute_script(
                #         "arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});",
                #         __place_bet,
                #     )
                # except:
                #     pass

                time.sleep(2)
                __place_bet.click()
                time.sleep(20)

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
                            # raise
                            pass

                        time.sleep(INTERACTIVE_ELEMENT_WAIT_PERIOD)
                else:
                    print(
                        f"{browser_type} --- [ {datetime.now()} ] ✅ ✅ ✅ GROUP NUMBER: {__group_number}/{__match_groups_list_length:<3} | Bet Done: {__bet_done} | Match Count: {__match_count}"
                    )

            print(
                f"{browser_type} --- [ {datetime.now()} ] ⓿ ⓿ ⓿ Reset Match Count\n\n"
            )

        del __match_count
        del __bet_done
        del __match_not_started
        time.sleep(5)
