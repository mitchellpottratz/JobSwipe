import os
from flask import request, jsonify
from flask.views import View
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
from werkzeug.utils import secure_filename
from flask_bcrypt import generate_password_hash

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
    uploaded_images_path = ''

    def dispatch_request(self):
        data = request.form

        try:
            user = User.get(User.email == data['email'])

            return jsonify(
                data={},
                status={
                    'code': 409,
                    'message': 'Email already exists.'
                }
            )

        # if a user with the email does not already exist
        except DoesNotExist:

            # if they are registering as a company user
            if data['is_company_user']:      
                self.register_company_user(data)
            

    def register_company_user(self, data):
        data['password'] = generate_password_hash(data['password'])

        new_company_user = CompanyUser.create(**data)
        new_company_user.generate_email_confirmation_code()
        new_company_user.save()

        self.


    def handle_profile_image_upload(self):
        # gets the image from the form data if it exists
        if 'image' in request.files:
            self.uploaded_images_path = request.files['image']
        else: 
            self.uploaded_images_path = ''

        # uploads the users profile image
        image_name = secure_filename(self.uploaded_images_path.filename)
        self.uploaded_images_path.save(os.path.dirname(__file__) + self.RELATIVE_IMAGE_UPLOAD_FOLDER + image_name)

        


    





