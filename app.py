from flask import g
from server import Server 
from database import Database

# imports models here
from models.base import BaseModel
from models.user import User
from models.candidate_user import CandidateUser


# creates instances of the server and database
server = Server([])
database = Database([BaseModel, User, CandidateUser])


# gets the flask app object from the server so it can be used as a decorator
app = server.app

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



