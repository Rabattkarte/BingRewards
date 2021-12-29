import json
import os
import random
import time

import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# TODO: test for ENV vars being set
load_dotenv()  # take environment variables from .env
username = os.getenv("MSFT_USERNAME")
password = os.getenv("MSFT_PASSWORD")
remote_host = os.getenv("SELENIUM_REMOTE_HOST", "localhost")
remote_port = os.getenv("SELENIUM_REMOTE_PORT", "4444")
count_words = int(os.getenv("NUMBER_OF_WORDS", 60))

remote_url = "http://" + remote_host + ":" + remote_port
bing_url_base = "http://www.bing.com/search?q="

randomlists_url = "https://www.randomlists.com/data/words.json"
words_list = random.sample(json.loads(
    requests.get(randomlists_url).text)["data"], count_words)

print("{0} words selected from {1}".format(len(words_list), randomlists_url))

# Establish connection to selenium/standalone-edge container
driver = webdriver.Remote(command_executor=remote_url)

try:
    driver.get("https://login.live.com/")
    form_user = driver.find_element(By.NAME, "loginfmt")
    form_user.clear()
    form_user.send_keys(username + Keys.RETURN)

    time.sleep(5)
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable("passwd"))

    form_pass = driver.find_element(By.NAME, "passwd")
    form_pass.clear()
    form_pass.send_keys(password + Keys.ENTER)

    try:
        print("Waiting for 2FA ack ...")
        WebDriverWait(driver, 999999999).until(EC.url_contains("route=R3_BL2"))
    except TimeoutException as t:
        print("TimeoutException for 2FA. " + t)
        driver.quit()
        quit()

except Exception as e:
    print(e)
    time.sleep(4)

for num, word in enumerate(words_list):
    print("{0}. URL : {1}".format(str(num + 1), bing_url_base + word))
    try:
        driver.get(bing_url_base + word)
        # print("\t" + driver.find_element(By.TAG_NAME, "h2").text)
        print("\t" + driver.title)
    except Exception as e1:
        print(e1)
    time.sleep(10)

driver.quit()
