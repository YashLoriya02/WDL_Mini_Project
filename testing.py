import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["productData"]
collection = db["mobiles"]

pipeline = [
    {
        "$set": {
            "Price": {
                "$toInt": {
                    "$trim": {
                        "input": {
                            "$replaceAll": {
                                "input": "$Price",
                                "find": "[^\d]",
                                "replacement": ""
                            }
                        }
                    }
                }
            }
        }
    }
]

result = collection.update_many({}, pipeline)

print("Number of documents updated:", result.modified_count)
