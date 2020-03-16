import os
from flask import request, jsonify
from flask.views import View
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from models.user import User
from models.company_user import CompanyUser
from models.candidate_user import CandidateUser


# Reset Forgotten Password Route
# this route is where users are able to create a new password with the update password code
# that was sent to their email address
class ResetForgottenPassword(View):
    path = '/users/reset-forgotten-password'
    view_name = 'reset_forgotten_password'
    methods = ['POST']

    def dispatch_request(self):
        return jsonify(
            data={},
            status={
                'code': 200,
                'message': 'Resource is working'
            }
        )





