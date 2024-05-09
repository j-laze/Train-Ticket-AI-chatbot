import requests
import re
import json
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import *



def get_search_url(enquiry: Enquiry):

    ## get the raw text from the link
    station_code_js_url = "https://book.splitmyfare.co.uk/static/js/57.80112f8e.chunk.js"
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
    if enquiry.journey_type == JourneyType.RETURN:                  ## if return journey, add return date and time to url
        url += f"&returnDate={enquiry.ret_date}T{enquiry.ret_time}"
        if enquiry.ret_time_condition == TimeCondition.ARRIVE_BEFORE:   ## if return time condition is on arrival, add to url
            url += "&returnBefore=1"

    return url




def OLD_get_journeys(url):

    something_wrong_xpath = "//*[@id=\"root\"]/div[2]/div/div[2]/div/div/div[2]/a/button"
    search_again_xpath = "//*[@id=\"root\"]/div/div/div/div[2]/button"
    outbound_container_div_xpath = "/html/body/div[1]/div[1]/div/div[2]/div/div[1]/div[3]"

    driver = webdriver.Chrome()

    driver.get(url)

    ## you must be a bot... click the button to prove you're not!
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, something_wrong_xpath)))
    button.click()

    ## reapply the search, because you're not a bot!
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, search_again_xpath)))
    button.click()

    ## outbound journeys
    i = 0
    while (True):
        container_div_xpath = f"{outbound_container_div_xpath}/div[{i+2}]"
        time_span_xpath = f"{container_div_xpath}/div[1]/div[2]/div/span"
        price_container_div_xpath = f"{container_div_xpath}/div[2]/div[1]"

        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, container_div_xpath)))
        except:
            break

        ## get departure and arrival times using substring of time span element text
        # NOTE: first and last 5 characters of text are departure and arrival times respectively
        time_span = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, time_span_xpath)))
        depart_time_str = time_span.text[:5]
        arrive_time_str = time_span.text[-5:]

        ## get the price from the price container div using regex on the innerHTML of the price container div
        # NOTE: uses innerHTML because the cheapest price has another div inside the price container div
        price_container_div = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, price_container_div_xpath)))
        price_str = re.search(r"£(\d+\.\d{2})", price_container_div.get_attribute("innerHTML")).group(1)

        print(f"{depart_time_str}-{arrive_time_str}, £{price_str}")
        i+=1
