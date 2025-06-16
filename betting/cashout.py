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
from datetime import datetime


os.system("clear")
is_live_sports = True
# GET GAMES LIST
__DRIVER_WAIT_PERIOD = 60

# Optional: configure Chrome to stay open
# Create a temporary directory
user_data_dir = tempfile.mkdtemp()

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# Disable browser notification popups
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)


def reload_results_and_table(driver: webdriver.Chrome):
    #  Click History
    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable(
            (By.XPATH,
             "//div[contains(@class,'profileInfo__history-wrapper')]")
        )
    ).click()

    # wait for data to appear
    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//th[normalize-space(text())='Date/ID/Bet Type']")
        )
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
        By.XPATH, "//div[@data-testid='results_option']"
    )
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


def withdraw_cashout(btn_cashout, cash, row, driver):
    # Click the cashout button
    btn_cashout.click()
    
    print(f"[ {datetime.now()} ] 💰 💰 💰 Cashing out: {row:>5} | Cashout Money: {cash:>5}")

    # Wait for and click the button that contains the text 'Cash Out'
    WebDriverWait(driver=driver, timeout=__DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(@class, 'v3-btn') and .//span[normalize-space(text())='Cash Out']]",
            )
        )
    ).click()

    # wait for the proceed modal to appear
    try:
        time.sleep(5)
        proceed_buttons = driver.find_elements(
            By.XPATH, "//*[normalize-space(text())='Proceed']"
        )
        if proceed_buttons[0].is_displayed() and proceed_buttons[0].is_enabled():
            proceed_buttons[0].click()

        # WebDriverWait(driver=driver, timeout=__DRIVER_WAIT_PERIOD).until(
        #     EC.element_to_be_clickable(
        #         (By.XPATH,
        #             "[//*[normalize-space(text())='Proceed']]")
        #     )
        # ).click()

        print(
            f"[ {datetime.now()} ] 💼 💼 💼 Bagged: {row:>5} | 💸 💸 💸 WIN: {cash:>5}"
        )
        return
    except:
        pass

    # confirm cashout
    try:
        WebDriverWait(driver=driver, timeout=__DRIVER_WAIT_PERIOD).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'v3-btn') and .//span[normalize-space(text())='OK']]",
                )
            )
        ).click()
        print(
            f"[ {datetime.now()} ] 💼 💼 💼 Bagged: {row:>5} | 💸 💸 💸 WIN: {cash:>5}"
        )
        return
    except:
        WebDriverWait(driver=driver, timeout=__DRIVER_WAIT_PERIOD).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'v3-btn') and .//span[normalize-space(text())='Cancel']]",
                )
            )
        ).click()
        print(
            f"[ {datetime.now()} ] 😩 😩 😩 Canceled: {row:>5} | ❌ ❌ ❌ LOSS: {cash:>5}"
        )
        return


def gbets_cashout():
    __CASHOUT_LOWER_BOUND = 2
    __CASHOUT_MEDIAN = 10
    __CASHOUT_UPPER_BOUND = 20

    __POSSIBLE_WIN_LOWER_BOUND = 5
    __POSSIBLE_WIN_MEDIAN = 10
    __POSSIBLE_WIN_UPPER_BOUND = 100

    # Launch the browser
    driver = webdriver.Chrome(options=chrome_options)

    # Open the website
    driver.get("https://www.gbets.co.ls/")
    driver.execute_script("document.body.style.zoom='80%'")
    driver.set_window_position(10, -1280)  # x=1920
    driver.fullscreen_window()

    # # Find and click the login button
    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[normalize-space()='Sign In']"))
    ).click()

    WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='username']"))
    ).send_keys("priska.phahla@gmail.com")
    driver.find_element(
        By.XPATH, "//input[@id='password']").send_keys("201200xXx")
    driver.find_element(
        By.XPATH, "//button[@type='submit']//span[contains(text(),'Sign In')]"
    ).click()
    time.sleep(3)

    while True:
        # load results table
        __table_body = reload_results_and_table(driver=driver)
        if not __table_body:
            print(f"[ {datetime.now()} ] No results found, retrying...")
            time.sleep(15)
            continue

        # get rows from not resulted
        __table_rows = __table_body[0].find_elements(
            By.CSS_SELECTOR, "tr.v3-table-row.v3-table-row-level-0"
        )
        
        for i, __row in enumerate(__table_rows, 0):
            # find the first cashout option that has possible cashout
            __possible_cashout_elements = __row.find_elements(
                By.XPATH,
                ".//td[@class='v3-table-cell']//span[contains(text(), 'Possible Win')]",
            )
            
            # find the first cashout option that has cashout money
            __cashout_money_elements = __row.find_elements(
                By.XPATH,
                ".//span[@class='myBetsCashout__text']/span[starts-with(normalize-space(text()), 'LSL')]",
            )
            if not len(__possible_cashout_elements) or not len(__cashout_money_elements):
                print(
                    f"[[ 👀 👀 👀 ]] [ {datetime.now()} ] COUNT: Possible Cashout: {len(__cashout_money_elements)} -- Cashout: {len(__possible_cashout_elements)}")
                continue
            
            # Extract the possible cashout and cashout money values
            __possible_cashout = float(
                __possible_cashout_elements[0].text.split(" ")[-1]
            )
            __cashout_money = float(
                __cashout_money_elements[0].text.split(" ")[1])

            print(
                f"[[ 👀 👀 👀 ]] [ {datetime.now()} ] Row: {i:>5} | Possible Cashout: {__possible_cashout:>5} | Cashout Money: {__cashout_money:>5} LOW {__CASHOUT_LOWER_BOUND}: {__cashout_money > __CASHOUT_LOWER_BOUND and __possible_cashout > __POSSIBLE_WIN_LOWER_BOUND and __possible_cashout < __POSSIBLE_WIN_MEDIAN} -- MEDIUM {__CASHOUT_MEDIAN}: {__cashout_money > __CASHOUT_MEDIAN and __possible_cashout > __POSSIBLE_WIN_MEDIAN and __possible_cashout < __POSSIBLE_WIN_UPPER_BOUND} -- HIGH {__CASHOUT_UPPER_BOUND}: {__cashout_money > __CASHOUT_UPPER_BOUND and __possible_cashout > __POSSIBLE_WIN_UPPER_BOUND}"
            )

            # Check if cashout money and possible cashout meet the criteria
            if (
                __cashout_money > __CASHOUT_LOWER_BOUND
                and __possible_cashout >= __POSSIBLE_WIN_LOWER_BOUND
                and __possible_cashout < __POSSIBLE_WIN_MEDIAN
            ):
                withdraw_cashout(
                    btn_cashout=__cashout_money_elements[0],
                    cash=__cashout_money,
                    row=i,
                    driver=driver,
                )
                print(
                    f"[ {datetime.now()} ] 💰 💰 💰 Small Win: {i:>5} | Possible Cashout: {__possible_cashout:>5} | Cashout Money: {__cashout_money:>5}"
                )
            elif (
                __cashout_money >= __CASHOUT_MEDIAN
                and __possible_cashout >= __POSSIBLE_WIN_MEDIAN
                and __possible_cashout < __POSSIBLE_WIN_UPPER_BOUND
            ):
                withdraw_cashout(
                    btn_cashout=__cashout_money_elements[0],
                    cash=__cashout_money,
                    row=i,
                    driver=driver,
                )
                print(
                    f"[ {datetime.now()} ] 💰 💰 💰 Medium Win: {i:>5} | Possible Cashout: {__possible_cashout:>5} | Cashout Money: {__cashout_money:>5}"
                )
            elif (
                __cashout_money >= __CASHOUT_UPPER_BOUND
                and __possible_cashout > __POSSIBLE_WIN_UPPER_BOUND
            ):
                withdraw_cashout(
                    btn_cashout=__cashout_money_elements[0],
                    cash=__cashout_money,
                    row=i,
                    driver=driver,
                )
                print(
                    f"[ {datetime.now()} ] 💰 💰 💰 Big Win: {i:>5} | Possible Cashout: {__possible_cashout:>5} | Cashout Money: {__cashout_money:>5}"
                )
            else:
                print(
                    f"[ {datetime.now()} ] 😒 😒 😒 Nothing Withdrawable: {i:>5} | Possible Cashout: {__possible_cashout:>5} | Cash: {__cashout_money:>5}\n"
                )

            del __cashout_money
            del __possible_cashout

        __close_header = driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'accountModal__header__title')]/following-sibling::*",
        )
        __close_header[0].click()
        time.sleep(15)

    driver.quit()
