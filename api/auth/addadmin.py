
from database.operations import save_to
from database import db
from auth import User


def addusers():
    authusers = [
        {"id": 1, "username": 'admin', "password": ''}
    ]
    users = []

    for user in authusers:
        users.append(User(user["id"], user["username"], user["password"]))

    for user in users:
        print(user)
        save_to(user, db)
