import datetime
from peewee import *
from .base import BaseModel
from flask_login import UserMixin


''' 
This is the base user model which defines fields for both the CandidateUser
and CompanyUser models which inherit from this class
'''

class User(BaseModel, UserMixin):
    image = CharField(max_length=500)
    first_name = CharField(max_length=55)
    last_name = CharField(max_length=55)
    email = CharField(max_length=155)
    password = CharField(max_length=155)
    email_confirmation_code = CharField(max_length=25)
    email_confirmed = BooleanField(default=False)
    active = BooleanField(default=False)
    soft_delete = BooleanField(default=False)


