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
from players import gbets_player_bet_combo, gbets_player_bet_split
import threading
import tempfile

os.system("clear")
is_live_sports = True
# GET GAMES LIST
__MATCHES_CHUNK_LENGTH = 10
__MATCHES_COMBINATIONS_LENGTH = 7
__DRIVER_WAIT_PERIOD = 60

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

    # wait for e-sport games to load
    WebDriverWait(driver=driver, timeout=__DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='e-sport-game']"))
    )

    # wait for the e-sport games to load
    __left_sidebar = WebDriverWait(driver=driver, timeout=__DRIVER_WAIT_PERIOD).until(
        EC.visibility_of_element_located((By.ID, "prematch-left-sidebar-wrapper"))
    )

    # Locate the last child of the wrapper
    last_child = __left_sidebar.find_elements(By.XPATH, "./*")[
        -1
    ]  # All direct children, pick last

    # Scroll smoothly to the last child
    driver.execute_script(
        """
        arguments[0].scrollIntoView({ behavior: 'smooth', block: 'end' });
    """,
        last_child,
    )

    # driver.execute_script("arguments[0].style.scrollBehavior = 'smooth';arguments[0].scrollTop = arguments[0].scrollHeight;", __left_sidebar)
    print("Scrolling to the bottom of the left sidebar to load all e-sport games...")

    # wait for the e-sport games to load
    # get the e-sport live games
    time.sleep(__DRIVER_WAIT_PERIOD)
    __e_sport_live_games = driver.find_elements(
        By.XPATH, "//div[@data-testid='e-sport-game']"
    )

    return __e_sport_live_games


def get_teams():
    # Launch the browser
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
    driver.execute_cdp_cmd('Network.clearBrowserCache', {})

    # Open the website
    driver.get("https://www.gbets.co.ls/")
    driver.execute_script("document.body.style.zoom='80%'")
    # driver.set_window_position(10, -1280)  # x=1920
    driver.fullscreen_window()

    # login to the website
    sign_in(driver)

    # get the live e-sport games
    __e_sport_live_games = navigate_to_sports(driver)

    print(f"⚽️ ⚽️ ⚽️ E-Sports Games Length:: {len(__e_sport_live_games)}")
    # get match teams
    with open("teams.dat", "w") as __file:
        for _game in __e_sport_live_games:
            __teams = _game.find_elements(By.CLASS_NAME, "comp__teamName__wrapper")
            if len(__teams) == 0:
                continue

            print(
                f"{__teams[0].text}:{__teams[1].text if len(__teams) == 2 else 'OTHER'.split('\n')}",
                file=__file,
            )

    driver.quit()
    del driver
    del __e_sport_live_games
