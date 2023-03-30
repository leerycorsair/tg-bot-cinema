import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time

def by_name(in_name, msg, bot):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.kinopoisk.ru/")
        elem = driver.find_element_by_name("kp_query")
        elem.clear()
        elem.send_keys(in_name)
        elem.send_keys(Keys.RETURN)
        for i in range(1,0, -1):
            time.sleep(0.5)
        driver.find_element_by_partial_link_text(in_name).click()
        for i in range(1,0, -1):
            time.sleep(0.5)
        get_name = driver.find_element_by_tag_name("h1").text
        name = get_name
        get_data = driver.find_elements_by_tag_name("tr")
        data = ''.join(get_data[0].text)
        get_stars = driver.find_elements_by_tag_name("li")
        star1 = get_stars[4].text
        star2 = get_stars[5].text
        star3 = get_stars[6].text
        driver.find_element_by_id("online-view-options-watch-button").click()
        for i in range(1,0, -1):
            time.sleep(0.5)
        get_url = driver.current_url
        url = get_url
        driver.close()
        if len(url) == 0:
            return '-1'
        else:
            txt = '🎞'+ name+ '\n' + '📆'+' '.join(data.split('\n'))+ '\n' +'🌟' +star1+ '\n' +'🌟' + star2+ '\n' +'🌟' + star3+ '\n' + url
            bot.send_message(msg.chat.id, text = txt)
    except:
        driver.close()
        return '-1'

