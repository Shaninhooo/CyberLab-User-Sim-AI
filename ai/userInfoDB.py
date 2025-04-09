from pymongo import MongoClient
from createPersonas import generatePersona
from bson import ObjectId
import json
import re

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
users_collection = db["users"]

def addUserToDB():
    personaDataJSON = generatePersona()

    match  = re.search(r"```json\s*(\{.*\})", personaDataJSON, re.DOTALL)

    if match:
        json_data = match.group(1)
        
        # Convert the extracted JSON string to a Python dictionary
        try:
            persona_dict = json.loads(json_data)

            # Step 4: Insert the persona data into MongoDB
            inserted_id = users_collection.insert_one(persona_dict).inserted_id

            # Step 5: Print the inserted ID (optional)
            print(f"Inserted document with ID: {inserted_id}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print("No valid JSON found.")


addUserToDB()