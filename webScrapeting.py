import requests
import re
import json
import pandas as pd
import datetime
import os
import time

# from seleniumbase import Driver
# from seleniumbase import BaseCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#from webscrape_objects import Journey


station_json_url = "https://book.splitmyfare.co.uk/static/js/57.80112f8e.chunk.js"




## TODO: use enquirey object to get the search link
def get_search_link(from_alpha3, to_alpha3, departure, adults=1, children=0):

    ## get the raw text from the link
    response = requests.get(station_json_url)
    raw_text = response.text

    # Extract the string passed to JSON.parse
    match = re.search(r"JSON\.parse\('(.*)'\)", raw_text, re.DOTALL)
    if match:

        ## extract and parse the JSON string
        json_string = match.group(1)
        json_string = json_string.replace("\\", "\\\\") # Replace single backslashes with double backslashes
        data = json.loads(json_string)

        ## create a dictionary mapping alpha3 to unique code
        alpha3_to_uic = {}
        for entry in data:
            if 'crs' in entry and 'uic' in entry and entry['uic'] != '':
                alpha3_to_uic[entry['crs']] = entry['uic']

        ## get the unique code for the start and end stations
        from_uic = alpha3_to_uic[from_alpha3]
        to_uic = alpha3_to_uic[to_alpha3]

        ## create and return the search link
        if from_uic and to_uic:
            return f"https://book.splitmyfare.co.uk/search?from={from_uic}&to={to_uic}&adults={adults}&children={children}&departureDate={departure.strftime('%Y-%m-%d')}T{departure.strftime('%H:%M')}"
        return None


def get_journeys(url):

    something_wrong_xpath = "//*[@id=\"root\"]/div[2]/div/div[2]/div/div/div[2]/a/button"
    search_again_xpath = "//*[@id=\"root\"]/div/div/div/div[2]/button"

    journeys_xpath = "//*[@id=\"root\"]/div/div/div[3]/div/div/div[2]"
    time_span_xpath = "//*[@id=\"root\"]/div[1]/div/div[2]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/span"
    price_div_xpath = "//*[@id=\"root\"]/div[1]/div/div[2]/div/div[1]/div[3]/div[2]/div[2]/div[1]/div[2]"

    # driver = Driver(uc=True, undetectable=True)
    driver = webdriver.Chrome()

    driver.get(url)

    ## you must be a bot... click the button and prove you're not!
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, something_wrong_xpath)))
    button.click()

    ## reapply the search
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, search_again_xpath)))
    button.click()

    journeys = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, journeys_xpath)))

    ## WWWWWWWWWWHHHHHHHHHHHHYYYYYYYYYYYYYYYY
    ## does not work.....
    html = driver.page_source
    print(html)
    print(journeys.text)



start_alpha3 = "NRW"
end_alpha3 = "LST"
departure = (datetime.datetime.now() + datetime.timedelta(days=1)) .replace (hour=9, minute=0, second=0, microsecond=0)

# url = get_search_link("NRW", "LST", departure)
url = "https://book.splitmyfare.co.uk/search?from=7073090&to=7069650&adults=1&children=0&departureDate=2024-05-08T09:00"
print(url)
print()
journeys = get_journeys(url)