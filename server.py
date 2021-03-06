import os
from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS

# allows flask to access enviroment variables
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env') 
load_dotenv(dotenv_path)


class Server:

    def __init__(self, resources):
        self.app = Flask(__name__)
        self.DEBUG = os.environ['DEBUG']
        self.PORT = os.environ['PORT']
        self.origin = self.set_origin()    
        self.resources = resources

        self.app.secret_key = os.environ['SECRET_KEY']

        self.setup_cors()

        # configures the flask login manager
        self.login_manager = LoginManager()
        self.configure_login_manager()

        # sets the directory to where files are uploaded
        self.app.config['UPLOAD_FOLDER'] = '/media'

        # registers all of the resources
        self.register_resources()

    # sets the origin to either development or production depending on 
    # if DEBUG is set to true
    def set_origin(self):
        if os.environ['DEBUG']:
            return os.environ['DEVELOPMENT_ORIGIN']
        else:
            return os.environ['PRODUCTON_ORIGIN']

    def setup_cors(self):
        CORS(self.app, resources={r"/*": {"origins": "*"}})

    def configure_login_manager(self):
        self.login_manager.init_app(self.app)

    def register_resources(self):
        for resource in self.resources:
            self.app.add_url_rule('/api/v1' + resource.path, view_func=resource.as_view(resource.view_name))

    def start(self): 
        print("Server is running on port", self.PORT)
        self.app.run(debug=self.DEBUG, port=self.PORT)
        

    