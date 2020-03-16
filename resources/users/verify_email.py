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
            candidate_user = CandidateUser.get(
                CandidateUser.email_confirmation_code == email_confirmation_code
            )

            # verifies the candidate users email
            candidate_user.email_confirmed = True
            candidate_user.email_confirmation_code = None
            candidate_user.save()

            candidate_user_dict = model_to_dict(candidate_user)
            del candidate_user_dict['password']

            return jsonify(
                data=candidate_user_dict,
                status={
                    'code': 204,
                    'message': 'Email address confirmed.'
                }
            )

        # exception thrown if a candidate user with a matching email confirmation does not exists
        except DoesNotExist:

            try:
                company_user = CompanyUser.get(
                    CompanyUser.email_confirmation_code == email_confirmation_code
                )

                # verifies the company users email
                company_user.email_confirmed = True
                company_user.email_confirmation_code = None
                company_user.save()

                company_user_dict = model_to_dict(company_user)
                del company_user_dict['password']

                return jsonify(
                    data=company_user_dict,
                    status={
                        'code': 204,
                        'message': 'Email address confirmed.'
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










