import time
import os
import math
import random
from itertools import combinations
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from betting.bet import bet_gbets, chunk_list
import tempfile

os.system("clear")
is_live_sports = True
# GET GAMES LIST
MINIMUM_TEAMS = 12
MINIMUM_ACCEPTABLE_TEAMS = 8
TEAMS_COMBINATIONS_LENGTH = 10
MATCHES_MAX_COMBINATIONS_LENGTH = 100
DRIVER_WAIT_PERIOD = 60
DRIVER_WAIT_FOR_BROWSER_LOAD_PERIOD = 10

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
    WebDriverWait(driver, DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Sign In']"))
    ).click()

    WebDriverWait(driver, DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='username']"))
    ).send_keys("priska.phahla@gmail.com")
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys("201200xXx")
    driver.find_element(
        By.XPATH, "//button[@type='submit']//span[contains(text(),'Sign In')]"
    ).click()


def sign_out(driver):
    # # Find and click the login button
    __profile_button = driver.find_elements(
        By.CSS_SELECTOR, ".v3-dropdown-trigger.profileInfo__circleButton"
    )
    if len(__profile_button) == 0:
        pass
    ActionChains(driver).move_to_element(__profile_button[0]).perform()
    time.sleep(3)
    __logout = driver.find_elements(By.XPATH, "//div[normalize-space(text())='Logout']")
    if len(__logout) == 0:
        return
    __logout[0].click()
    time.sleep(5)


def navigate_to_sports(driver: webdriver.Firefox):
    #  Click Sports
    time.sleep(3)
    WebDriverWait(driver, DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@class,'center') and contains(., 'Sport')]")
        )
    ).click()

    # click live for live sports
    time.sleep(3)
    if is_live_sports:
        WebDriverWait(driver, DRIVER_WAIT_PERIOD).until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Live']"))
        ).click()

    # click today
    else:
        WebDriverWait(driver=driver, timeout=DRIVER_WAIT_PERIOD).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='today']"))
        ).click()

    WebDriverWait(driver=driver, timeout=DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='e-sport-game']"))
    )

    time.sleep(DRIVER_WAIT_PERIOD)
    __e_sport_live_games = driver.find_elements(
        By.XPATH, "//div[@data-testid='e-sport-game']"
    )

    # Set the title via JavaScript
    driver.execute_script("document.title = 'BET COMBO';")

    return __e_sport_live_games


def bet_combo_lists():
    __teams_list = []
    __random_teams_combination = []
    __match_combinations = []

    # Launch the browser
    driver = webdriver.Firefox(options=options)
    driver.delete_all_cookies()

    # Open the website
    driver.get("https://www.gbets.co.ls/")
    time.sleep(DRIVER_WAIT_FOR_BROWSER_LOAD_PERIOD)
    driver.execute_script("document.body.style.zoom='80%'")
    driver.set_window_position(10, -1280)  # x=1920
    driver.fullscreen_window()

    # login to the website
    try:
        sign_in(driver)
    except Exception as e:
        pass

    # get the live e-sport games
    navigate_to_sports(driver)

    with open("data/teams.combo.data", "r") as __file:
        __teams_list = [
            team.strip().replace("\n", "")
            for team in __file.readlines()
            if team.strip()
        ]
        __first_half_teams = [
            s.split("|")[0]
            for s in __teams_list
            if "1st Half".lower() in str(s).lower()
        ]

        __second_half_teams = [
            s.split("|")[0]
            for s in __teams_list
            if "2nd Half".lower() in str(s).lower()
            or "3rd Half".lower() in str(s).lower()
            or "4th Half".lower() in str(s).lower()
        ]

        __half_time_teams = [
            s.split("|")[0]
            for s in __teams_list
            if "Half Time".lower() in str(s).lower()
        ]

        __not_started_teams = [
            s.split("|")[0]
            for s in __teams_list
            if "Not Started".lower() in str(s).lower()
        ]

        # Generate all combinations of half the available matches
        if len(__first_half_teams) >= MINIMUM_ACCEPTABLE_TEAMS:
            __first_half_teams = list(
                combinations(
                    __first_half_teams,
                    (
                        TEAMS_COMBINATIONS_LENGTH
                        if len(__first_half_teams) >= MINIMUM_TEAMS
                        else 3
                    ),
                )
            )
            __first_half_teams = random.sample(
                population=__first_half_teams,
                k=(
                    len(__first_half_teams)
                    if len(__first_half_teams) < MATCHES_MAX_COMBINATIONS_LENGTH
                    else MATCHES_MAX_COMBINATIONS_LENGTH
                ),
            )
            __match_combinations = __match_combinations + [__first_half_teams]
        else:
            __match_combinations = __match_combinations + [__first_half_teams]

        print(
            f"🧩 🧩 🧩 First Half: Total Teams Matches Combinations: {len(__first_half_teams):<5}"
        )

        if len(__second_half_teams) >= MINIMUM_ACCEPTABLE_TEAMS:
            __second_half_teams = list(
                combinations(
                    __second_half_teams,
                    (
                        TEAMS_COMBINATIONS_LENGTH
                        if len(__second_half_teams) >= MINIMUM_TEAMS
                        else 3
                    ),
                )
            )
            __second_half_teams = random.sample(
                population=__second_half_teams,
                k=(
                    len(__second_half_teams)
                    if len(__second_half_teams) < MATCHES_MAX_COMBINATIONS_LENGTH
                    else MATCHES_MAX_COMBINATIONS_LENGTH
                ),
            )
            __match_combinations = __match_combinations + [__second_half_teams]
        else:
            __match_combinations = __match_combinations + [__second_half_teams]

        print(
            f"🧩 🧩 🧩  Second Half: Total Teams Matches Combinations: {len(__second_half_teams):<5}"
        )

        if len(__half_time_teams) >= MINIMUM_ACCEPTABLE_TEAMS:
            __half_time_teams = list(
                combinations(
                    __half_time_teams,
                    (
                        TEAMS_COMBINATIONS_LENGTH
                        if len(__half_time_teams) >= MINIMUM_TEAMS
                        else 3
                    ),
                )
            )

            __half_time_teams = random.sample(
                population=__half_time_teams,
                k=(
                    len(__half_time_teams)
                    if len(__half_time_teams) < MATCHES_MAX_COMBINATIONS_LENGTH
                    else MATCHES_MAX_COMBINATIONS_LENGTH
                ),
            )
            __match_combinations = __match_combinations + [__half_time_teams]
        else:
            __match_combinations = __match_combinations + [__half_time_teams]

        print(
            f"🧩 🧩 🧩 Half Time: Total Teams Matches Combinations: {len(__half_time_teams):<5}"
        )

        if len(__not_started_teams) >= MINIMUM_ACCEPTABLE_TEAMS:
            __not_started_teams = list(
                combinations(
                    __not_started_teams,
                    (
                        TEAMS_COMBINATIONS_LENGTH
                        if len(__not_started_teams) >= MINIMUM_TEAMS
                        else 3
                    ),
                )
            )
            __not_started_teams = random.sample(
                population=__not_started_teams,
                k=(
                    len(__not_started_teams)
                    if len(__not_started_teams) < MATCHES_MAX_COMBINATIONS_LENGTH
                    else MATCHES_MAX_COMBINATIONS_LENGTH
                ),
            )

            __match_combinations = __match_combinations + [__not_started_teams]
        else:
            __match_combinations = __match_combinations + [__not_started_teams]

        print(
            f"🧩 🧩 🧩 Not Started: Total Teams Matches Combinations: {len(__not_started_teams):<5}"
        )

    if len(__match_combinations) == 0:
        try:
            sign_out(driver=driver)
        except:
            pass

        driver.quit()
        return

    try:
        print(f"🧩 🧩 🧩 --- Total Combinations: {len(__match_combinations):<5}")
        bet_gbets(
            driver=driver,
            match_groups_list=__match_combinations,
            browser_type="🔥 🔥 🔥 - FIREFOX",
        )

        try:
            sign_out(driver=driver)
        except:
            pass

        driver.quit()
        del __teams_list
        del __random_teams_combination
        del driver

    except Exception as e:

        driver.quit()
        del driver
