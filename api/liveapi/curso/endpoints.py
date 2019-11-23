
from flask_restplus import Resource
from liveapi.restplus import api as liveapi
from liveapi.unidade.serializer import unidades_field
from  liveapi.scrapper.sigaa  import curso


ns = liveapi.namespace('curso', description='Operations related to "curso"')


@ns.route('/')
class Curso(Resource):
    def get(self):
        return curso.get_cursos()



@ns.route('/<string:codigo>/monografias/<string:ano>')
## Endpoint - Monografias
# 16822859
class Monografias(Resource):
    def get(self, codigo, ano):
        return curso.get_monografias(codigo, ano)

## Endpoint - Discentes Ativos do Curso
# 16822859
@ns.route('/<string:codigo>/discentes')
class Discentes(Resource):
    def get(self, codigo):
        return curso.get_discentes_ativos(codigo)

@ns.route('/<string:codigo>/turmas/<string:ano>/<string:periodo>')
## Endpoint - Monografias
# 16822859
class Turmas (Resource):
    def get(self, codigo, ano, periodo):
        return curso.get_turmas(codigo, ano, periodo)

