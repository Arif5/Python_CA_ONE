#Git repository link -
#importing required libraries
import time
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pymongo
from pandas.io import json
import urllib.parse

#Setting up selinium chrome driver
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

#scraping the data using beautiful soup
soup = BeautifulSoup(b.page_source, 'html.parser')
lists = soup.find_all('div', class_="result-item" )

title = []
address = []
hotel_type = []
actual_price = []
cross_price = []
prn_tax = []
cancel_chrg_apply = []
offer_code = []
top_deal = []
reviews = []
text_reviews = []
star_rating = []

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
    if l.find('div', class_="offer-sec"):
        offer_code.append(l.find('div', class_="offer-sec").text.replace('\n', '').replace('\r', '').replace(' ', ''))
    else:
        offer_code.append('NA')
    if l.find('div', class_="top_deal"):
        top_deal.append(l.find('div', class_="top_deal").text.replace('\n', '').replace('\r', '').replace(' ', ''))
    else:
        top_deal.append('NA')
    if l.find('div', class_="Review-Section-count"):
        reviews.append(l.find('div', class_="Review-Section-count").text.replace('\n', '').replace('\r', '').replace(' ', ''))
    else:
        reviews.append('NA')
    if l.find('div', class_="ReviewSection-scoreText"):
        text_reviews.append(l.find('div', class_="ReviewSection-scoreText").text.replace('\n', '').replace('\r', '').replace(' ', ''))
    else:
        text_reviews.append('NA')
    if l.find('div', class_="review-bg-g"):
        star_rating.append(l.find('div', class_="review-bg-g").text.replace('\n', '').replace('\r', '').replace(' ', ''))
    else:
        star_rating.append('NA')

#creating the dataframe from the lists
data = pd.DataFrame({'title': title, 'address': address, 'hotel_type': hotel_type, 'actual_price': actual_price,
                     'cross_price': cross_price, 'prn_tax': prn_tax, 'cancel_chrg_apply': cancel_chrg_apply,
                     'offer_code': offer_code, 'top_deal': top_deal, 'reviews': reviews, 'text_reviews': text_reviews,
                     'star_rating': star_rating})
pd.set_option('display.max_columns', None)

#applying transformations
data[['offer_code', 'offer']] = data['offer_code'].str.split("and", expand=True)
data['offer_code'] = data['offer_code'].str.replace('UseCode:', '')
data['offer'] = data['offer'].str.replace('OFFonthisHotel', '')
data['offer'] = data['offer'].str.replace('GetINR', '')
data['prn_tax'] = data['prn_tax'].str.replace('NA', '0.0')
data['reviews'] = data['reviews'].str.replace('NA', '0')
data['reviews'] = data['reviews'].str.replace('reviews', '')
data['offer'] = data['offer'].replace(np.nan, '0.0')
data['price_inc_tax'] = data['actual_price'].astype(float) + data['prn_tax'].astype(float)
data['final_effective_price'] = data['price_inc_tax'].astype(float) - data['offer'].astype(float)
data['date'] = pd.to_datetime('today').strftime("%Y-%m-%d")

#printing the dataframe
print(data)

#inserting the data into mongodb
my_client = pymongo.MongoClient("mongodb+srv://arif584:" + urllib.parse.quote("Mancity@123") + "@webscrapepy.hwzhmpg.mongodb.net/?retryWrites=true&w=majority")
my_db = my_client["banglr_hotels"]
my_col = my_db["hotels_data"]
records = json.loads(data.T.to_json()).values()
my_db.my_col.insert_many(data.to_dict('records'))



