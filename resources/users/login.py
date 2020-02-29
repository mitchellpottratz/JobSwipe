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


class Login(View):
    path = '/users/login'
    view_name = 'users_login'
    methods = ['POST']

    
    def dispatch_request(self):
        data = request.get_json()
        print('data:', data)
        print('type of:', type(data))

        if data['is_candidate_user'] == 'True':
            try:
                candidate_user = CandidateUser.get(CandidateUser.email == data['email'])

                if check_password_hash(candidate_user.password, data['password']):
                    login_user(candidate_user)

                    candidate_user_dict = model_to_dict(candidate_user)
                    del candidate_user_dict['password']

                    return jsonify(
                        data=candidate_user_dict,
                        status={
                            'code': 200,
                            'message': 'Successfully logged in.'
                        }
                    )

            except DoesNotExist:
                return jsonify(
                    data={},
                    status={
                        'code': 404,
                        'message': 'Email or password is incorrect.'
                    }
                )

        

            

        return jsonify(
            status={
                'code': 200,
                'message': 'Resource is working.'
            }
        )