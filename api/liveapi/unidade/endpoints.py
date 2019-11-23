
from flask_restplus import Resource
from liveapi.restplus import api as liveapi
from liveapi.unidade.serializer import unidades_field
from  liveapi.scrapper.sigaa  import unidade

ns = liveapi.namespace('unidade', description='Operations related to "unidade"')

import json

with open('liveapi/unidade/unidades.json') as json_file:  
    unidades = json.load(json_file)


@ns.route('/')
class Unidade (Resource):
    def get(self):
        return unidades

@ns.route('/<string:codigo>')
class Unidade (Resource):
    @liveapi.marshal_with(unidades_field)
    def get(self, codigo):
        return unidade.get_unidade(codigo)

@ns.route('/<string:codigo>/subunidade')
class Subunidades(Resource):
    def get(self, codigo):
        return unidade.get_subunidades(codigo)


@ns.route('/<string:codigo>/grupos_pesquisa')
class Grupos_Pesquisa(Resource):
    def get(self, codigo):
        return unidade.get_grupos_pesquisa(codigo)

@ns.route('/<string:codigo>/cursos_pos')
class Cursos_Pos(Resource):
    def get(self, codigo):
        return unidade.get_cursos_pos(codigo)

@ns.route('/<string:codigo>/cursos_graduacao')
class Cursos_Graduacao(Resource):
    def get(self, codigo):
        return unidade.get_cursos_graduacao(codigo)