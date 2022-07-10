from typing import Tuple
from pymongo import MongoClient


class DatabaseRouter:

    user_column = ["id", "username", "password", "group_list", "date_joined"]
    client = MongoClient()
    db = client["ChatDB"]

    def write_user(self, data: dict) -> Tuple[bool, str]:
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

    def delete_user(self, data: dict, many: bool = False):
        collection = self.db["user"]
        if many:
            collection.delete_many(data)
        else:
            collection.delete_one(data)

    def check_username_existence(self, username: str):
        # return True if username is exists and return False if not exists
        all_users = self.read_user({}, many=True)
        if [i for i in all_users if i["username"] == username]:
            return True 
        return False

    def write_user_groups(self, data: dict):
        group_name = data["group_name"]
        user_name = data["username"]
        user = self.read_user({"username": user_name})
        if group_name not in user["group_list"]:
            user["group_list"].append(group_name)
        self.update_user({"username": user_name}, {"group_list": user["group_list"]})

    def read_user_groups(self, data: dict):
        user_name = data["username"]
        user = self.read_user({"username": user_name})
        return user["group_list"]


if __name__ == "__main__":
    app = DatabaseRouter()
    # print(list(app.db["user"].find({})))
    print(app.read_user({}))
    # app.delete_user({}, many=True)