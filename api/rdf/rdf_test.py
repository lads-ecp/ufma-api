import requests, json
from crdf_serializer import graph
import models as modelo

request = requests.get('http://dados-ufma.herokuapp.com/liveapi/v01/docente/407686').text
json = json.loads(request)
docente = modelo.Docente(json['nome'],json['telefone'],json['urlimg'], json['email'], json['descricao'])

grafo = graph([docente])


saida = grafo.serialize(format='xml')
rdf = open('rdf_test.xml', 'r+b')
rdf.write(saida)
rdf.close()


