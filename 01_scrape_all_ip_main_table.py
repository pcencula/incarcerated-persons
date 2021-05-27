from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--headless')
# options.add_argument('--ignore-certificate-errors')
options.add_argument("--incognito")
driver = webdriver.Chrome(options = options)
url = 'http://apps.hcso.org/inmates.aspx'

# go to url
driver.get(url)

# click the button called "View All Inmates"
button = driver.find_element_by_xpath('//*[@id="btnViewall"]')
button.click()

# create list from current page
ip_dfs = pd.read_html(driver.page_source)

# pull main table list from current page
ip_df = ip_dfs[1]

# drop first column
ip_df = ip_df.iloc[: , 1:]

# turn main table list into csv file, remove index and save to Documents folder
ip_df.to_csv('/home/paul/Documents/ip'+'.csv', index = False)
