from flask_restplus import fields
from liveapi.restplus import api




unidades_field = api.model('Unidade' ,{
    'nome': fields.String,
    'diretor': fields.String,
    'telefone': fields.String,
    'end_alt': fields.String
})

