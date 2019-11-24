from ufma_scrapper.subunidade import get_subunidades, get_docentes
from ufma_scrapper.docente import get_docente

from ufma_scrapper.curso import get_cursos, get_discentes_ativos, get_monografias


from database.models import Subunidade, Discente, Curso, Monografia, Docente

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from database import db
from database.operations import save_to


print ("loading data ...")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = False



db.init_app(app)
app.app_context().push()
db.create_all()




cursos = get_cursos()
subunidades = get_subunidades()

# cursos e discentes
for curso in cursos[1:10]:
    c = Curso (curso)
    save_to(c, db)
    discentes = get_discentes_ativos(c.codigo)["data"]
    for disc in discentes:
        #print (disc)
        d = Discente (disc)
        save_to(d, db)
        #print (d)

# monografias
for ano in range(2017,2018):
    cod_monografia = 1
    for curso in cursos[100:102]:
        #print (curso)
        monografias = get_monografias (curso["codigo"], str(ano))["data"]
        for monografia in monografias:
            monografia["codigo_curso"] = curso["codigo"]
            monografia["ano"] = str(ano)
            monografia["codigo"] = curso["codigo"]+"_"+str(ano)+str(cod_monografia)
            #print (monografia)
            m = Monografia (monografia)
            cod_monografia = cod_monografia + 1
            save_to(m, db)

## subunidades e docentes
for sub in subunidades[1:4]:
    s = Subunidade (sub)
    save_to(s, db)
    docentes = get_docentes(sub["codigo"])
    #print (sub["codigo"])
    for docente in docentes[1:5]:
        docente_detail = get_docente(docente["siape"])
        docente_detail["codigo_subunidade"] = docente["codigo_subunidade"]
        print (docente_detail)
        doc = Docente(docente_detail)
        save_to(doc, db)


    


