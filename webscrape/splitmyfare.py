import requests
import re
import json
import pandas as pd
import socket

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service

from utils import JourneyType, TimeCondition
from utils import Enquiry, Journey



STATION_CODE_JS_URL = "https://book.splitmyfare.co.uk/static/js/59.ff0845d3.chunk.js"

SOMETHING_WRONG_XPATH        = "/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/a/button"
SEARCH_AGAIN_XPATH           = "/html/body/div[1]/div[1]/div/div/div[2]/button"
OUTBOUND_CONTAINER_DIV_XPATH = "/html/body/div[1]/div[1]/div/div[2]/div/div[1]/div[3]"

driver = None


def init_driver():
    global driver
    if socket.gethostname() == "Gordon": ## because conda is a pain
        service = Service(executable_path="C:\Program Files\chromedriver-win64\chromedriver.exe")
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome()
        
def wait_xpath_ret(xpath, timeout=3):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))

def get_xpaths_to_scrape(i: int) -> tuple[str, str]:
    container_div_xpath       = f"{OUTBOUND_CONTAINER_DIV_XPATH}/div[{i+2}]"
    time_span_xpath           = f"{container_div_xpath}/div[1]/div[2]/div/span"
    price_container_div_xpath = f"{container_div_xpath}/div[2]/div[1]"
    return container_div_xpath, time_span_xpath, price_container_div_xpath

get_price_str = lambda div: re.search(r"£(\d+\.\d{2})", div.get_attribute("innerHTML")).group(1)


def get_search_url(enquiry: Enquiry) -> str:

    ## get the raw text from the link
    station_code_js_url = "https://book.splitmyfare.co.uk/static/js/59.ff0845d3.chunk.js"
    station_code_js = requests.get(station_code_js_url)

    ## verify the station_js request was successful
    if station_code_js.status_code != 200:
        raise Exception(f"Unable to create splitmyfare search url, request for any station information failed")

    ## extract the string passed to JSON.parse
    match = re.search(r"JSON\.parse\('(.*)'\)", station_code_js.text, re.DOTALL)

    ## verify the JSON.parse string was found
    if match is None:
        raise Exception("Unable to create splitmyfare search url, could not find any splitmyfare station information")

    ## extract and clean the JSON string 
    station_json_str = match.group(1)
    station_json_str = station_json_str.replace("\\", "\\\\")

    ## parse the JSON string
    station_json = json.loads(station_json_str)

    ## create a dictionary mapping alpha3 to unique code
    alpha3_to_uic = {}
    for entry in station_json:
        if 'crs' in entry and 'uic' in entry and entry['uic'] != '':
            alpha3_to_uic[entry['crs']] = entry['uic']

    ## get the unique code for the start and end stations
    from_uic = alpha3_to_uic[enquiry.start_alpha3]
    to_uic = alpha3_to_uic[enquiry.end_alpha3]

    ## verify the given stations are actually in the JSON
    if from_uic is None:
        raise Exception(f"Unable to create splitmyfare search url, splitmyfare does not have station code {enquiry.start_alpha3}")
    if to_uic is None:
        raise Exception(f"Unable to create splitmyfare search url, splitmyfare does not have station code {enquiry.end_alpha3}")
    
    ## populate url with universally required ticket information
    url = "https://book.splitmyfare.co.uk/search"                   ## base url
    url += f"?from={from_uic}&to={to_uic}"                          ## add the start and end stations
    url += f"&adults={enquiry.adults}&children={enquiry.children}"  ## add the number of adults and children
    url += f"&departureDate={enquiry.out_date}T{enquiry.out_time}"  ## add the departure date and time

    ## populate url with optional ticket information
    ## TODO: if specified, apply railcard information to url here
    if enquiry.out_time_condition == TimeCondition.ARRIVE_BEFORE:       ## if out time condition is on arrival, add to url
        url += "&departureBefore=1"
    if enquiry.journey_type == JourneyType.RETURN:                      ## if return journey, add return date and time to url
        url += f"&returnDate={enquiry.ret_date}T{enquiry.ret_time}"
        if enquiry.ret_time_condition == TimeCondition.ARRIVE_BEFORE:   ## if return time condition is on arrival, add to url
            url += "&returnBefore=1"

    return url



def get_journeys(enquiry: Enquiry) -> list[tuple[str, Journey]]:

    init_driver()
    driver.get(get_search_url(enquiry))

    ## you must be a bot... click the button to prove you're not!
    button = wait_xpath_ret(SOMETHING_WRONG_XPATH, 5)
    button.click()

    ## reapply the search, because you're not a bot!
    button = wait_xpath_ret(SEARCH_AGAIN_XPATH, 5)
    button.click()

    ## outbound journeys
    i = 0
    price_floats = []
    price_strings = []
    journeys = []
    while True:
        
        container_div_xpath, time_span_xpath, price_container_div_xpath = get_xpaths_to_scrape(i)

        try: wait_xpath_ret(container_div_xpath)    ## break if no more journeys found
        except: break

        time_span = wait_xpath_ret(time_span_xpath) ## first and last 5 characters are dept and arrival times
        depart_time_str = time_span.text[:5]
        arrive_time_str = time_span.text[-5:]

        price_str = get_price_str(wait_xpath_ret(price_container_div_xpath))
        price_strings.append(price_str)
        price_floats.append(float(price_str))

        journeys.append(Journey( start_alpha3 = enquiry.start_alpha3,
                                 end_alpha3 = enquiry.end_alpha3,
                                 journey_type = enquiry.journey_type,
                                 out_depart_time = depart_time_str,
                                 out_arrive_time = arrive_time_str, ))
        i+=1

    if not price_strings:
        print("No journeys found")
        return []

    price_strings[price_floats.index(min(price_floats))] += " <- Cheapest"
    price_strings = ["£"+s for s in price_strings]

    return list(zip(price_strings, journeys))


