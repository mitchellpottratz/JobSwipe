import os
from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS

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
        self.blueprints = blueprints

        # configures the flask login manager
        self.login_manager = LoginManager()
        self.configure_login_manager()

        self.app.secret_key = os.environ['SECRET_KEY']

        # sets the directory to where files are uploaded
        self.app.config['UPLOAD_FOLDER'] = '/media'

        # registers all of the blueprints
        self.register_blueprints()

    # sets the origin to either development or production depending on 
    # if DEBUG is set to true
    def set_origin(self):
        if os.environ['DEBUG']:
            return os.environ['DEVELOPMENT_ORIGIN']
        else:
            return os.environ['PRODUCTON_ORIGIN']

    def configure_login_manager(self):
        self.login_manager.init_app(self.app)

    # registers all of the blueprints and configures cors for them
    def register_blueprints(self):
        for blueprint in self.blueprints:
            self.app.register_blueprint(blueprint[0], url_prefix=blueprint[1])
            CORS(blueprint[0], origins=[self.origin], supports_credentials=True)

    def start(self): 
        self.app.run(debug=self.DEBUG, port=self.PORT)
        print("Server is running on port", self.PORT)

    