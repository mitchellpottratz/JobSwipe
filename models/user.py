from peewee import *
from .base import BaseModel
from flask_login import UserMixin
import random


''' 
This is the base user model which defines fields for both the CandidateUser
and CompanyUser models which inherit from this class
'''

class User(BaseModel, UserMixin):
    image = CharField(max_length=500, null=True)
    first_name = CharField(max_length=55)
    last_name = CharField(max_length=55)
    email = CharField(max_length=155)
    password = CharField(max_length=155)
    email_confirmation_code = CharField(max_length=25, null=True)
    email_confirmed = BooleanField(default=False)
    update_password_code = CharField(max_length=25, null=True)
    active = BooleanField(default=True)
    soft_delete = BooleanField(default=False)


    # generate a random 15 digit code required for the user to confirm their email address
    def generate_email_confirmation_code(self):
        confirmation_code_list = []

        for i in range(1, 15):
            confirmation_code_list.append(str(random.randint(1, 9)))

        self.email_confirmation_code = ''.join(confirmation_code_list)


    # generate a random 15 digit code which is used to change a users password
    @staticmethod
    def generate_update_password_code():
        password_code_list = []
        
        for i in range(1, 15):
            password_code_list.append(str(random.randint(1, 9)))

        return ''.join(password_code_list)





