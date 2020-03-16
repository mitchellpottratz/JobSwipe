import os
from flask import request, jsonify
from flask.views import View
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist

from flask_bcrypt import generate_password_hash

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
    methods = ['PUT']

    def dispatch_request(self):
        # checks if all required fields are present in the request body
        try:
            data = request.get_json()
            update_password_code = data['update_password_code']
            new_password = data['new_password']
            new_confirmed_password = data['new_confirmed_password']
        except TypeError:
            return jsonify(
                data={},
                status={
                    'code': 422,
                    'message': 'Invalid request body.'
                }
            )

        # if the new passwords do not match 
        if new_password != new_confirmed_password:
            return jsonify(
                data={},
                status={
                    'code': 422,
                    'message': 'Passwords do not match.'
                }
            )
        
        # checks if the update password code is exists for a candidate or company user
        try:
            candidate_user = CandidateUser.get(CandidateUser.update_password_code == update_password_code)

            candidate_user.password = generate_password_hash(new_password)
            candidate_user.update_password_code = None
            candidate_user.save()

            candidate_user_dict = model_to_dict(candidate_user)
            del candidate_user_dict['password']

            return jsonify(
                data=candidate_user_dict,
                status={
                    'code': 204,
                    'message': 'Successfully reset password.'
                }
            )

        except DoesNotExist:
            try:
                company_user = CompanyUser.get(CompanyUser.update_password_code == update_password_code)

                company_user.password = generate_password_hash(new_password)
                company_user.update_password_code = None
                company_user.save()

                company_user_dict = model_to_dict(company_user)
                del company_user_dict['password']                

                return jsonify(
                    data=company_user_dict,
                    status={
                        'code': 204,
                        'message': 'Successfully reset password.'
                    }
                )

            except DoesNotExist:
                return jsonify(
                    data={},
                    status={
                        'code': 404,
                        'message': 'Resource does not exist.'
                    }
                )





    





