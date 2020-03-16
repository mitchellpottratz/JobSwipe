from flask import g
from flask_login import current_user
from peewee import DoesNotExist

from server import Server 
from database import Database

# imports models here
from models.base import BaseModel
from models.user import User
from models.candidate_user import CandidateUser
from models.company_user import CompanyUser

# resource imports
from resources.users import *


# creates instances of the server and database
server = Server([Ping, Register, Login, VerifyEmail, CreateForgottenPasswordCode, ResetForgottenPassword])
database = Database([BaseModel, User, CandidateUser, CompanyUser])


# gets the app and login_manager object from the server so it can be used as a decorator
app = server.app
login_manager = server.login_manager

# required by flask_login for loading users
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get(User.id == user_id)
    except DoesNotExist:
        return None

# established connection to the database before every request
@app.before_request
def before_request():
    g.db = database.DATABASE
    g.db.connect()

# closes the database and returnt the response for every request
@app.after_request
def after_request(response):
    g.db.close()
    return response


if __name__ == '__main__':
    database.initialize_tables()
    server.start()  



