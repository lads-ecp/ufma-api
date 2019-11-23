
from flask_restplus import Resource, reqparse, Api
from flask_jwt import  jwt_required

from flask.json import jsonify

from endpoints.restplus import api as api
from flask import request
from flask import make_response 

from database.models import Curso
from database import db
from database.operations import save_to, delete_data


from rdf.models import Curso as CursoRDF
from crdf_serializer import graph
from rdflib import Graph

ns = api.namespace('curso', description='Operations related to "curso"')


def grapho_f (l):
    g = Graph()
    for o in l:
        for s, p, o in o.g:
            g.add ((s,p,o))
    return g

@api.representation('application/xml')
def xml(data, code, headers):
    resp = make_response(data, code)
    resp.headers.extend(headers)
    return resp

@ns.route('/<string:codigo>')
@api.response(404, 'Subunidade not found.')
class CursoItem(Resource):
    parser = reqparse.RequestParser()
    
    for i in ["nome","codigo", "municipio", "modalidade", "coordenador" ]:
        parser.add_argument(i, type=str, required=False, help='')
    
    def get(self, codigo):
        if Curso.query.filter(Curso.codigo == codigo).first():
            curso = Curso.query.filter(Curso.codigo == codigo).one()
            cursordf = CursoRDF (curso.codigo, curso.nome)
            if request.headers['accept'] == 'application/xml':
                return xml(cursordf.g.serialize().decode(), 201, {'Content-Type': 'application/xml'})
            else:
                return jsonify(curso.json())

        return {'Message': 'Curso with the codigo {} is not found'.format(codigo)}

    #@api.expect(subunidade_model)
    @api.response(201, 'Curso successfully created.')
    @jwt_required()
    def post(self, codigo):
        if Curso.query.filter(Curso.codigo == codigo).first():
            return {' Message': 'Curso with the codigo {} already exists'.format(codigo)}

        args = CursoItem.parser.parse_args()
        item = Curso(args)
        save_to(item, db)
        return "ok", 201


get_arguments = reqparse.RequestParser()
get_arguments.add_argument('nome', type=str, required=False, help='Nome ou parte do nome de um curso')
get_arguments.add_argument('municipio', type=str, required=False, help='Nome ou parte do nome de um município')

@ns.route('/')
class CursoCollection (Resource):

    @api.expect(get_arguments, validate=True)
    def get(self):
        nome = request.args.get("nome")
        municipio = request.args.get("municipio")
        query = Curso.query
        if (nome):
            query = query.filter(Curso.nome.like("%"+nome+"%") )
        
        if (municipio):
            query = query.filter(Curso.municipio.like("%"+municipio+"%") )


        if request.headers['accept'] == 'application/xml':
            dados_rdf =  list(map(lambda curso: CursoRDF (curso.codigo, curso.nome) , Curso.query.order_by(Curso.nome).all() )) 
            grafo = graph(dados_rdf)
            return xml(grafo.serialize().decode(), 201, {'Content-Type':'application/xml'})
        else:
            data = list(map(lambda x: x.json(), query.order_by(Curso.nome).all() ))
            return jsonify({'data': data, 'length': len(data)})