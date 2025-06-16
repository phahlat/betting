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
import tempfile

os.system("clear")
is_live_sports = True
# GET GAMES LIST
__MATCHES_CHUNK_LENGTH = 7
__DRIVER_WAIT_PERIOD = 60
__DRIVER_WAIT_FOR_BROWSER_LOAD_PERIOD = 15

# Optional: configure Chrome to stay open
# Create a temporary directory
user_data_dir = tempfile.mkdtemp()

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
# chrome_options.add_argument("--headless=new")  # Headless mode

# Disable browser notification popups
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)


def sign_in(driver: webdriver.Chrome):
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


def navigate_to_sports(driver: webdriver.Chrome):
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


def bet_splitted_lists():
    __teams_list = []

    # Launch the browser
    driver = webdriver.Chrome(options=chrome_options)

    # Open the website
    driver.get("https://www.gbets.co.ls/")
    driver.execute_script("document.body.style.zoom='80%'")
    driver.set_window_position(10, -1280)  # x=1920
    driver.fullscreen_window()

    # wait for the browser to load
    print(
        f"🌐 🌐 🌐 Waiting for the browser to load... {driver._check_if_window_handle_is_current}"
    )
    time.sleep(__DRIVER_WAIT_FOR_BROWSER_LOAD_PERIOD)

    # login to the website
    print(
        f"🔐 🔐 🔐 Signing in to GBets... {driver._check_if_window_handle_is_current}"
    )
    sign_in(driver)

    # get the live e-sport games
    navigate_to_sports(driver)

    with open("teams.dat", "r") as __file:
        __teams_list = [team.strip() for team in __file.readlines() if team.strip()]

        print(f"⚽️ ⚽️ ⚽️ Total E-Sports Teams Matches: {len(__teams_list)}")
        __chunked_matches_lists = list(
            chunk_list(
                __teams_list,
                chunk_size=(__MATCHES_CHUNK_LENGTH if len(__teams_list) >= 10 else 3),
            )
        )

        __match_groups_length = len(__chunked_matches_lists)
        print(f"🧩 🧩 🧩 Total Initial Match Groups: {__match_groups_length}")

    if len(__chunked_matches_lists) == 0:
        print("⚽️ ⚽️ ⚽️ No E-Sports Teams Matches Found. Exiting...")
        driver.quit()
        return

    try:
        bet_gbets(
            driver=driver,
            match_groups_list=__chunked_matches_lists,
            browser_type="☢️ - CHROME",
        )
    except Exception as e:
        print(f"⚠️ ⚠️ ⚠️ Error in betting Splitted Lists: {e}")
        raise

    driver.quit()
    del driver
    del __teams_list

    # WRITE PROCESS NAMES FOR CLARITY
