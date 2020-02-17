import datetime
from peewee import *
from flask_login import UserMixin


class User(UserMixin, Model):
    pass

