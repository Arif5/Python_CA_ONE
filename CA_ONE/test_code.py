import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#with closing(Chrome()) as driver:
 #   driver.get("https://www.easemytrip.com/hotels/hotels-in-bangalore")
 #   driver.execute_script('return document.body.scrollHeight')
 #   button = driver.find_elements_by_id('divEndloader')
 #   button.click()
    # wait for the page to load
 #   element = WebDriverWait(driver, 10).until(
 #      EC.invisibility_of_element_located((By.ID, "deviceShowAllLink"))
 #   )
    # store it to string variable
 #   page_source = driver.page_source

options = Options()
b = webdriver.Chrome(options=options)
url = 'https://www.easemytrip.com/hotels/hotels-in-bangalore'
b.get(url)
last_height = b.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to the bottom.
    b.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load the page.
    time.sleep(2)
    # Calculate new scroll height and compare with last scroll height.
    new_height = b.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break
    last_height = new_height

soup = BeautifulSoup(b.page_source, 'html.parser')
lists = soup.find_all('div', class_="result-item" )

title = []
address = []
hotel_type = []
actual_price = []
cross_price = []
prn_tax = []
cancel_chrg_apply = []

for l in lists:
    title.append(l.find('div', class_="htl_ttl").text.replace('\n', '').replace(' ', '', 1))
    address.append(l.find('div', class_="address").text.replace('\n', ''))
    hotel_type.append(l.find('div', class_="type-hotel").text.replace('\n', ''))
    actual_price.append(l.find('div', class_="act_price").text.replace('\n', '').replace('\r', '').replace(' ', ''))
    if l.find('div', class_="cross_price"):
        cross_price.append(l.find('div', class_="cross_price").text.replace('\n', '').replace('\r', '').replace(' ', ''))
    else:
        cross_price.append('NA')
    if l.find('div', class_="prntax"):
        prn_tax.append(l.find('div', class_="prntax").text.replace('\n', '').replace('+', '').replace('₹', '').replace('Taxes & fees', '').replace(' ', ''))
    else:
        prn_tax.append('NA')
    if l.find('div', class_="fr_cnc"):
        cancel_chrg_apply.append(l.find('div', class_="fr_cnc").text.replace('\n', '').replace('\r', '').replace(' ', ''))
    else:
        cancel_chrg_apply.append('NA')


data = pd.DataFrame({'title':title, 'address':address, 'hotel_type':hotel_type, 'actual_price':actual_price,
                     'cross_price':cross_price,'prn_tax':prn_tax, 'cancel_chrg_apply':cancel_chrg_apply})
pd.set_option('display.max_columns', None)
print(data)