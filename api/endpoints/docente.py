
import re
from flask.json import jsonify
from flask_restplus import Resource, reqparse, Api
from flask import request
from flask import make_response 
from flask_jwt import  jwt_required
from flask_restplus import fields

from endpoints.restplus import api as api

from database.models import Docente as docenteModelDB


from rdf.models import Docente as docenteModelRDF
from crdf_serializer import graph
from rdflib import Graph

ns = api.namespace('docente', description='Operations related to "docente"')

#testando funcao mais eficiente

def grapho_f (l):
    g = Graph()
    for o in l:
        for s, p, o in o.g:
            g.add ((s,p,o))
    return g


docente_model = api.model('Blog category', {
    'siape': fields.Integer(readOnly=True, description='The unique identifier of a blog category'),
    'nome': fields.String(required=True, description='Nome do docente'),
})

@api.representation('application/xml')
def xml(data, code, headers):
    resp = make_response(data, code)
    resp.headers.extend(headers)
    return resp


@ns.route('/<int:siape>')
@api.response(404, 'Docente not found.')
class DocenteItem(Resource):
    parser = reqparse.RequestParser()
    
    for i in ["nome","departamento", "codigo_subunidade", "descricao","formacao","areas_interesse","lattes","email","telefone", "urlimg" ]:
        parser.add_argument(i, type=str, required=False, help='')


    def get(self, siape):
        
        if docenteModelDB.query.filter(docenteModelDB.siape == siape).first():
            docente = docenteModelDB.query.filter(docenteModelDB.siape==siape).one()
 
            docenteRDF = docenteModelRDF (docente.nome, docente.telefone, docente.urlimg, docente.email, docente.descricao, docente.siape, docente.codigo_subunidade)

            if request.headers['accept'] == 'application/xml':
                grafo = graph(docenteRDF)
                return xml(grafo.serialize().decode(), 201, {'Content-Type':'application/xml'})
            else:
                #return json(docente.json(), 201,  {'Content-Type': 'application/json'}) # talvez nao precise isso
                return jsonify({'data': docente.json() })


        return {'Message': 'Curso with the codigo {} is not found'.format(siape)}


    #@api.expect(docente_model)
    @api.response(201, 'Docente successfully created.')
    @jwt_required()
    def post(self, siape):
        
        item = docenteModelDB.query.filter(docenteModelDB.siape == siape).first()
        if item:
           return {' Message': 'Docente with the siape {} already exists'.format(siape)}
        
        args = DocenteItem.parser.parse_args()
        args["siape"] = siape
        item = docenteModelDB(args)
        #print (item, args)
        item.save_to()
        return None, 201


get_arguments = reqparse.RequestParser()
get_arguments.add_argument('subunidade', type=int, required=False, help='Código da subunidade')
get_arguments.add_argument('nome', type=str, required=False, help='Nome ou parte do nome de um docente')

@ns.route('/')
class DocentesCollection (Resource):

 
    @api.expect(get_arguments, validate=True)
    def get(self):
        cod_subunidade = request.args.get("subunidade")
        nome = request.args.get("nome")
        query = docenteModelDB.query
        if (cod_subunidade):
            query = query.filter(docenteModelDB.codigo_subunidade == cod_subunidade)
        if (nome):
            query = query.filter(docenteModelDB.nome.like("%"+nome+"%") )

        if request.headers['accept'] == 'application/xml':
            dados_rdf =  list(map(lambda docente: docenteModelRDF (docente.nome, docente.telefone, docente.urlimg, docente.email, docente.descricao, docente.siape, docente.codigo_subunidade) , query.order_by(docenteModelDB.nome).all() )) 
            grafo = grapho_f(dados_rdf)
            return xml(grafo.serialize().decode(), 201, {'Content-Type':'application/xml'})
        else:
            data = list(map(lambda x: x.json(), query.order_by(docenteModelDB.nome).all() ))
            return jsonify({'data': data, 'length': len(data)})