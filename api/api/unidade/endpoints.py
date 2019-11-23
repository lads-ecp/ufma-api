
from flask_restplus import Resource
from liveapi.restplus import api as liveapi
from flask_jwt import  jwt_required
from flask.json import jsonify

ns = liveapi.namespace('unidade', description='Operations related to "unidades"')


@ns.route('/')
class Unidades (Resource):
    def get(self):
        return "{'status':'ok'}"
