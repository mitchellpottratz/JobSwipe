from flask import request, jsonify
from flask.views import View
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist

from models.user import User
from models.company_user import CompanyUser
from models.candidate_user import CandidateUser


# Create Update Password Code Route
# this route creates a update password code and send a email for the user to update their password
class CreateUpdatePasswordCode(View):
    path = '/users/create-update-password-code'
    view_name = 'create_update_password_code'
    methods = ['POST']


    def dispatch_request(self):
        # checks if the email exists in the request body
        try: 
            data = request.get_json()
            email = data['email']
        except TypeError:
            return jsonify(
                data={},
                status={
                    'code': 422,
                    'message': 'Invalid request body.'
                }
            )

        # checks if the email exists for a candidate user
        try:
            candidate_user = CandidateUser.get(CandidateUser.email == email)
            self.create_update_password_code(candidate_user)

            candidate_user_dict = model_to_dict(candidate_user)
            del candidate_user_dict['password']
            # del candidate_user_dict['update_password_code']

            return jsonify(
                data=candidate_user_dict,
                status={
                    'code': 204,
                    'message': 'Update password confirmation sent to email address.'
                }
            )

        except DoesNotExist:

            # checks if a email exists for a company user
            try:
                company_user = CompanyUser.get(CompanyUser.email == email)
                self.create_update_password_code(company_user)

                company_user_dict = model_to_dict(company_user)
                del company_user_dict['password']
                # del company_user_dict['update_password_code']

                return jsonify(
                    data=candidate_user_dict,
                    status={
                        'code': 204,
                        'message': 'Update password confirmation sent to email address.'
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


    # creates a update password code for candidate and compnay users
    def create_update_password_code(self, user):
        code_exists = True
        while code_exists:
            print('generating code')
            update_password_code = User.generate_update_password_code()

            # while loop if broken out of if update password code does not already exist
            if not (CandidateUser.select().where(CandidateUser.update_password_code == update_password_code) and
               not CompanyUser.select().where(CompanyUser.update_password_code == update_password_code)):
                print('code does not exist')
                code_exists = False
            else:
                print('code exists')
                

        











