# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from datetime import datetime

from database import db

from rdflib import Namespace


class Docente(db.Model):
    siape = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), unique=False, nullable=False)
    departamento = db.Column(db.String(50), unique=False, nullable=True)
    codigo_subunidade = db.Column(db.String(50), unique=False, nullable=True)
    descricao = db.Column(db.Text, unique=False, nullable=True)
    formacao = db.Column(db.Text, unique=False, nullable=True)
    areas_interesse = db.Column(db.Text, unique=False, nullable=True)
    lattes = db.Column(db.String(50), unique=False, nullable=True)
    email = db.Column(db.String(50), unique=False, nullable=True)
    telefone = db.Column(db.String(30), unique=False, nullable=True)
    urlimg = db.Column(db.String(50), unique=False, nullable=True)
    
    def __init__ (self, dict):
        self.__dict__.update(dict)

    def json(self):
        dic = dict (filter (lambda v: v[0] != "_sa_instance_state", self.__dict__.items()))
        return dic
    
    def save_to(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_(self):
        db.session.delete(self)
        db.session.commit()

class Subunidade(db.Model):
    codigo = db.Column(db.String(15), primary_key=True)
    nome = db.Column(db.String(30), unique=False, nullable=False)
    
    def __init__ (self, dict):
        self.__dict__.update(dict)

    def json(self):
        dic = dict (filter (lambda v: v[0] != "_sa_instance_state", self.__dict__.items()))
        return dic
    
    def save_to(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_(self):
        db.session.delete(self)
        db.session.commit()



class Discente (db.Model):
    matricula = db.Column(db.String(15), primary_key=True)
    nome = db.Column(db.String(30), unique=False, nullable=False)
    codigo_curso = db.Column(db.String(30), unique=False, nullable=True)
    nome_curso = db.Column(db.String(30), unique=False, nullable=True)

    def __init__ (self, dict):
        self.__dict__.update(dict)

    def json(self):
        dic = dict (filter (lambda v: v[0] != "_sa_instance_state", self.__dict__.items()))
        return dic

  
vcard = Namespace('https://www.w3.org/2006/vcard/ns#') #Trazendo uma nova ontologia
n = Namespace("http://linkedscience.org/teach/ns#")

class Curso (db.Model):
    codigo = db.Column(db.String(15), primary_key=True)
    nome = db.Column(db.String(30), unique=False, nullable=False)
    modalidade = db.Column(db.String(30), unique=False, nullable=False)
    municipio = db.Column(db.String(30), unique=False, nullable=False)
    coordenador = db.Column(db.String(30), unique=False, nullable=False)

    def __init__ (self, dict):
        self.__dict__.update(dict)

    def json(self):
        dic = dict (filter (lambda v: v[0] != "_sa_instance_state", self.__dict__.items()))
        return dic


class Monografia (db.Model):
    codigo = db.Column(db.String(15), primary_key=True)
    codigo_curso = db.Column(db.String(30), unique=False, nullable=True)
    titulo = db.Column(db.String(30), unique=False, nullable=True)
    ano = db.Column(db.String(10), unique=False, nullable=True)
    discente = db.Column(db.String(30), unique=False, nullable=True)
    orientador = db.Column(db.String(30), unique=False, nullable=True)
    siape_orientador = db.Column(db.String(30), unique=False, nullable=True)


    def __init__ (self, dict):
        self.__dict__.update(dict)

    def json(self):
        dic = dict (filter (lambda v: v[0] != "_sa_instance_state", self.__dict__.items()))
        return dic