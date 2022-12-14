import pymongo
import urllib.parse

client = pymongo.MongoClient("mongodb+srv://arif584:" + urllib.parse.quote("Mancity@123") + "@webscrapepy.hwzhmpg.mongodb.net/?retryWrites=true&w=majority")

db = client["hotel_test"]
col = db["my_col"]


for i in col.find():
    print(i)

