import os
from flask import request, jsonify
from flask.views import View
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
from werkzeug.utils import secure_filename

from models.user import User


class Register(View):
    path = '/users/register'
    view_name = 'users_register'
    IMAGE_UPLOAD_FOLDER = '/../../media/profile_pictures/'
    methods = ['POST']


    def dispatch_request(self):
        data = request.form

        self.handle_image_upload()

        return data

    # handles uploading the users profile image
    def handle_image_upload(self):
        image = self.get_image()

        # uploads the users profile image
        image_name = secure_filename(image.filename)
        image.save(os.path.dirname(__file__) + self.IMAGE_UPLOAD_FOLDER + image_name)

    # gets the image from the form data
    def get_image(self):
        if 'image' in request.files:
            image = request.files['image']
        else: 
            image = ''
        return image


    





