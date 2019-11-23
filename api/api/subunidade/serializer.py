from flask_restplus import fields
from api.restplus import api


subunidade_model = api.model('Subunidade model', {
    'codigo': fields.String(readOnly=True, description='The unique identifier of a "subunidade"'),
    'nome': fields.String(required=True, description='Nome do docente'),
})

