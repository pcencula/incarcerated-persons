from selenium import webdriver
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--incognito')


headers = {"jms_number":(), "cp_case_number":(), "municipal_case_number":(), "other_case_number":(), "court_date":(),
           "orc_code":(), "charge_description":(), "bond_type":(), "bond_amount":(), "disposition":(),
           "fine":(), "comments":(), "holder":(), "timestamp":()
}

start = pd.DataFrame(headers)
start.to_csv('/home/paul/Documents/people.csv', index=False)

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

# below loop iterates through each individual on the 'view all inmates' table, visits their page,
# and scrapes their charges info from that table, then adds one to the value of "counter" at end of loop
# continues through this while loop until the value of counter is the same as the length of ip_url column
# might need to change statement to:
# while counter < 1+ len(ip_url): to get last element on list?

while counter < len(ip_url):
    url = ip_url[counter]
    driver.get(url)
    raw = pd.read_html(driver.page_source)
    indiv = raw[1]
    timestamp = pd.to_datetime("today")
    indiv.insert(0, 'jms_number', driver.current_url[-7:])
    indiv.insert(13, 'timestamp', timestamp)
    indiv.to_csv('/home/paul/Documents/people.csv', mode='a', header=False, index=False)
    # turns the dataframe into csv and appends what has been scraped in this loop to the existing file
    # also removes header and index

    counter+=1