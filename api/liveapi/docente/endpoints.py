
from flask_restplus import Resource
from liveapi.restplus import api as liveapi
from liveapi.unidade.serializer import unidades_field
from  liveapi.scrapper.sigaa  import docente


ns = liveapi.namespace('docente', description='Operations related to "docente"')

@ns.route('/<string:siape>')
class Docente(Resource):
    def get(self, siape):
        return docente.get_docente(siape)

@ns.route('/<string:siape>/turmas')
class Turmas(Resource):
    def get(self, siape):
        return docente.get_turmas(siape)

@ns.route('/<string:siape>/projetos')
class Projetos(Resource):
    def get(self, siape):
        return docente.get_projetos(siape)

@ns.route('/<string:siape>/producao')
class Producao(Resource):
    def get(self, siape):
        return docente.get_producao(siape)