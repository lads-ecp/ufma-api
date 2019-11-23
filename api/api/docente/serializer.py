from flask_restplus import fields
from api.restplus import api


docente_model = api.model('Blog category', {
    'siape': fields.Integer(readOnly=True, description='The unique identifier of a blog category'),
    'nome': fields.String(required=True, description='Nome do docente'),
})