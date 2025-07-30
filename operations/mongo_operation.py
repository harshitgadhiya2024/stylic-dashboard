from pymongo import MongoClient
from datetime import datetime

from utils.constant import constant_dict

class mongoOperation():

    def __init__(self):
        self.database="stylic"
        self.client = MongoClient(constant_dict.get("mongo_url"))

    def get_specific_db(self, database_name):
        db = self.client[database_name]
        return db

    # connection of data insertion on mongodb
    def insert_data_from_coll(self, coll_name, mapping_dict):
        try:
            db = self.client[self.database]
            coll = db[coll_name]
            coll.insert_one(mapping_dict)
            return "add_data"

        except Exception as e:
            print(f"{datetime.utcnow()}: Error when data inserting on mongo: {e}")

    # get all data from mongodb collection
    def get_all_data_from_coll(self, coll_name):
        try:
            db = self.client[self.database]
            coll = db[coll_name]
            res = list(coll.find({}))
            return res

        except Exception as e:
            print(f"{datetime.utcnow()}: Error when fetch all data in collection: {e}")

    # get only specific data from collection
    def get_spec_data_from_coll(self, coll_name, condition_dict):
        try:
            db = self.client[self.database]
            coll = db[coll_name]
            res = list(coll.find(condition_dict))
            return res

        except Exception as e:
            print(f"{datetime.utcnow()}: Error when fetch specific data from collection: {e}")

    # delete data from collection with specific condition dict
    def delete_data_from_coll(self, coll_name, di):
        try:
            db = self.client[self.database]
            coll = db[coll_name]
            res = coll.delete_one(di)
            return res

        except Exception as e:
            print(f"{datetime.utcnow()}: Error when delete data from collection: {e}")

    # update data from collection with specific dict and specific data
    def update_mongo_data(self, coll_name, condition_dict, update_mapping_dict):
        try:
            db = self.client[self.database]
            coll = db[coll_name]
            coll.update_one(condition_dict, {"$set": update_mapping_dict})
            return "updated"

        except Exception as e:
            print(f"{datetime.utcnow()}: Error when update data from collection: {e}")

