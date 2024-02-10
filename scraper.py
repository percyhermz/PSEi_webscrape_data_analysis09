# import libraries
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pdurl
import csv

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Define the URL
url = "https://www.pse.com.ph/indices-composition/"

# load the web page
# waits until an HTML element with id tag of "indices_composition" appears
driver.get(url)
WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.ID, "indices_composition")))

#switch driver to an inline html that contains indices_composition
driver.switch_to.frame("indices_composition")


#collect data that are within the id of contents
contents = driver.find_element(By.ID, 'index-body')

# Get all the company code/symbols and their outstanding shares
stocks = contents.find_elements(By.CLASS_NAME, "index-symbol")
shares = contents.find_elements(By.CLASS_NAME, "text-shares")



#collect symbol and outstanding shares for each company into a list
symbols = []
outstanding_shares = []
for stock, shares_indiv in zip(stocks, shares):

    #Extract the symbol and outstanding shares per company
    symbol = stock.find_element(By.TAG_NAME,"a").get_attribute('text')
    outstanding_shares_per_co = shares_indiv.get_attribute('innerHTML')

    #append the symbol and outstanding shares to their list
    symbols.append(symbol)
    outstanding_shares.append(outstanding_shares_per_co)

data_rows = []
fields = ["company", "date", "open", "high","low","close", "average", "volume", "value", "out_shares", "sector", "sub_sector"]
#Open each link in the list then scrape the data per company and put them in data_rows list
#Each row represents one company and one day of stock price data
for s, o_s in zip(symbols, outstanding_shares):
    s_url = "https://frames.pse.com.ph/security/" + str(s).lower()
    driver.get(s_url)
    WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.ID, "data")))
    sector = driver.find_element(By.XPATH, "//div[@class='col-8 px-0']/div[1]")
    sub_sector = driver.find_element(By.XPATH, "//div[@class='col-8 px-0']/div[2]")
    table = driver.find_element(By.ID, "data")
    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME,"tr")
    sec_data = sector.get_attribute("innerHTML").replace("<b>Sector</b>:", "").strip()
    sub_sec_data = sub_sector.get_attribute("innerHTML").replace("<b>Sub-Sector</b>:", "").strip()
    for row in rows:
        comp_data = []
        comp_data.append(s)
        
        data = row.find_elements(By.TAG_NAME, "td")

        for d in data:
            comp_data.append(d.get_attribute("innerHTML"))

        comp_data.append(o_s)
        comp_data.append(sec_data)
        comp_data.append(sub_sec_data)
        data_rows.append(comp_data)
    
    

    
#Create a CSV file from the scraped data from PSE
with open("psei_data_v2.csv", "w") as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(data_rows)
    

driver.close()







