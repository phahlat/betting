import time
import os
import math
import random
from itertools import combinations, combinations_with_replacement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from betting.bet import bet_gbets, chunk_list

os.system("clear")
is_live_sports = True
# GET GAMES LIST
__MATCHES_CHUNK_LENGTH = 5
__MATCHES_COMBINATIONS_LENGTH = 3
__DRIVER_WAIT_PERIOD = 30
__INTERACTIVE_ELEMENT_WAIT_PERIOD_3S = 2
__INTERACTIVE_ELEMENT_WAIT_PERIOD_5S = 4
__INTERACTIVE_ELEMENT_WAIT_PERIOD_15S = 15

# Optional: configure Chrome to stay open
options = Options()
# options.add_experimental_option("detach", True)

# Disable browser notification popups
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)


def play():
    __matches_list = []

    # Launch the browser
    driver = webdriver.Chrome(options=options)

    # Open the website
    driver.get('https://www.gbets.co.ls/')
    # driver.set_window_position(10, -1280)  # x=1920
    driver.maximize_window()

    # # Find and click the login button
    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[normalize-space()='Sign In']"))
    ).click()

    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='username']"))
    ).send_keys('priska.phahla@gmail.com')
    driver.find_element(
        By.XPATH, "//input[@id='password']").send_keys("201200xXx")
    driver.find_element(
        By.XPATH, "//button[@type='submit']//span[contains(text(),'Sign In')]").click()
    time.sleep(3)

    #  Click Sports
    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@class,'center') and contains(., 'Sport')]"))
    ).click()

    # click live for live sports
    if is_live_sports:
        time.sleep(3)
        WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[normalize-space()='Live']"))
        ).click()

    # click today
    else:
        time.sleep(3)
        WebDriverWait(driver=driver, timeout=__DRIVER_WAIT_PERIOD).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@data-testid='today']"))
        ).click()

    time.sleep(__INTERACTIVE_ELEMENT_WAIT_PERIOD_15S)
    __e_sport_live_games = driver.find_elements(
        By.XPATH, "//div[@data-testid='e-sport-game']")
    # get match teams
    for _game in __e_sport_live_games:
        __teams = _game.find_elements(By.CLASS_NAME, "comp__teamName__wrapper")
        __matches_list.append(f"{__teams[0].text}:{__teams[1].text}")

    # Example: list of 21 strings
    print(f"🧮 🧮 🧮 Matches List Length:: {len(__matches_list)}")
    __chunked_matches_lists = list(chunk_list(__matches_list, chunk_size=(
        __MATCHES_CHUNK_LENGTH if len(__matches_list) >= 12 else 4)))
    print(f"🧮 🧮 🧮 Total Chunked Matches Lists::: {len(__chunked_matches_lists)}")

    for __matches_list in __chunked_matches_lists:
        # Generate all combinations of half the available matches
        if len(__matches_list) >= 3:
            match_combinations = list(combinations(
                __matches_list, __MATCHES_COMBINATIONS_LENGTH if len(__matches_list) >= 4 else 2))
            print(f"📼 📼 📼 Total Matches Combinations: {len(__chunked_matches_lists):<5}")
            random_matches = random.sample(
                population=match_combinations, k=len(match_combinations) if len(match_combinations) < 50 else 50)
        else:
            random_matches = [__matches_list]

        print(f"📼 📼 📼 --> Random Bets List Length::: {len(random_matches):< 5}")
        bet_gbets(driver=driver, matches=random_matches)
    # time.sleep(3)
    driver.quit()


def reload_results_and_table(driver: webdriver.Chrome):
    #  Click History
    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class,'profileInfo__history-wrapper')]"))
    ).click()

    # wait for data to appear
    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//th[normalize-space(text())='Date/ID/Bet Type']"))
    )

    # click on results options
    __result_selector = WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@data-testid='results']"))
    )
    __result_selector.click()
    time.sleep(5)

    # select Not Resulted
    __result_options = driver.find_elements(
        By.XPATH, "//div[@data-testid='results_option']")
    if len(__result_options) == 0:
        return
    __result_options[1].click()
    time.sleep(1)

    # close results options
    __result_selector.click()

    # get results table
    __table_body = driver.find_elements(
        By.CSS_SELECTOR, "tbody.v3-table-tbody")
    if len(__table_body) == 0:
        return

    return __table_body


def cashout():
    __CASHOUT_MINIMUM = 1.5

    # Launch the browser
    driver = webdriver.Chrome(options=options)

    # Open the website
    driver.get('https://www.gbets.co.ls/')
    driver.set_window_position(10, -1280)  # x=1920
    driver.maximize_window()

    # # Find and click the login button
    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[normalize-space()='Sign In']"))
    ).click()

    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='username']"))
    ).send_keys('priska.phahla@gmail.com')
    driver.find_element(
        By.XPATH, "//input[@id='password']").send_keys("201200xXx")
    driver.find_element(
        By.XPATH, "//button[@type='submit']//span[contains(text(),'Sign In')]").click()
    time.sleep(3)

    # load results table
    __table_body = reload_results_and_table(driver=driver)
    if not __table_body:
        return

    # get rows from not resulted
    __table_rows = __table_body[0].find_elements(
        By.CSS_SELECTOR, "tr.v3-table-row.v3-table-row-level-0")

    while (len(__table_rows)):
        for i, __row in enumerate(__table_rows, 1):
            # get cashout rows
            __cashout_option_rows = __row.find_elements(
                By.XPATH, ".//span[contains(@class, 'myBetsCashout__text')]")
            if len(__cashout_option_rows) == 0:
                continue
            
            for _ in __cashout_option_rows:
                print(f"💶 💶 💶 💶 💶 💶 Cashout Data: {" ".join(_.text.split('\n')):>15}\n")
                
            __cashout_money = __cashout_option_rows[0].find_elements(
                By.XPATH, ".//span[starts-with(normalize-space(text()), 'LSL')]")
            if not len(__cashout_money):
                continue

            __cash = float(__cashout_money[0].text.split(" ")[1])
            if __cash > __CASHOUT_MINIMUM:
                # click cashout parent
                print(f"💰 💰 💰 Cashout Row: {i:>10} | 🤑 🤑 🤑 CASHOUT: {__cash:>5}")
                __cashout_money[0].click()

                # Wait for and click the button that contains the text 'Cash Out'
                WebDriverWait(driver=driver, timeout=__DRIVER_WAIT_PERIOD).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//button[contains(@class, 'v3-btn') and .//span[normalize-space(text())='Cash Out']]"
                    ))
                ).click()

                try:
                    WebDriverWait(driver=driver, timeout=__DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "[//span[normalize-space(text())='Proceed']]"))
                    ).click()
                    print(f"💼 💼 💼 Bagged: {i:>10} | 💸 💸 💸 WIN: {__cash:>5}")
                    time.sleep(5)
                    break
                except:
                    pass

                # confirm cashout
                try:
                    WebDriverWait(driver=driver, timeout=__DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//button[contains(@class, 'v3-btn') and .//span[normalize-space(text())='OK']]"))
                    ).click()
                    time.sleep(5)
                    print(f"💼 💼 💼 Bagged: {i:>10} | 💸 💸 💸 WIN: {__cash:>5}")
                except:
                    WebDriverWait(driver=driver, timeout=__DRIVER_WAIT_PERIOD).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//button[contains(@class, 'v3-btn') and .//span[normalize-space(text())='Cancel']]"))
                    ).click()
                    print(f"😩 😩 😩 Canceled: {i:>10} | ❌ ❌ ❌ LOSS: {__cash:>5}")
                    break

            del __cashout_option_rows
            del __cash
            del __cashout_money

        __close_header = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'accountModal__header__title')]/following-sibling::*")
        __close_header[0].click()
        
        time.sleep(15)
        __table_body = reload_results_and_table(driver=driver)
        if not __table_body:
            return
        time.sleep(15)
        __table_rows = __table_body[0].find_elements(
            By.CSS_SELECTOR, "tr.v3-table-row.v3-table-row-level-0")
