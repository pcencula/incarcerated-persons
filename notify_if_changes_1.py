import pandas as pd
import requests
import time
import smtplib
from email.message import EmailMessage
import hashlib
from urllib.request import urlopen
from selenium import webdriver
from bs4 import BeautifulSoup as bs

options = webdriver.ChromeOptions()
options.add_argument('--headless')
# options.add_argument('--ignore-certificate-errors')
options.add_argument("--incognito")
driver = webdriver.Chrome(options= options)
url = 'http://apps.hcso.org/inmates.aspx'

# go to url
driver.get(url)

# raw = pd.read_html(driver.current_url)
# test1=pd.DataFrame(raw)


# print (test1)
# click the button called "View All Inmates"
button = driver.find_element_by_xpath('//*[@id="btnViewall"]')
button.click()
#
#
r = requests.get(driver.current_url)
soup = bs(r.text, 'html.parser')
test = soup.find_all('table')[1]

df = pd.read_html(str(test))

print(df)
#
#
# print(soup)

# response = urlopen(url).read()
# currentHash = hashlib.sha224(response).hexdigest()
#
# while True:
#
#     try:
#
#         response = urlopen(url).read()
#         currentHash = hashlib.sha224(response).hexdigest()
#         time.sleep(240)
#         response = urlopen(url).read()
#         newHash = hashlib.sha224(response).hexdigest()
#
#         if newHash == currentHash:
#             continue
#
#         else:
#
#             #here you would run the python script to pull and etl
#
#     except:
#         print('Something fundamental must have changed in the markup for ' + str(url) +
#               'visit site and check against code in 01_ script.'