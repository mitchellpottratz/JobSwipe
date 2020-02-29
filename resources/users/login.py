from flask import request, jsonify
from flask.views import View
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
from werkzeug.utils import secure_filename
from flask_bcrypt import check_password_hash
from flask_login import login_user

from models.user import User
from models.company_user import CompanyUser
from models.candidate_user import CandidateUser


# Login Route
# this route logs in either a canidate user or company user
class Login(View):
    path = '/users/login'
    view_name = 'users_login'
    methods = ['POST']

    
    def dispatch_request(self):
        data = request.get_json()
    
        # if the user loggin in is a candidate user
        if data['is_candidate_user'] == 'True':
            try:
                candidate_user = CandidateUser.get(CandidateUser.email == data['email'])

                # logs in the candidate user and returns the response
                response = self.login(candidate_user, data['password'])
                return response

            except DoesNotExist:
                return Login.incorrect_email_or_password_json_response()

        # if the user logging in is a company user
        else:
            try:
                company_user = CompanyUser.get(CompanyUser.email == data['email'])

                # logs in the candidate user and returns the response
                response = self.login(company_user, data['password'])
                return response
                
            except DoesNotExist:
                return Login.incorrect_email_or_password_json_response()

    # logs in either a candidate user or company user
    def login(self, user, password_to_check):

        # if the password matches
        if check_password_hash(user.password, password_to_check):
            login_user(user)

            user_dict = model_to_dict(user)
            del user_dict['password']    

            return jsonify(
                data=user_dict,
                status={
                    'code': 200,
                    'message': 'Successfully logged in.'
                }
            )

        # otherwise if the password does not match
        else:
            return Login.incorrect_email_or_password_json_response()


    # returns a jsonify response saying the provided email or password is incorrect
    @staticmethod
    def incorrect_email_or_password_json_response():
        return jsonify(
            data={},
            status={
                'code': 404,
                'message': 'Email or password is incorrect.'
            }
        )
