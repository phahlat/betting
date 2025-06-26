import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import tempfile

os.system("clear")
is_live_sports = True
DRIVER_WAIT_PERIOD = 60
MINIMUM_GAMES = 5
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

    # wait for e-sport games to load
    WebDriverWait(driver=driver, timeout=DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='e-sport-game']"))
    )

    # wait for the e-sport games to load
    __left_sidebar = WebDriverWait(driver=driver, timeout=DRIVER_WAIT_PERIOD).until(
        EC.visibility_of_element_located((By.ID, "prematch-left-sidebar-wrapper"))
    )

    # Locate the last child of the wrapper
    last_child = __left_sidebar.find_elements(By.XPATH, "./*")[-1]

    # Scroll smoothly to the last child
    driver.execute_script(
        """
        arguments[0].scrollIntoView({ behavior: 'smooth', block: 'end' });
    """,
        last_child,
    )

    # get the e-sport live games
    time.sleep(15)
    __get_e_games = driver.find_elements(By.XPATH, "//div[@data-testid='e-sport-game']")

    return __get_e_games


def get_teams():
    # Launch the browser
    driver = webdriver.Firefox(options=options)

    # Open the website
    driver.get("https://www.gbets.co.ls/")
    driver.execute_script("document.body.style.zoom='80%'")
    driver.set_window_position(10, -1280)  # x=1920
    driver.maximize_window()

    # login to the website
    try:
        sign_in(driver)
    except:
        pass

    # get the live e-sport games
    __get_e_games = navigate_to_sports(driver)

    print(f"⚽️ ⚽️ ⚽️ E-Sports Games Count: {len(__get_e_games):<5}")
    # get match teams
    with open("data/teams.split.data", "w") as __split_teams_file:
        with open("data/teams.combo.data", "w") as __combo_teams_file:
            for _game in __get_e_games:
                if len(__get_e_games) < MINIMUM_GAMES:
                    pass

                # find teams
                __teams = _game.find_elements(By.CLASS_NAME, "comp__teamName__wrapper")
                if len(__teams) == 0:
                    continue

                # get time of match
                # get goals at the time
                __time = _game.find_element(By.CSS_SELECTOR, "div.custom__row")

                # write split
                print(
                    f"{__teams[0].text.strip()}:{__teams[1].text.strip() if len(__teams) == 2 else 'OTHER'}|{__time.text.strip()}",
                    file=__split_teams_file,
                )

                # write combo
                print(
                    f"{__teams[0].text.strip()}:{__teams[1].text.strip() if len(__teams) == 2 else 'OTHER'}|{__time.text.strip()}",
                    file=__combo_teams_file,
                )

        __combo_teams_file.close()
        __split_teams_file.close()

        try:
            sign_out(driver=driver)
        except:
            pass
        print(f"⚽️ ⚽️ ⚽️ Done!!!\n")

    driver.quit()
    del driver
    del __get_e_games
