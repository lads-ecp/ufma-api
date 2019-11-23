
from flask_restplus import Resource
from liveapi.restplus import api as liveapi
from liveapi.unidade.serializer import unidades_field
from  liveapi.scrapper.sigaa  import subunidade

ns = liveapi.namespace('subunidade', description='Operations related to "subunidade"')

@ns.route('/')
class SubUnidade (Resource):
    def get(self, ):
        return subunidade.get_subunidades()


@ns.route('/<string:codigo>')
class SubUnidade (Resource):
    def get(self, codigo):
        return subunidade.get_subunidade(codigo)

@ns.route('/<string:codigo>/disciplina')
class Disciplinas(Resource):
    def get(self, codigo):
        return subunidade.get_disciplinas(codigo)

@ns.route('/<string:codigo>/docente')
class Docentes(Resource):
    def get(self, codigo):
        return subunidade.get_docentes(codigo)

'''

@ns.route('/<string:codigo>/administrativo')
class Administrativo(Resource):
    def get(self, codigo):
        return subunidade.get_administrativo(codigo)

@ns.route('/<string:codigo>/extensao')
class Extensao(Resource):
    def get(self, codigo):
        return subunidade.get_extensoes(codigo)

@ns.route('/<string:codigo>/pesquisa')
class Pesquisa(Resource):
    def get(self, codigo):
        return subunidade.get_pesquisas(codigo)

@ns.route('/<string:codigo>/monitoria')
class Monitorias(Resource):
    def get(self, codigo):
        return subunidade.get_monitorias(codigo)

@ns.route('/<string:codigo>/documento')
class Documentos(Resource):
    def get(self, codigo):
        return subunidade.get_documentos(codigo)

'''