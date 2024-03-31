import pymongo
import pandas as pd

df = pd.read_excel("data.xlsx")

client = pymongo.MongoClient("mongodb+srv://yashloriya0206:Yash0206@cluster0.u6icnjq.mongodb.net/mern_admin?retryWrites=true&w=majority")
db = client["productData"] 
collection = db["mobiles"]

data_dict = df.to_dict(orient="records")
collection.insert_many(data_dict)

print("Inserted Document Successfully.")
