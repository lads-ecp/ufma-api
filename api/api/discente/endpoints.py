
from flask_restplus import Resource, reqparse, Api

from api.restplus import api as api
from flask.json import jsonify
from database.models import Discente
from database import db
from database.operations import save_to, delete_data
from flask import request
from flask_jwt import  jwt_required

from flask import make_response     


from rdf.models import Discente as DiscenteRDF
from crdf_serializer import graph
from rdflib import Graph

ns = api.namespace('discente', description='Operations related to "Discente"')


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


@ns.route('/<string:matricula>')
@api.response(404, 'Discente not found.')
class DiscenteItem(Resource):
    parser = reqparse.RequestParser()
    
    for i in ["nome","matricula", "nome_curso", "codigo_curso" ]:
        parser.add_argument(i, type=str, required=False, help='')

    def get(self, matricula):
        if Discente.query.filter(Discente.matricula == matricula).first():
            return jsonify(Discente.query.filter(Discente.matricula == matricula).one().json())
        return {'Message': 'Discente with the matricula {} is not found'.format(matricula)}

    #@api.expect(subunidade_model)
    @api.response(201, 'Discente successfully created.')
    @jwt_required()
    def post(self, matricula):
        if Discente.query.filter(Discente.matricula == matricula).first():
            return {' Message': 'Discente with the matricula {} already exists'.format(matricula)}

        args = DiscenteItem.parser.parse_args()
        item = Discente(args)
        print (item)
        save_to(item, db)
        return "ok", 201


get_arguments = reqparse.RequestParser()
get_arguments.add_argument('curso', type=int, required=False, help='Código do curso')
get_arguments.add_argument('nome', type=str, required=False, help='Nome ou parte do nome de um discente')


@ns.route('/')
class DiscenteCollection (Resource):

    @api.expect(get_arguments, validate=True)
    def get(self):
        cod_curso = request.args.get("curso")
        nome = request.args.get("nome")
        query = Discente.query
        print (cod_curso, nome)
        if (cod_curso):
            query = query.filter(Discente.codigo_curso == cod_curso)
        if (nome):
            query = query.filter(Discente.nome.like("%"+nome+"%") )


        if request.headers['accept'] == 'application/xml':
            dados_rdf =  list(map(lambda discente: DiscenteRDF (discente.matricula, discente.nome, discente.codigo_curso) , query.order_by(Discente.nome).all() )) 
            grafo = grapho_f(dados_rdf)
            return xml(grafo.serialize().decode(), 201, {'Content-Type':'application/xml'})
        else:
            data = list(map(lambda x: x.json(), query.order_by(Discente.nome).all() ))
            return jsonify({'data': data, 'length': len(data)})

        #return {'data': list(map(lambda x: x.json(), query.order_by(Discente.nome).all() ))}