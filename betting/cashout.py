import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import tempfile


os.system("clear")
is_live_sports = True
# GET GAMES LIST
__DRIVER_WAIT_PERIOD = 60
__CASHOUT_RATIO = 0.8

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
    time.sleep(3)

    # Set the title via JavaScript
    driver.execute_script("document.title = 'CASHOUT';")


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


def reload_results_and_table(driver):
    try:
        #  Click History
        WebDriverWait(driver, __DRIVER_WAIT_PERIOD).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'profileInfo__history-wrapper')]")
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
                (By.XPATH, "//div[@data-testid='results']")
            )
        )
        __result_selector.click()
        time.sleep(2)

        # select Not Resulted
        __result_options = driver.find_elements(
            By.XPATH,
            "//div[@data-testid='results_option']//div[normalize-space(text())='Not Resulted']",
        )

        if len(__result_options) == 0:
            return None

        __result_options[0].click()
    except Exception as e:
        return None
    time.sleep(10)

    # close results options
    __result_selector.click()

    # get results table
    __table_body = driver.find_elements(By.CSS_SELECTOR, "tbody.tableWrapper__tbody")
    if len(__table_body) == 0:
        return None

    return __table_body


def withdraw_cashout(driver, btn_cashout, cash, row, is_low_return: bool = True):
    if not btn_cashout:
        return

    # money back
    __cashout = cash

    try:
        # click cash out to open dialog
        print(f"[ {datetime.now()} ] -------- Click Action Cashout")
        if btn_cashout.is_displayed() and btn_cashout.is_enabled():
            driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});",
                btn_cashout,
            )
            btn_cashout.click()
        else:
            return

        if is_low_return:
            # if it's a low return, do partial cashout
            # click partial pay option
            print(f"[ {datetime.now()} ] -------- Click Partial Cashout")
            __partial_pay_radio = driver.find_elements(
                By.XPATH, "//*[normalize-space(text())='Partial Cashout']"
            )
            if len(__partial_pay_radio) == 0:
                return
            __partial_pay_radio[0].click()
            time.sleep(1)

            # find partial cashout input box and send keys
            print(f"[ {datetime.now()} ] -------- Send Input Partial Cashout")
            __partial_pay_input = driver.find_element(
                By.XPATH,
                "//input[@type='text' and contains(@class, 'v3-input') and contains(@class, 'v3-input-lg')]",
            )
            __cashout = f"{cash * __CASHOUT_RATIO:.2f}"
            __partial_pay_input.clear()
            __partial_pay_input.send_keys(__cashout)
            # time.sleep(2)

        # Wait for and click the button that contains the text 'Cash Out'
        print(f"[ {datetime.now()} ] -------- Click Cashout Button")
        WebDriverWait(driver=driver, timeout=__DRIVER_WAIT_PERIOD).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'v3-btn') and .//span[normalize-space(text())='Cash Out']]",
                )
            )
        ).click()
        time.sleep(5)

        try:
            __proceed_button = driver.find_elements(
                By.XPATH, "//*[normalize-space(text())='Proceed']"
            )
            if len(__proceed_button):
                __proceed_button[0].click()
                time.sleep(2)

                print(f"[ {datetime.now()} ] -------- Clicked Proceed")
                print(
                    f"[ {datetime.now()} ] 💼 💼 💼 Proceeded to Bag: {row:>5} | 💸 💸 💸 WIN: {__cashout:>5}"
                )
        except:
            pass

        # confirm cashout
        print(f"[ {datetime.now()} ] -------- Click Ok")
        time.sleep(5)
        __okay_button = driver.find_elements(
            By.XPATH,
            "//button[contains(@class, 'v3-btn') and .//span[normalize-space(text())='OK']]",
        )
        if not len(__okay_button):
            raise Exception("No Okay Button Found")
        __okay_button[0].click()

        print(
            f"[ {datetime.now()} ] 💼 💼 💼 Bagged: {row:>5} | 💸 💸 💸 WIN: {__cashout:>5}"
        )
        time.sleep(2)
        return
    except:
        print(f"[ {datetime.now()} ] -------- Click Cancel Button")
        __cancel_cashout = driver.find_elements(
            By.XPATH,
            "//button[contains(@class, 'v3-btn') and .//span[normalize-space(text())='Cancel']]",
        )
        if len(__cancel_cashout):
            __cancel_cashout[0].click()
            time.sleep(3)

        else:
            # will come here if cashed-out or failed and can't find ok button
            __modal_close = driver.find_elements(By.CLASS_NAME, "custom__modalClose")
            if len(__modal_close):
                __modal_close[0].click()
            time.sleep(3)
        print(
            f"[ {datetime.now()} ] 😩 😩 😩 Canceled: {row:>5} | ❌ ❌ ❌ LOSS: {__cashout:>5}"
        )


def gbets_cashout():
    __MINIMUM_CASHOUT_BASE = 0.10
    __POSSIBLE_WIN_LOWER_BOUND = 10
    __POSSIBLE_WIN_MEDIAN = 40
    __POSSIBLE_WIN_UPPER_BOUND = 100

    # Launch the browser
    driver = webdriver.Firefox(options=options)

    # Open the website
    driver.get("https://www.gbets.co.ls/")
    driver.execute_script("document.body.style.zoom='80%'")
    driver.set_window_position(10, -1280)  # x=1920
    driver.fullscreen_window()

    # log in to the account
    try:
        sign_in(driver)
        time.sleep(3)
    except Exception as e:
        raise

    while True:
        __table_body = reload_results_and_table(driver=driver)
        if not __table_body:
            try:
                sign_out(driver=driver)
            except:
                pass
            finally:
                driver.quit()
                return

        # get rows from not resulted
        time.sleep(3)
        __table_rows = __table_body[0].find_elements(
            By.CSS_SELECTOR, "tr.tableWrapper__body__row--expandable"
        )
        print(f"Cashout Table Rows:: {len(__table_rows)}")
        if len(__table_rows) == 0:
            break

        for i, __row in enumerate(__table_rows, 0):
            # find the first cashout option that has possible cashout
            try:
                time.sleep(5)
                __possible_cashout_elements = __row.find_elements(
                    By.XPATH,
                    ".//td[@class='tableBodyCell']//span[contains(text(), 'Possible Win')]",
                )

                # find the first cashout option that has cashout money
                __cashout_money_elements = __row.find_elements(
                    By.XPATH,
                    ".//span[@class='myBetsCashout__text']/span[starts-with(normalize-space(text()), 'LSL')]",
                )

                # find the first cashout option that has cashout money
                __stake_element = __row.find_elements(
                    By.XPATH,
                    ".//span[@class='betHistory__bonus-stake-style']",
                )

                # possible cashout
                if (
                    not len(__possible_cashout_elements)
                    or not len(__cashout_money_elements)
                    or not len(__stake_element)
                ):
                    continue

                # Extract the possible cashout and cashout money values
                __possible_cashout = float(
                    __possible_cashout_elements[0].text.split(" ")[-1]
                )

                __cashout_money = float(__cashout_money_elements[0].text.split(" ")[1])

                __stake = float(__stake_element[0].text.split(" ")[-1])

                # if __cashout_money >= __stake:
                print(
                    f"[[ 🧮 🧮 🧮 ]] [ {datetime.now()} ] Row: {i:<3} | Stake: {__stake} | Possible Cashout: {__possible_cashout:>3} | Cashout Money: {__cashout_money:>3}"
                )

                # Check if cashout money and possible cashout meet the criteria
                if (
                    __cashout_money > __POSSIBLE_WIN_LOWER_BOUND
                    and __cashout_money < __POSSIBLE_WIN_MEDIAN
                ):
                    time.sleep(2)
                    withdraw_cashout(
                        btn_cashout=__cashout_money_elements[0].find_element(
                            By.XPATH, "./../.."
                        ),
                        cash=__cashout_money,
                        row=i,
                        driver=driver,
                        is_low_return=True,
                    )
                    print(
                        f"[ {datetime.now()} ] 📉 📉 📉 Small Win: {i:<3} | Possible Cashout: {__possible_cashout:>5} | Cashout Money: {__cashout_money:>5}"
                    )

                elif (
                    __cashout_money >= __POSSIBLE_WIN_MEDIAN
                    and __cashout_money < __POSSIBLE_WIN_UPPER_BOUND
                ):
                    time.sleep(2)
                    withdraw_cashout(
                        btn_cashout=__cashout_money_elements[0].find_element(
                            By.XPATH, "./../.."
                        ),
                        cash=__cashout_money,
                        row=i,
                        driver=driver,
                        is_low_return=False,
                    )
                    print(
                        f"[ {datetime.now()} ] ⭐︎ ⭐︎ ⭐︎ Medium Win: {i:<3} | Possible Cashout: {__possible_cashout:>5} | Cashout Money: {__cashout_money:>5}"
                    )

                elif __cashout_money >= __POSSIBLE_WIN_UPPER_BOUND:
                    time.sleep(2)
                    withdraw_cashout(
                        btn_cashout=__cashout_money_elements[0].find_element(
                            By.XPATH, "./../.."
                        ),
                        cash=__cashout_money,
                        row=i,
                        driver=driver,
                        is_low_return=False,
                    )
                    print(
                        f"[ {datetime.now()} ] 🚛 🚛 🚛 Big Win: {i:<3} | Possible Cashout: {__possible_cashout:>5} | Cashout Money: LSL{__cashout_money:>5}"
                    )

                elif __cashout_money >= __MINIMUM_CASHOUT_BASE:
                    time.sleep(2)
                    withdraw_cashout(
                        btn_cashout=__cashout_money_elements[0].find_element(
                            By.XPATH, "./../.."
                        ),
                        cash=__cashout_money,
                        row=i,
                        driver=driver,
                        is_low_return=True,
                    )
                    print(
                        f"[ {datetime.now()} ] 🔻 🔻 🔻 Lowest Win: {i:<3} | Possible Cashout: {__possible_cashout:>5} | From: LSL{__cashout_money:>5}"
                    )

                del __possible_cashout_elements
                del __possible_cashout
                del __cashout_money_elements
                del __cashout_money
                del __stake_element
                del __stake
                time.sleep(5)
            except:
                # close modal
                __close_header = driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class, 'accountModal__header__title')]/following-sibling::*",
                )
                __close_header[0].click()
                break

    try:
        # sign out
        sign_out(driver=driver)
    except:
        pass
    finally:
        driver.quit()
        return
