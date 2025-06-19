import time
import os
import math
import random
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
MINIMUM_TEAMS = 10
MATCHES_CHUNK_LENGTH = 7
DRIVER_WAIT_PERIOD = 60
DRIVER_WAIT_FOR_BROWSER_LOAD_PERIOD = 10

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


def sign_in(driver):
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


def navigate_to_sports(driver):
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

    return __e_sport_live_games


def bet_splitted_lists():
    __teams_list = []

    # Launch the browser
    driver = webdriver.Firefox(options=options)

    # Open the website
    driver.get("https://www.gbets.co.ls/")
    driver.execute_script("document.body.style.zoom='80%'")
    driver.set_window_position(10, -1280)  # x=1920
    driver.fullscreen_window()

    # wait for the browser to load
    time.sleep(DRIVER_WAIT_FOR_BROWSER_LOAD_PERIOD)

    try:
        sign_in(driver)
    except Exception as e:
        pass

    # get the live e-sport games
    navigate_to_sports(driver)

    with open("data/teams.split.data", "r") as __file:
        __teams_list = [team.strip() for team in __file.readlines() if team.strip()]
        __chunked_matches_lists = list(
            chunk_list(
                __teams_list,
                chunk_size=(
                    MATCHES_CHUNK_LENGTH if len(__teams_list) >= MINIMUM_TEAMS else 3
                ),
            )
        )

    if len(__chunked_matches_lists) == 0:
        driver.quit()
        return

    try:
        print(f"🧩 🧩 🧩 Total Teams: {len(__teams_list)}")
        print(f"🧩 🧩 🧩 Total Match Groups: {len(__chunked_matches_lists)}")

        bet_gbets(
            driver=driver,
            match_groups_list=__chunked_matches_lists,
            browser_type="🔥 🔥 🔥 - FIREFOX",
        )

        # sign out of the platform
        sign_out(driver=driver)
        driver.quit()
        del driver
        del __teams_list
    except Exception as e:
        print(f"⚠️ ⚠️ ⚠️ Error in betting Splitted Lists: {e}")
