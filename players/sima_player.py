import time
import os
import math
import random
from itertools import combinations
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from betting.bet import bet_sima


os.system("clear")

# Optional: configure Chrome to stay open
options = Options()
options.add_experimental_option("detach", True)

# Launch the browser
driver = webdriver.Chrome(options=options)

# Open the website
driver.get('https://www.simacombet.com/')
driver.maximize_window()

# close add box
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(
        (By.XPATH, "//i[@class='n-i n-i-close-a']"))
).click()

# Find and click the login button
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "button-login"))
).click()


WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, 'modal-header-title'))
)
driver.find_element(
    By.XPATH, "//input[@placeholder='E-mail']").send_keys('priska.phahla@gmail.com')
driver.find_element(
    By.XPATH, "//input[@placeholder='Password']").send_keys('201200xXx')
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Wait for overlay to disappear
WebDriverWait(driver, 10).until(
    EC.invisibility_of_element_located((By.CLASS_NAME, "overlay-wrap"))
)

#  Click Sports
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(
        (By.XPATH, "//span[normalize-space()='Sports']"))
).click()

# Enter Frame
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "PluginSMGatewayPrematch"))
)
driver.switch_to.frame(driver.find_element(By.ID, "PluginSMGatewayPrematch"))

# Click Soccer
WebDriverWait(driver=driver, timeout=20).until(
    EC.visibility_of_element_located(
        (By.XPATH, "//span[normalize-space()='Soccer']"))
).click()

WebDriverWait(driver=driver, timeout=20).until(
    EC.visibility_of_element_located(
        (By.XPATH, f"//div[contains(@class, 'event-row')]"))
).click()

match_list = [_.text for _ in driver.find_elements(
    By.CLASS_NAME, "event-wrap-name")]

# Generate all combinations of 4 matches
if len(match_list) > 2:
    match_combinations = list(combinations(
        match_list, math.ceil(len(match_list)/2)))
else:
    match_combinations = [match_list,]

print(
    f"Matches: {len(match_list)} \nPossible Bets Total: {len(match_combinations)}")

# Randomly pick 6 combinations to bet on
random_bets = random.sample(match_combinations, 2)

bet_sima(driver=driver, matches=random_bets)

time.sleep(10)
driver.quit()
