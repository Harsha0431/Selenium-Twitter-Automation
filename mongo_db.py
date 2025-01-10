from pymongo import MongoClient as MC
from bson import ObjectId
import uuid
import datetime
from dotenv import load_dotenv
import os


load_dotenv()

uri = os.getenv("MONGO_URI")


class MongoClient:

    def __init__(self):
        self.client = MC(uri)
        self.db = self.client["twitter_trends_automation_db"]
        self.collection = self.db["trends"]
        print("Database login successful")

    def insert_data(self, data, ip_addr):
        unique_id = str(uuid.uuid4())
        # Get current date and time
        end_time = datetime.datetime.now()
        trend_data = {
            "_id": unique_id,
            "end_time": end_time,
            "ip_address": ip_addr,
            "topics": data
        }
        result = self.collection.insert_one(trend_data)
        trend_data["_id"] = str(result.inserted_id)
        print("Data inserted to database")
        self.client.close()
        return trend_data
