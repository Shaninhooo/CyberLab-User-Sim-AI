from pymongo import MongoClient
from bson import ObjectId
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
users_collection = db["users"]

def getAllUsers():
    data = list(users_collection.find({}))
    # Convert ObjectId to string for JSON serialization
    for item in data:
        item["_id"] = str(item["_id"])

    data_string = json.dumps(data)

    return data_string
