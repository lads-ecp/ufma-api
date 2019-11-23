from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp


from database import db



class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=False, nullable=False)
    password = db.Column(db.String(30), unique=False, nullable=False)


    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id



def createTable():
    users = User.query.all()
    print (users)
    username_table = {u.username: u for u in users}
    userid_table = {u.id: u for u in users}
    return username_table, userid_table


def authenticate(username, password):
    username_table, userid_table = createTable()
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    username_table, userid_table = createTable()
    user_id = payload['identity']
    return userid_table.get(user_id, None)


