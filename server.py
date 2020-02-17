import os
from flask import Flask

# allows flask to access enviroment variables
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env') 
load_dotenv(dotenv_path)


class Server:

    def __init__(self, blueprints):
        self.app = Flask(__name__)
        self.DEBUG = os.environ['DEBUG']
        self.PORT = os.environ['PORT']
        self.origin = self.set_origin()    
        self.app.secret_key = os.environ['SECRET_KEY']
        self.blueprints = blueprints

        # sets the directory to where file are uploaded
        self.app.config['UPLOAD_FOLDER'] = '/media'

    # sets the origin to either development or production depending on 
    # if DEBUG is set to true
    def set_origin(self):
        if os.environ['DEBUG']:
            return os.environ['DEVELOPMENT_ORIGIN']
        else:
            return os.environ['PRODUCTON_ORIGIN']

    def start(self): 
        self.app.run(debug=self.DEBUG, port=self.PORT)
        print("Server is running on port", self.PORT)

    