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


# Create Update Password Code Route
# this route creates a update password code and send a email for the user to update their password
class CreateForgottenPasswordCode(View):
    path = '/users/create-forgotten-password-code'
    view_name = 'create_forgotten_password_code'
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
            self.send_forgot_password_email(candidate_user_dict)

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
                self.send_forgot_password_email(company_user_dict)

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
            update_password_code = User.generate_update_password_code()

            # while loop if broken out of if update password code does not already exist
            if not (CandidateUser.select().where(CandidateUser.update_password_code == update_password_code) and
               not CompanyUser.select().where(CompanyUser.update_password_code == update_password_code)):
                user.update_password_code = update_password_code
                user.save()
                code_exists = False


    def send_forgot_password_email(self, user):
        try:
            forgot_password_email_data = {
                'personalizations': [
                    {
                        'to': [
                            { 'email': user['email']}
                        ],
                        'subject': 'JobSwipe: Password Reset'
                    }
                ],
                'from': {
                    'email': os.environ.get('EMAIL_ADDRESS')
                },
                'content': [
                    {
                        'type': 'text/html',
                        'value': 'Hello World'
                    }
                ],
                'template_id': os.environ.get('FORGOT_PASSWORD_EMAIL_TEMPLATE_ID'),
                'dynamic_template_data': {
                    'confirmation_url': os.environ.get('DEVELOPMENT_ORIGIN') + '/some/react/url/' + 
                                        user['update_password_code']
                }
            }

            send_grid_client = SendGridAPIClient(os.environ.get('SEND_GRID_MAIL_API_KEY'))
            response = send_grid_client.send(forgot_password_email_data)
            
        except Exception as e:

            print('exception occurred while sending email:', e) 

        


        
                

        











