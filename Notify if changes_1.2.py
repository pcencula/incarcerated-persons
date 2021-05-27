from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
from pandas.util import hash_pandas_object

options = webdriver.ChromeOptions()
options.add_argument('--headless')
# options.add_argument('--ignore-certificate-errors')
options.add_argument("--incognito")
driver = webdriver.Chrome(options = options)
url = 'http://apps.hcso.org/inmates.aspx'

while True:
    # go to url
    driver.get(url)

    # click the button called "View All Inmates"
    button = driver.find_element_by_xpath('//*[@id="btnViewall"]')
    button.click()

    # create list from current page
    ip_dfs = pd.read_html(driver.page_source)

    # pull main table list from current page
    ip_df = ip_dfs[1]
    current = hash_pandas_object(ip_df).sum()

    time.sleep(15)

    driver.get(url)

    # click the button called "View All Inmates"
    button = driver.find_element_by_xpath('//*[@id="btnViewall"]')
    button.click()

    new_ip_dfs = pd.read_html(driver.page_source)

    new_ip_df = new_ip_dfs[1]
    new = hash_pandas_object(new_ip_df).sum()


    if current == new:
        continue
    else:
        print("site is updated")