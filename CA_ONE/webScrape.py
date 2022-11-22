from bs4 import BeautifulSoup
import requests

url = 'https://www.easemytrip.com/hotel/region/bangalore-india'
page = requests.get(url)
print(page)

soup = BeautifulSoup(page.content, 'html.parser')
#{"id": "hotelListDiv"}
lists = soup.find_all('div', class_="result-item" )

for l in lists:
    print(1)
    title = l.find('div', class_="htl_ttl")
    print(title)