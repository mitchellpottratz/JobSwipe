from peewee import *
from .user import User

'''
This model is for users that are searching for jobs
'''

class CandidateUser(User):
    location = CharField(max_length=255)
    headline = CharField(max_length=100)
    bio = CharField(max_length=500)
    phone_number = CharField(max_length=12)




