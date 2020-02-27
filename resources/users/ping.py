from flask import jsonify
from flask.views import View 


# Ping route for tesing 
class Ping(View):
    path = '/users/ping'
    view_name = 'users_ping'
    methods = ['GET']

    def dispatch_request(self):
        return jsonify(
            data={},
            status={
                'code': 200,
                'message': 'Resource is working.'
            }
        )