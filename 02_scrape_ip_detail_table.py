from selenium import webdriver
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--incognito')

ip = pd.read_csv("/home/paul/Documents/ip.csv")
# assigns 'view all inmates' table (ip.csv) to ip
ip.columns = ['jms_number', 'last_name', 'first_name', 'admit_date', 'proj_release_date', 'holder']
# names columns for ip object for later usage
url_pattern = "http://apps.hcso.org/InmateDetail.aspx?ID="
# creates base url that jms_number can be concatenated to the end of to create url for each person

ip.insert(0, 'ip_url', url_pattern + ip['jms_number'].map(str))
# inserts a column at the far left that is url pattern + person's jms number

driver = webdriver.Chrome(options=options)
# assigns webdriver.Chrome() to object driver for easier reference later
ip_url = ip.iloc[0:, 0]
# assigns object ip_url to first row, first column of ip (which is the url to lookup

counter = 0
# gives counter object a value of 0
url = ip_url[counter]
# gives url object the value of whatever is in the [current counter value]th row of the ip_url object
driver.get(url)
# accesses the url for current person


# url = 'http://apps.hcso.org/InmateDetail.aspx?ID=1729726'
r = requests.post(url)
soup = bs(r.text, 'lxml')

# driver = webdriver.Chrome()
# driver.get(url)

ip_detail = []

jms_number = soup.find('input', {'id': 'lbJms'})['value']
control_number = soup.find('input', {'id': 'lbControl'})['value']
housing_location = soup.find('input', {'id': 'lbHouse'})['value']
dob = soup.find('input', {'id': 'lbDob'})['value']
sex = soup.find('input', {'id': 'lbSex'})['value']
race = soup.find('input', {'id': 'lbRace'})['value']
admitted_date = soup.find('input', {'id': 'lbAdmit'})['value']
timestamp = pd.to_datetime("today")

ip_elements = {
    'jms_number': jms_number[13:],
    # pulls jms number from page starting with 13th character
    'control_number': control_number[17:],
    # pulls control number from page starting with 17th character
    'housing_location': housing_location[19:],
    'dob': dob[16:],
    'sex': sex[6:],
    'race': race[7:],
    'admitted_date': admitted_date[16:],
    'timestamp': timestamp
}

ip_detail.append(ip_elements)

df = pd.DataFrame(ip_detail)
df.to_csv('/home/paul/Documents/ip_detail.csv', index=False)


while counter < len(ip_url):
    url = ip_url[counter]
    driver.get(url)
    r = requests.post(url)
    soup = bs(r.text, 'lxml')

    ip_detail2 = []

    jms_number = soup.find('input', {'id': 'lbJms'})['value']
    control_number = soup.find('input', {'id': 'lbControl'})['value']
    housing_location = soup.find('input', {'id': 'lbHouse'})['value']
    dob = soup.find('input', {'id': 'lbDob'})['value']
    sex = soup.find('input', {'id': 'lbSex'})['value']
    race = soup.find('input', {'id': 'lbRace'})['value']
    admitted_date = soup.find('input', {'id': 'lbAdmit'})['value']
    timestamp = pd.to_datetime("today")

    ip_elements2 = {
        'jms_number': jms_number[13:],
        # pulls jms number from page starting with 13th character
        'control_number': control_number[17:],
        # pulls control number from page starting with 17th character
        'housing_location': housing_location[19:],
        'dob': dob[16:],
        'sex': sex[6:],
        'race': race[7:],
        'admitted_date': admitted_date[16:],
        'timestamp': timestamp
    }

    ip_detail2.append(ip_elements2)

    df2 = pd.DataFrame(ip_detail2)

    df2.to_csv('/home/paul/Documents/ip_detail.csv', mode='a', header=False, index=False)
    # turns the dataframe into csv and appends what has been scraped in this loop to the existing file
    # also removes header and index
    #time.sleep(5)
    # goes to sleep for stated seconds before running through the loop again--can be removed or reduced
    counter += 1
