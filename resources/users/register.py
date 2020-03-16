import os
from flask import request, jsonify
from flask.views import View
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
from werkzeug.utils import secure_filename
from flask_bcrypt import generate_password_hash

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from models.user import User
from models.company_user import CompanyUser
from models.candidate_user import CandidateUser


# Registration Route
# registers a new company user or candidate user
class Register(View):
    path = '/users/register'
    view_name = 'users_register'
    methods = ['POST']

    RELATIVE_IMAGE_UPLOAD_FOLDER = '/../../media/profile_pictures/'
    uploaded_images_name = ''


    def dispatch_request(self):
        data = request.form.to_dict()

        # checks if a candidate user already exists
        try:
            CandidateUser.get(CandidateUser.email == data['email'])

            return jsonify(
                data={},
                status={
                    'code': 409,
                    'message': 'Email already exists.'
                }
            )
        
        # if the email does exists for a candidate user
        except DoesNotExist:

            # checks if a company user already exists
            try: 
                CompanyUser.get(CompanyUser.email == data['email'])

                return jsonify(
                    data={},
                    status={
                        'code': 409,
                        'message': 'Email already exists.'
                    }
                )    

            # if the email doesnt exists for a company user
            except DoesNotExist: 

                # since company users and candidate users use different models they need to be
                # created individually
                if data['is_company_user'] == 'True':      
                    new_company_user = self.register_company_user(data)
                    new_company_user_dict = model_to_dict(new_company_user)
                    del new_company_user_dict['password']
                    response_data = new_company_user_dict
                else:
                    new_candidate_user = self.register_candidate_user(data)
                    new_candidate_user_dict = model_to_dict(new_candidate_user)
                    del new_candidate_user_dict['password']
                    response_data = new_candidate_user_dict

                # send a confirmation email to the new user
                self.send_confirmation_email(response_data)

            return jsonify(
                data=response_data,
                status={
                    'code': 201,
                    'message': 'Resource created successfully.'
                }
            )
                

    def register_company_user(self, data):
        data['password'] = generate_password_hash(data['password'])

        new_company_user = CompanyUser.create(**data)
        new_company_user.generate_email_confirmation_code()
        self.handle_profile_image_upload()
        new_company_user.image = self.uploaded_images_name
        new_company_user.save()

        return new_company_user

    
    def register_candidate_user(self, data):
        data['password'] = generate_password_hash(data['password'])

        new_candidate_user = CandidateUser.create(**data)
        new_candidate_user.generate_email_confirmation_code()
        self.handle_profile_image_upload()
        new_candidate_user.image = self.uploaded_images_name
        new_candidate_user.save()

        return new_candidate_user

 
    def handle_profile_image_upload(self):
        # gets the image from the form data if it exists
        if 'image' in request.files:
            image = request.files['image']
        else: 
            image = ''

        # uploads the users profile image
        self.uploaded_images_name = str(secure_filename(image.filename))
        image.save(
            os.path.dirname(__file__) + self.RELATIVE_IMAGE_UPLOAD_FOLDER + self.uploaded_images_name
        )


    def send_confirmation_email(self, user):
        try:

            confirmiation_email_data = {
                'personalizations': [
                    {
                        'to': [
                            { 'email': user['email'] }
                        ],
                        'subject': 'Please Confirm Your Email Address'
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
                'template_id': os.environ.get('EMAIL_CONFIRMATION_TEMPLATE_ID'),
                'dynamic_template_data': {
                    'confirmation_url': os.environ.get('DEVELOPMENT_ORIGIN') + '/api/v1/users/email_confirmation/' + 
                                        user['email_confirmation_code']
                }
            }

            send_grid_client = SendGridAPIClient(os.environ.get('SEND_GRID_MAIL_API_KEY'))
            response = send_grid_client.send(confirmiation_email_data)
            
        except Exception as e:
            print('exception occurred while sending email:', e) 



        


    





