import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



from utils import Journey
from utils import Enquiry




def get_journeys(url):

    reject_cookies_button_id = "onetrust-reject-all-handler"
    journey_list_xpath = "//*[@id=\"grid-jp-results\"]/div/div/div[1]/div/div[1]/div/div/section/ul"

    driver = webdriver.Chrome()
    driver.get(url)

    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, reject_cookies_button_id)))
    button.click()

    time.sleep(3)

    journey_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, journey_list_xpath)))
    journey_items = journey_list.find_elements(By.XPATH, "./li")

    print()
    for i, item in enumerate(journey_items):
        depart_time_str = re.search(r"Departs\n(\d{2}:\d{2})", item.text).group(1)
        arrive_time_str = re.search(r"Arrives\n(\d{2}:\d{2})", item.text).group(1)
        price_str = re.search(r"£(\d+\.\d{2})", item.text).group(1)
        print(f"Item {i}")
        print(f"Depart: {depart_time_str}")
        print(f"Arrive: {arrive_time_str}")
        print(f"Price: £{price_str}")
        print()

    time.sleep(500)



url = "https://www.nationalrail.co.uk/journey-planner/?type=single&origin=NRW&destination=LST&leavingType=departing&leavingDate=090524&leavingHour=07&leavingMin=45&adults=1&extraTime=0#O"

get_journeys(url)
