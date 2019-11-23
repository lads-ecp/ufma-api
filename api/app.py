from flask import Flask, Blueprint, render_template
from flask_cors import CORS
from flask_jwt import JWT
from auth import authenticate, identity
from database import db

import os


#api
from api.restplus import api as api
from api.docente.endpoints import ns as docente_namespace
from api.subunidade.endpoints import ns as subunidade_namespace
from api.curso.endpoints import ns as curso_namespace
from api.discente.endpoints import ns as discente_namespace
from api.monografia.endpoints import ns as monografia_namespace

import settings


def configure_app(flask_app):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    CORS(flask_app)






blueprint = Blueprint('api', __name__, url_prefix='/api/v01')
api.init_app(blueprint)
api.add_namespace(docente_namespace)
api.add_namespace(subunidade_namespace)
api.add_namespace(curso_namespace)
api.add_namespace(discente_namespace)
api.add_namespace(monografia_namespace)

app = Flask(__name__)
configure_app(app)


app.register_blueprint(blueprint)
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)


# Endpoint Home
@app.route('/')
def index():
    return render_template('index.html')


db.init_app(app)
app.app_context().push()
db.create_all()
# app.add_url_rule('/favicon.ico',redirect_to=url_for('static', filename='images/ufmafavicon.ico'))

# descomentar apenas para criar novo usuario admin
# addusers () 

if __name__ == '__main__':
    if os.environ.get('PORT') is not None:
        app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT'))
    else:
        app.run(debug=True, host='0.0.0.0') 
