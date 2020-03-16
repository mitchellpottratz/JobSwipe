from flask import request, jsonify
from flask.views import View
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist

from models.company_user import CompanyUser
from models.candidate_user import CandidateUser


# Create Update Password Code Route
# this route creates a update password code and send a email for the user to update their password
class CreateUpdatePasswordCode(View):
    path = '/users/create-update-password-code'
    view_name = 'create_update_password_code'
    methods = ['POST']

    def dispatch_request(self):
        return jsonify(
            data={},
            status={
                'code': 200,
                'message': 'Resource is working.'
            }
        )






