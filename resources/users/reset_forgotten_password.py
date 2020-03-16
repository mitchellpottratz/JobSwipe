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
        # checks if all required fields are present in the request body
        try:
            data = request.get_json()
            update_password_code = data['update_password_code']
            password = data['password']
            confirmed_password = data['confirmed_password']
        except TypeError:
            return jsonify(
                data={},
                status={
                    'code': 422,
                    'message': 'Invalid request body.'
                }
            )
        
        # try:
        #     candidate_user = CandidateUser.get(CandidateUser.update_password_code == update_password_code)

        # except Does:


    





