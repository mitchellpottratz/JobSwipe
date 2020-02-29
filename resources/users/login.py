from flask import request, jsonify
from flask.views import View
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
from werkzeug.utils import secure_filename
from flask_bcrypt import check_password_hash

from models.user import User
from models.company_user import CompanyUser
from models.candidate_user import CandidateUser


class Login(View):
    path = '/users/login'
    view_name = 'users_login'
    methods = ['POST']

    
    def dispatch_request(self):
        return jsonify(
            status={
                'code': 200,
                'message': 'Resource is working.'
            }
        )