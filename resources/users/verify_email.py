from flask import request, jsonify
from flask.views import View
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist

from models.user import User
from models.company_user import CompanyUser
from models.candidate_user import CandidateUser


# Email Verication
# verifies the email address for company and candidate users
class VerifyEmail(View):
    path = '/users/verify-email'
    view_name = 'veryify_email'
    methods = ['GET']

    def dispatch_request(self):
        return jsonify(
            data={},
            status={
                'code': 204,
                'message': 'Resource is working.'
            }
        )









