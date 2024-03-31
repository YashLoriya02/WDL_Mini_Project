import pymongo
import pandas as pd

df = pd.read_excel("data.xlsx")

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["productData"] 
collection = db["mobiles"]

data_dict = df.to_dict(orient="records")
collection.insert_many(data_dict)

print("Inserted Document Successfully.")