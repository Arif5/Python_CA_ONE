from bs4 import BeautifulSoup
import requests

url = 'https://www.easemytrip.com/hotel/hotels-in-bangalore-india'
page = requests.get(url)
print(page)
#print(page.content)

soup = BeautifulSoup(page.content, 'html.parser')
#{"id": "hotelListDiv"}
lists = soup.find_all('div', class_="result-item" )

for l in lists:
    hotel_info = {}

    title = l.find('div', class_="htl_ttl").text.replace('\n', '').replace(' ', '', 1)
    address = l.find('div', class_="address").text.replace('\n', '')#.replace(' ', '')
    actual_price = l.find('div', class_="act_price").text.replace('\n', '').replace('\r', '').replace(' ', '')
    if l.find('div', class_="cross_price"):
        cross_price = l.find('div', class_="cross_price").text.replace('\n', '').replace('\r', '').replace(' ', '')
    else:
        cross_price = 'NA'
    if l.find('div', class_="prntax"):
        prn_tax = l.find('div', class_="prntax").text.replace('\n', '').replace('+', '').replace('₹', '').replace('Taxes & fees', '').replace(' ', '')
    else:
        prn_tax = 'NA'
    cancel_chrg_apply = l.find('div', class_="fr_cnc").text.replace('\n', '').replace('\r', '').replace(' ', '')
    #cancel_chrg = l.find('i', class_="far fa-check-circle").text.replace('\n', '').replace('\r', '').replace(' ', '')
    hotel_info = [title, address, actual_price, cross_price, prn_tax, cancel_chrg_apply, ]
    print(hotel_info)