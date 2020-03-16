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
    path = '/users/verify-email/<email_confirmation_code>'
    view_name = 'veryify_email'
    methods = ['GET']

    def dispatch_request(self, email_confirmation_code):
        try:    
            candidate_user = CandidateUser.select().where(
                CandidateUser.email_confirmation_code == email_confirmation_code
            ).first()

            print('code exists for candidate user')

        # exception thrown if a candidate user with a matching email confirmation does not exists
        except DoesNotExist:


            try:
                company_user = CompanyUser.select().where(
                    CompanyUser.email_confirmation_code == email_confirmation_code
                ).first()

                print('code exists for company user')

            except DoesNotExist:
                return jsonify(
                    data={},
                    status={
                        'code': 404,
                        'message': 'Resource does not exist.'
                    }
                )










