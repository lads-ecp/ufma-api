
from flask_restplus import Resource, reqparse, Api
from flask.json import jsonify
from api.restplus import api as api

from database.models import Monografia
from database import db
from database.operations import save_to, delete_data
from flask import request
from flask import make_response 

from flask_jwt import  jwt_required

from rdf.models import Monografia as MonografiaRDF
from crdf_serializer import graph
from rdflib import Graph


ns = api.namespace('monografia', description='Operations related to "Monografias"')

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
class MonografiaItem(Resource):
    parser = reqparse.RequestParser()
    
    for i in ["codigo", "discente","orientador", "titulo", "codigo_curso" , "ano", "siape_orientador"]:
        parser.add_argument(i, type=str, required=False, help='')

    def get(self, codigo):
        if Monografia.query.filter(Monografia.codigo == codigo).first():
            return Monografia.query.filter(Monografia.codigo == codigo).one().json()
        return {'Message': 'Monografia with the codigo {} is not found'.format(cdigo)}

    #@api.expect(subunidade_model)
    @api.response(201, 'Monografia successfully created.')
    @jwt_required()
    def post(self, codigo):
        if Monografia.query.filter(Monografia.codigo == codigo).first():
            return jsonify({' Message': 'Monografia with the codigo {} already exists'.format(codigo)})

        args = MonografiaItem.parser.parse_args()
        item = Monografia(args)
        print (item)
        save_to(item, db)
        return "ok", 201


get_arguments = reqparse.RequestParser()
get_arguments.add_argument('curso', type=int, required=False, help='Código do curso')
get_arguments.add_argument('discente', type=str, required=False, help='Nome ou parte do nome de um discente')
get_arguments.add_argument('titulo', type=str, required=False, help='Titulo da monografia')
get_arguments.add_argument('siape_orientador', type=str, required=False, help='Siape do orientador')


@ns.route('/')
class MonografiaCollection (Resource):

    @api.expect(get_arguments, validate=True)
    def get(self):
        cod_curso = request.args.get("curso")
        discente = request.args.get("discente")
        titulo = request.args.get("titulo")
        siape_orientador = request.args.get("siape_orientador")
        query = Monografia.query
        print (cod_curso, discente)
        if (cod_curso):
            query = query.filter(Monografia.codigo_curso == cod_curso)
        if (discente):
            query = query.filter(Monografia.discente.like("%"+discente+"%") )
        if (titulo):
            query = query.filter(Monografia.titulo.like("%"+titulo+"%") )
        if (siape_orientador):
            query = query.filter(Monografia.siape_orientador.like("%"+siape_orientador+"%") )

        if request.headers['accept'] == 'application/xml':
            dados_rdf =  list(map(lambda mono: MonografiaRDF (mono.codigo, mono.titulo, mono.codigo_curso, mono.discente, mono.siape_orientador) , query.order_by(Monografia.titulo).all() ))
            grafo = grapho_f(dados_rdf)
            return xml(grafo.serialize().decode(), 201, {'Content-Type':'application/xml'})
        else:
            data = list(map(lambda x: x.json(), query.order_by(Monografia.titulo).all() ))
            return jsonify({'data': data, 'length':len(data) })