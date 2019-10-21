# graphql call to retrieve all records from damage comparisons table

# first get all he records from the table
import json
import requests
import re

from bs4 import BeautifulSoup as bs
import requests
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
import requests


def getAllDamageComparisons():

    headers = {
        'Authorization': 'Bearer jAL8mDIwpm7Pqk7BUtelsgW3jIFUkO',
        "Content-Type": "application/json",

    }

    data = {
        "query": """query getDamagedCars{
  allDamageComparisonObjects{
      vin
      id
         }
    }""",
    }

    data = json.dumps(data)

    #response = requests.post("http://localhost:3000/graphql", headers=headers, data=data)
    response2 = requests.post("https://gsm-django.herokuapp.com/graphqlui", headers=headers, data=data)

    allDamagedCars = [[car["vin"], car["id"]] for car in json.loads(response2.text)["data"]["allDamageComparisonObjects"]]
    return allDamagedCars

import codecs
def updateDamageComparisons(car_info=None):
    test1 = [['RGFtYWdlQ29tcGFyaXNvblR5cGU6Mw==', ['5UXFG2C53BLX09045', 'No Issues Reported, ', 'No Issues Reported, ', 'No Issues Reported, ', 'Mileage Inconsistency, ', 'No Issues Reported, ', 'No Recalls Reported, ', '\n \n Service Facility\n \n ,\n \n \n Mississauga, ON\n \n \n \n \n ']], ['RGFtYWdlQ29tcGFyaXNvblR5cGU6NA==', ['WDCGG8HB4AF472595', 'No Issues Reported, ', 'No Issues Reported, ', 'No Issues Reported, ', 'No Issues Indicated, ', 'No Issues Reported, ', 'No Recalls Reported, ', '\n \n Quebec\n \n ,\n \n \n Motor Vehicle Dept.\n \n ,\n \n \n Sainte-Anne-des-Lacs, QC\n \n \n \n \n ']]]

    test = [['RGFtYWdlQ29tcGFyaXNvblR5cGU6MA==', ['1FTFW1EG4HFA67794', 'No Issues Reported, No Issues Reported, ', 'No Issues Reported, No Issues Reported, ', 'No Issues Reported, No Issues Reported, ', 'No Issues Indicated, No Issues Indicated, ', 'No Issues Reported, No Issues Reported, ', 'No New Recalls Reported, Recall Reported, ', '\n \n Sherlock\n \n ,\n \n \n Antitheft Marking\n \n ,\n \n \n \n sherlock.ca\n \n \n \n ']]]
    for car in car_info:
        car[0] = codecs.encode(car[0], encoding='ascii', errors='strict')
        car[0] = str(codecs.decode(car[0], encoding='base64', errors='strict'))
        car[0] = car[0].replace('b', '').replace("DamageComparisonType:", '').replace("'", "")
        print("CAR", car)


    headers = {
        'Authorization': 'Bearer jAL8mDIwpm7Pqk7BUtelsgW3jIFUkO',
        "Content-Type": "application/json",

    }

    data = {
        "query": """mutation updateDamage($car_info:[[String]]){
  updateDamageComparison(args:{carInfo:$car_info}){
      ok
      response
         }
    }""",
        "variables": {"car_info": car_info},
    }

    data = json.dumps(data)
    response = requests.post("http://localhost:3000/graphqlui", headers=headers, data=data)
    response2 = requests.post("https://gsm-django.herokuapp.com/graphqlui", headers=headers, data=data)

    print(response2.content)
    return response2


def get_carfax_infoMMC():
    chromedriver = 'C:/Users/User/Desktop/chromedriver.exe'

    #create a chrome object
    browser = webdriver.Chrome(executable_path=chromedriver)
    browser.get('https://www.carfaxonline.com/login')


    username = browser.find_element_by_css_selector("input[type='text']")
    password = browser.find_element_by_css_selector("input[type='password']")

    username.send_keys("sencoreent@gmail.com")
    password.send_keys("7102677Se")

    browser.find_element_by_id("login_button").click()
    wait = WebDriverWait(browser, 3)
    wait_for_dashboard = wait.until(EC.url_to_be("https://www.carfaxonline.com/"))
    damageComparisonList = getAllDamageComparisons()[550:650]
    # a list of lists that contain each car's id and vin
    id_list = [car[1] for car in damageComparisonList]
    # get list of vins of damaged cars
    vin_list = [car[0] for car in damageComparisonList]
    print("VIN LIST LENGTH:", len(vin_list))

    carfax_data = []  # this will store the 6 values and be returned by the function to use in api calls

    try:
        for i, vin in enumerate(vin_list):

            if type(vin) is not str or len(vin) < 17:

                continue

            wait = WebDriverWait(browser, 1.5)
            wait.until(EC.presence_of_element_located((By.ID, "vin-input")))

            vin_field = browser.find_element_by_id('vin-input')
            vin_field.send_keys(vin)  # make the url for that vin available

            get_report_button = browser.find_element_by_id('header_run_vhr_button')  # get report

            get_report_button.click()
            time.sleep(2)

            # browser.switch_to.window(browser.window_handles[1])
            # close the new tab
            browser.close()

            last_handle = browser.window_handles[0]
            browser.switch_to.window(last_handle)

            browser.get("https://www.carfaxonline.com/api/report?vin={0}".format(vin))
            carfax_html = browser.page_source  # get all html from page
            soup = bs(carfax_html)
            [s.extract() for s in soup('script')]

            carfax_html.replace('opacity', 'margin')
            carfax_info = carfax_html
            time.sleep(1)
            browser.get('https://www.carfaxonline.com/')

            updateDamageComparisons([[id_list[i], carfax_info]]) # after the loop has ended send the array to be update function

    except Exception as error:
        print(error)
        get_carfax_infoMMC()  # run the function again
        time.sleep(5)


if __name__ == '__main__':
    #getAllDamageComparisons()
    #updateDamageComparisons()
    get_carfax_infoMMC()
