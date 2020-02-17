import datetime
from peewee import *

DATABASE = SqliteDatabase('foodsite.sqlite')

'''
All other models inherit from this model. The base model establishes the 
connection to the database and define the last updated and timestamp fields
which are present in every field
'''

class BaseModel(Model):
    last_updated = DateTimeField(default=datetime.datetime.now)
    timestamp = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = DATABASE
