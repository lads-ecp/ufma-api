from rdflib import Namespace, Literal, URIRef
from simpot import RdfsClass, BNamespace
from rdflib.namespace import DC, FOAF

VCARD = Namespace('https://www.w3.org/2006/vcard/ns#')
DBO = Namespace('http://dbpedia.org/data3/.n3#')
DC = Namespace('http://purl.org/dc/terms/#')
VIVO = Namespace("http://vivoweb.org/ontology/core#")
BIBO = Namespace("http://purl.org/ontology/bibo/")


class Docente ():

    nome = FOAF.name
    telefone = FOAF.phone
    imagem = VCARD.hasPhoto
    email = VCARD.hasEmail
    descricao = DBO.abstract
    subunidade = DC.isPartOf

    @RdfsClass(FOAF.Person, "https://sigaa.ufma.br/sigaa/public/docente/portal.jsf?siape=")
    @BNamespace('foaf', FOAF)
    @BNamespace('dc', DC)
    @BNamespace('vcard', VCARD)
    @BNamespace('dbo', DBO)
    def __init__(self, nome, telefone, imagem, email, descricao, siape, subunidade):
        self.nome = Literal(nome)
        self.id = str(siape)
        # if (telefone):
        #    self.telefone = URIRef('tel:+55.98'+telefone)
        if (imagem):
            self.imagem = URIRef(imagem)
        if (email):
            #self.email = URIRef('mailto:'+email)
            self.email = Literal('mailto:' + email)
        self.descricao = Literal(descricao)
        self.subunidade = URIRef("https://sigaa.ufma.br/sigaa/public/departamento/portal.jsf?id=" + str(subunidade))


class Subunidade ():

    nome = DC.title

    @RdfsClass(VIVO.AcademicDepartment, "https://sigaa.ufma.br/sigaa/public/departamento/portal.jsf?id=")
    @BNamespace('dc', DC)
    @BNamespace('vivo', VIVO)
    def __init__(self, codigo, nome):
        self.nome = Literal(nome)
        self.id = str(codigo)


class Discente ():

    nome = FOAF.name
    curso = FOAF.member

    @RdfsClass(FOAF.Person, "https://dados-ufma.herokuapp.com/api/v01/discente/")
    @BNamespace('dc', DC)
    @BNamespace('foaf', FOAF)
    def __init__(self, matricula, nome, curso):
        self.nome = Literal(nome)
        self.id = str(matricula)
        self.curso = URIRef("https://sigaa.ufma.br/sigaa/public/curso/portal.jsf?id=" + str(curso))


class Curso ():

    nome = DC.title

    @RdfsClass(VIVO.Course, "https://sigaa.ufma.br/sigaa/public/curso/portal.jsf?id=")
    @BNamespace('dc', DC)
    @BNamespace('vivo', VIVO)
    def __init__(self, codigo, nome):
        self.nome = Literal(nome)
        self.id = str(codigo)


class Monografia ():

    title = DC.title
    autor = DC.creator
    curso = DC.publisher
    orientador = DC.contributor

    @RdfsClass(BIBO.Thesis, "https://dados-ufma.herokuapp.com/api/v01/monografia/")
    @BNamespace('dc', DC)
    def __init__(self, codigo, title, curso, autor, orientador):
        self.title = Literal(title)
        self.id = str(codigo)
        self.curso = URIRef("https://sigaa.ufma.br/sigaa/public/curso/portal.jsf?id=" + str(curso))
        self.autor = Literal(autor)
        self.orientador = URIRef("https://sigaa.ufma.br/sigaa/public/docente/portal.jsf?siape=" + str(orientador))
