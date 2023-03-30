import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
from .SearchByName import *

def get_random(msg,bot):
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.kinopoisk.ru/chance/")
    try:
        for i in range(1,0, -1):
            time.sleep(0.5)
        driver.find_element_by_class_name('button').click()
        for i in range(1,0, -1):
            time.sleep(0.5)
        driver.find_element_by_class_name("syn").click()
        for i in range(1,0, -1):
            time.sleep(0.5)
        name = driver.find_element_by_class_name("moviename-title-wrapper").text
        driver.close()
        if by_name(name, msg, bot) == '-1':
            return "-1"
    except NoSuchElementException:
            driver.close()
            return "-1"
        
