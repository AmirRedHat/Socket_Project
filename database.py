from typing import Tuple
from pymongo import MongoClient


class DatabaseRouter:

    user_column = ["username", "password", "date_joined"]
    client = MongoClient()
    db = client["ChatDB"]

    def write_user(self, data: dict) -> Tuple[bool, str]:
        for key in data.keys():
            if key not in self.user_column:
                return False, "keys are invalid"

        collection = self.db["user"]
        collection.insert_one(data)
        return True, "saved"

    def read_user(self, data: dict, many: bool = True):
        collection = self.db["user"]
        if many:
            document = collection.find(data)
        else:
            document = collection.find_one(data)

        return list(document)

    def update_user(self, filter_data: dict, new_data: dict):
        collection = self.db["user"]
        collection.update_one(filter_data, new_data)

    def delete_user(self, data: dict):
        collection = self.db["user"]
        collection.delete_one(data)
