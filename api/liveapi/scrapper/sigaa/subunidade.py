from bs4 import BeautifulSoup as BS
import requests


def get_subunidades():

    link = 'https://sigaa.ufma.br/sigaa/public/docente/busca_docentes.jsf?aba=p-academico'
    subunidades = []

    try:
        page_text = requests.get(link).text
        page = BS(page_text, 'lxml')

        select = page.find(
            'select', {"id":"form:departamento"})
        options = select.find_all('option')
        for option in options[1:]:
            subunidades.append ({"nome": option.text, "codigo": option['value']})
            

    except Exception as e:
        print('erro ao recuperar a subunidade: ', e)

    
    return subunidades

get_subunidades()

# https://sigaa.ufma.br/sigaa/public/departamento/portal.jsf?id=1396&lc=pt_BR
def get_subunidade(codigo):
    link = 'https://sigaa.ufma.br/sigaa/public/departamento/portal.jsf?id='+codigo+'&lc=pt_BR'
    subunidade = {}

    try:
        page_text = requests.get(link).text
        page = BS(page_text, 'lxml')

        subunidade['nome'] = page.find(
            'span', class_='portal-title-1').text.strip()
        info = page.find(
            'div', class_='module variacao-module-02 orgaos-vinculados').find_all('div')
        subunidade['descricao'] = info[1].text.strip()
        info = page.find(
            'div', class_='module variacao-module-02 orgaos-vinculados').find_all('li')
        next_ = info[0].find_all_next(string=True)
        subunidade['chefia'] = next_[1].strip()
        subunidade['telefone'] = next_[5].strip()
        subunidade['endereco_alt'] = next_[9].strip()
    except Exception as e:
        print('erro ao recuperar a subunidade: ', e)

    return subunidade

# https://sigaa.ufma.br/sigaa/public/departamento/professores.jsf?id=1396&lc=pt_BR
def get_docentes(codigo):
    link = 'https://sigaa.ufma.br/sigaa/public/departamento/professores.jsf?id='+codigo
    docentes = []
    try:
        page_text = requests.get(link).text
        page = BS(page_text, 'lxml')
        tables = page.find_all('table', class_="table_lt")
        for tb in tables:
            docente = {}
            rows = tb.find_all('tr')
            cols = rows[1].find_all('td')
            href = cols[0].find("a").get('href')
            siape = href[39:46]
            docente['siape'] = siape
            docente['nome'] = cols[0].get_text().strip()
            docente["codigo_subunidade"] = codigo
            docentes.append(docente)
    except:
        print('erro ao recuperar os docentes!')
    return docentes

# https://sigaa.ufma.br/sigaa/public/departamento/administrativo.jsf?id=1396&lc=pt_BR
def get_administrativo(codigo):
    link = 'https://sigaa.ufma.br/sigaa/public/departamento/administrativo.jsf?id='+codigo
    administrativo = {}

    try:
        page_text = requests.get(link).text
        page = BS(page_text, 'lxml')
        administrativo['data'] = page.find('p', class_='vazio')
    except Exception as e:
        print('erro ao recuperar os administradores: ', e)

    return administrativo


# https://sigaa.ufma.br/sigaa/public/departamento/componentes.jsf?id=1396&lc=pt_BR
def get_disciplinas(codigo):
    link = 'https://sigaa.ufma.br/sigaa/public/departamento/componentes.jsf?id=' + codigo
    disciplinas = {}
    data = []

    try:
        page_text = requests.get(link).text
        page = BS(page_text, 'lxml')
        tables = page.find_all('div', class_='listagem_tabela')
        for tb in tables:
            disciplina = {}
            rows = tb.find_all('tr')
            cols = rows[1].find_all('td')
            disciplina['codigo'] = cols[0].text.strip()
            disciplina['nome'] = cols[1].a.text.strip()
            disciplina['tipo'] = cols[2].text.strip()
            disciplina['ch'] = cols[3].text.strip()
            data.append(disciplina)
    except Exception as e:
        print('erro ao recuperar as disciplinas: ', e)

    disciplinas['data'] = data

    return disciplinas

# https://sigaa.ufma.br/sigaa/public/departamento/extensao.jsf?id=1396&lc=pt_BR
def get_extensoes(codigo):
    link = 'https://sigaa.ufma.br/sigaa/public/departamento/extensao.jsf?id='+codigo
    extensoes = {}

    try:
        page_text = requests.get(link).text
        page = BS(page_text, 'lxml')
        extensoes['data'] = page.find('p', class_='vazio')
    except Exception as e:
        print('erro ao recuperar extensoes: ', e)

    return extensoes


# https://sigaa.ufma.br/sigaa/public/departamento/pesquisa.jsf?id=1396&lc=pt_BR
def get_pesquisas(codigo):
    link = 'https://sigaa.ufma.br/sigaa/public/departamento/pesquisa.jsf?id='+codigo
    pesquisas = {}

    try:
        page_text = requests.get(link).text
        page = BS(page_text, 'lxml')
        pesquisas['data'] = page.find('p', class_='vazio')
    except Exception as e:
        print('erro ao recuperar pesquisas: ', e)

    return pesquisas

# https://sigaa.ufma.br/sigaa/public/departamento/monitoria.jsf?id=1396&lc=pt_BR
def get_monitorias(codigo):
    link = 'https://sigaa.ufma.br/sigaa/public/departamento/monitoria.jsf?id='+codigo
    monitorias = {}

    try:
        page_text = requests.get(link).text
        page = BS(page_text, 'lxml')
        monitorias['data'] = page.find('p', class_='vazio')
    except Exception as e:
        print('erro ao recuperar as monitorias: ', e)
    
    return monitorias


# https://sigaa.ufma.br/sigaa/public/departamento/documentos.jsf?id=1396&lc=pt_BR
def get_documentos(codigo):
    link = 'https://sigaa.ufma.br/sigaa/public/departamento/documentos.jsf?id='+codigo
    documentos = {}

    try:
         page_text = requests.get(link).text
         page = BS(page_text, 'lxml')
         documentos['data'] = page.find('p', class_='vazio')
    except Exception as e:
         print('erro ao recuperar os documentos: ', e)

    return documentos
