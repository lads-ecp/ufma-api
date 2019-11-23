
from flask_restplus import Resource, reqparse, Api
from flask_restplus import fields
from endpoints.restplus import api as api
from flask import request
from flask import make_response     
from database.models import Subunidade
from rdf.models import Subunidade as SubunidadeRDF
from crdf_serializer import graph
from flask.json import jsonify


from flask_jwt import  jwt_required

subunidade_model = api.model('Subunidade model', {
    'codigo': fields.String(readOnly=True, description='The unique identifier of a "subunidade"'),
    'nome': fields.String(required=True, description='Nome do docente'),
})

ns = api.namespace('subunidade', description='Operations related to "subunidade"')

# repetindo codigo, refatorar
@api.representation('application/xml')
def xml(data, code, headers):
    resp = make_response(data, code)
    resp.headers.extend(headers)
    return resp

def grapho_f (l):
    g = Graph()
    for o in l:
        for s, p, o in o.g:
            g.add ((s,p,o))
    return g

@ns.route('/<string:codigo>')
@api.response(404, 'Subunidade not found.')
class SubunidadeItem(Resource):
    parser = reqparse.RequestParser()
    
    for i in ["nome","codigo" ]:
        parser.add_argument(i, type=str, required=False, help='')

    def get(self, codigo):
        if Subunidade.query.filter(Subunidade.codigo == codigo).first():
            subunidade = Subunidade.query.filter(Subunidade.codigo == codigo).one()

            subunidade_rdf = SubunidadeRDF (subunidade.codigo, subunidade.nome)

            if request.headers['accept'] == 'application/xml':
                grafo = grap_f(subunidade_rdf)
                return xml(grafo.serialize().decode(), 201, {'Content-Type':'application/xml'})
            else:
                #return json(docente.json(), 201,  {'Content-Type': 'application/json'}) # talvez nao precise isso
                return jsonify({'data': subunidade.json() })

        return {'Message': 'Subunidade with the codigo {} is not found'.format(codigo)}

    #@api.expect(subunidade_model)
    @api.response(201, 'Subunidade successfully created.')
    @jwt_required()
    def post(self, codigo):
        # todo: reinserção do mesma subunidade
        if Subunidade.query.filter(Subunidade.codigo == codigo).first():
            return {' Message': 'Subunidade with the codigo {} already exists'.format(codigo)}

        args = SubunidadeItem.parser.parse_args()
        item = Subunidade(args)
        item.save_to()
        return None, 201


@ns.route('/')
class SubunidadeCollection (Resource):
    def get(self):
        if request.headers['accept'] == 'application/xml':
            dados_rdf =  list(map(lambda subunidade: SubunidadeRDF (subunidade.codigo, subunidade.nome) , Subunidade.query.order_by(Subunidade.nome).all() )) 
            grafo = graph(dados_rdf)
            return xml(grafo.serialize().decode(), 201, {'Content-Type':'application/xml'})
        else:
            return jsonify({'data': list(map(lambda x: x.json(), Subunidade.query.order_by(Subunidade.nome).all() ))})