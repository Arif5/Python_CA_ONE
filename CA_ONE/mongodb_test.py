import pymongo

client = pymongo.MongoClient("mongodb://pythonca2:reU3cS3CLAUaHHJ4126e3FG6cZ5iZ2q4cFd8vbqu87bcPmfsJinH3LeTg22HCqMQfK1A1EGGjLyJACDbgxzTQg==@pythonca2.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@pythonca2@")

db = client["tstdb"]
col = db["tst"]

employee = {
   "name": "john",
   "age": "40",
   "designation": "engineer"
}

col.insert_one(employee)

for i in col.find():
    print(i)

