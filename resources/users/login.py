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

                # logs in the candidate user
                response = self.login(candidate_user, data['password'])
                return response

            except DoesNotExist:
                return jsonify(
                    data={},
                    status={
                        'code': 404,
                        'message': 'Email or password is incorrect.'
                    }
                )
        

    # logs in either a candidate user or company user
    def login(self, user, password_to_check):
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