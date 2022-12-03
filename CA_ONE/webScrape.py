from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
from pandas.io import json

url = 'https://www.easemytrip.com/hotels/hotels-in-bangalore'
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
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

my_client = pymongo.MongoClient("mongodb://pythonca2:reU3cS3CLAUaHHJ4126e3FG6cZ5iZ2q4cFd8vbqu87bcPmfsJinH3LeTg22HCqMQfK1A1EGGjLyJACDbgxzTQg==@pythonca2.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@pythonca2@")

my_db = my_client["hotel_test"]
my_col = my_db["test_data"]
records = json.loads(data.T.to_json()).values()
my_db.my_col.insert_many(data.to_dict('records'))

for i in my_col.find():
    print(i)

