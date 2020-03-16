from peewee import *
from .base import BaseModel
from flask_login import UserMixin
import random

from models.candidate_user import CandidateUser
from models.company_user import CompanyUser


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
    def generate_update_password_code(self):
        password_code_list = []
        
        code_exists = True
        while code_exists:
            for i in range(1, 15):
                password_code_list.append(str(random.randint(1, 9)))
            
            update_password_code = ''.join(password_code_list)
    
            # if the update password code generated does not already exist for a user
            if not (
                CandidateUser.get(CandidateUser.update_password_code == update_password_code
                )) or not (
                    CompanyUser.get(CompanyUser.update_password_code == update_password_code)
                ):
                code_exists= False

            self.update_password_code = ''.join(password_code_list)





