import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
from .SearchByName import *

def by_director(in_director, msg,bot):
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.kinopoisk.ru/")
    elem = driver.find_element_by_name("kp_query")
    elem.clear()
    elem.send_keys(in_director)
    elem.send_keys(Keys.RETURN) 
    for i in range(1,0, -1):
        time.sleep(1)
    try:
        driver.find_element_by_partial_link_text(in_director).click()
        for i in range(1,0, -1):
                    time.sleep(0.5)
        name = driver.find_element_by_tag_name("h1").text
        get_stars = driver.find_elements_by_tag_name("li")
        film1 = get_stars[7].text
        film2 = get_stars[8].text
        film3 = get_stars[9].text
        driver.close()
        by_name(film1,msg,bot)
        by_name(film2,msg,bot)
        by_name(film3,msg,bot)
    except:
        driver.close()
        return '-1'


