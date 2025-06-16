import time
import os
import math
import random
from itertools import combinations, combinations_with_replacement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from betting.bet import bet_gbets, chunk_list
import tempfile

os.system("clear")
is_live_sports = True
# GET GAMES LIST
__MATCHES_CHUNK_LENGTH = 6
__MATCHES_COMBINATIONS_LENGTH = 4
__DRIVER_WAIT_PERIOD = 60

__DRIVER_WAIT_FOR_BROWSER_LOAD_PERIOD = 15

# Optional: configure Chrome to stay open
# Create a temporary directory
user_data_dir = tempfile.mkdtemp()

# Configure Chrome options
options = Options()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.set_preference("browser.cache.disk.enable", False)
options.set_preference("browser.cache.memory.enable", False)
options.set_preference("browser.cache.offline.enable", False)
options.set_preference("network.http.use-cache", False)
options.set_preference("privacy.clearOnShutdown.cache", True)
options.set_preference("privacy.clearOnShutdown.cookies", True)
options.set_preference("privacy.sanitize.sanitizeOnShutdown", True)

def sign_in(driver: webdriver.Firefox):
    # # Find and click the login button
    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Sign In']"))
    ).click()

    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='username']"))
    ).send_keys("priska.phahla@gmail.com")
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys("201200xXx")
    driver.find_element(
        By.XPATH, "//button[@type='submit']//span[contains(text(),'Sign In')]"
    ).click()


def navigate_to_sports(driver: webdriver.Firefox):
    #  Click Sports
    time.sleep(3)
    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@class,'center') and contains(., 'Sport')]")
        )
    ).click()

    # click live for live sports
    time.sleep(3)
    if is_live_sports:
        WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Live']"))
        ).click()

    # click today
    else:
        WebDriverWait(driver=driver, timeout=__DRIVER_WAIT_PERIOD).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='today']"))
        ).click()

    WebDriverWait(driver=driver, timeout=__DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='e-sport-game']"))
    )

    time.sleep(__DRIVER_WAIT_PERIOD)
    __e_sport_live_games = driver.find_elements(
        By.XPATH, "//div[@data-testid='e-sport-game']"
    )

    return __e_sport_live_games


def bet_combo_lists():
    __teams_list = []
    __random_teams_combination = []

    # Launch the browser
    driver = webdriver.Firefox(options=options)
    driver.delete_all_cookies()

    # Open the website
    driver.get("https://www.gbets.co.ls/")
    time.sleep(__DRIVER_WAIT_FOR_BROWSER_LOAD_PERIOD)
    driver.execute_script("document.body.style.zoom='80%'")
    driver.set_window_position(10, -1280)  # x=1920
    driver.fullscreen_window()

    # login to the website
    sign_in(driver)

    # get the live e-sport games
    navigate_to_sports(driver)

    with open("teams.dat", "r") as __file:
        __matches_list = [team.strip() for team in __file.readlines() if team.strip()]
        # Generate all combinations of half the available matches
        if len(__matches_list) > 3:
            __match_combinations = list(
                combinations(
                    __matches_list,
                    __MATCHES_COMBINATIONS_LENGTH if len(__matches_list) >= 5 else 2,
                )
            )

            __random_teams_combination = random.sample(
                population=__match_combinations,
                k=len(__match_combinations) if len(__match_combinations) < 100 else 100,
            )
            __random_teams_combination = __random_teams_combination

        else:
            __random_teams_combination = [__matches_list]

        print(f"⚽️ ⚽️ ⚽️ Total Teams Matches Combinations: {len(__teams_list):<5}")

    if len(__random_teams_combination) == 0:
        print("⚽️ ⚽️ ⚽️ No E-Sports Teams Matches Found. Exiting...")
        driver.quit()
        return

    try:
        bet_gbets(
            driver=driver,
            match_groups_list=__random_teams_combination,
            browser_type="🔥-FIREFOX",
        )
    except Exception as e:
        print(f"⚠️ ⚠️ ⚠️ Error in betting Splitted Lists: {e}")
    
    driver.quit()
    del __teams_list
    del __random_teams_combination
    del driver
