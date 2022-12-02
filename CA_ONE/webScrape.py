from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.easemytrip.com/hotels/hotels-in-bangalore'
#https://www.easemytrip.com/hotels/hotels-in-bangalore/
page = requests.get(url)
print(page)
#print(page.content)

soup = BeautifulSoup(page.content, 'html.parser')
#{"id": "hotelListDiv"}
lists = soup.find_all('div', class_="result-item" )


title = []
address = []
hotel_type = []
actual_price = []
cross_price = []
prn_tax = []
cancel_chrg_apply = []

for l in lists:
    #hotel_info = {}

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
    #cancel_chrg = l.find('i', class_="far fa-check-circle").text.replace('\n', '').replace('\r', '').replace(' ', '')
    #hotel_info = [title, address, hotel_type, actual_price, cross_price, prn_tax, cancel_chrg_apply]

    #print(hotel_info)

data = pd.DataFrame({'title':title, 'address':address, 'hotel_type':hotel_type, 'actual_price':actual_price,
                         'cross_price':cross_price,'prn_tax':prn_tax, 'cancel_chrg_apply':cancel_chrg_apply})
pd.set_option('display.max_columns', None)
print(data)

