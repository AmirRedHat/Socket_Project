import hashlib

from database import DatabaseRouter


class BackEnd:

    @staticmethod
    def make_hash(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    # def authenticate(self, username: str, password: str) -> bool:
    #     hashed_password = self.make_hash(password)
    #     db = DatabaseRouter()
    #     user = db.read_user({"username": username, "password": hashed_password})
    #     if user:
    #         return True
    #     return False

    # def register(self, username, password, date_joined):
    #     password = self.make_hash(password)
    #     is_done = self.write_user(username, password, date_joined)
    #     return is_done

    def check_user_existence(self, username):
        all_users = self.read_user({})
        username_list = [i["username"] for i in all_users]
        if username in username_list:
            return True 
        return False

    def write_user(self, data):
        if not self.check_user_existence(data["username"]):
            db = DatabaseRouter()
            db.write_user(data)
            return "success"
        return "username is exists"

    @staticmethod
    def read_user(*args):
        db = DatabaseRouter()
        return db.read_user(*args)

    @staticmethod
    def delete_user(data):
        db = DatabaseRouter()
        db.delete_user(data)

    def save_chat(self):
        pass 

    def read_chat(self):
        pass

    def save_group_chat(self):
        pass 

    def read_group_chat(self):
        pass

