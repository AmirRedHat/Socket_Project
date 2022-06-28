import hashlib

from flask import Flask

from database import DatabaseRouter


class BackEnd:

    @staticmethod
    def make_hash(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, username: str, password: str) -> bool:
        hashed_password = self.make_hash(password)
        db = DatabaseRouter()
        user = db.read_user({"username": username, "password": hashed_password})
        if user:
            return True
        return False

    def register(self, username, password, date_joined):
        password = self.make_hash(password)
        db = DatabaseRouter()
        is_done = db.write_user({"username": username, "password": password, "date_joined": date_joined})
        return is_done

