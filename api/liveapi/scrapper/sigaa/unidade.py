import requests
import json
from bs4 import BeautifulSoup as BS


# https://sigaa.ufma.br/sigaa/public/centro/portal.jsf?lc=pt_BR&id=966
def get_unidade(codigo):
    link = 'https://sigaa.ufma.br/sigaa/public/centro/portal.jsf?id='+codigo+'&lc=pt_BR'
    unidade = {}

    try:
        page_text = requests.get(link).text
        page = BS(page_text, 'lxml')
        titulo = page.find('span', class_='portal-title corto').get_text()
        div = page.find(
            'div', class_='module variacao-module-02 orgaos-vinculados')
        info_centro = div.find_all('li')

        unidade['nome'] = titulo.strip()
        unidade['diretor'] = info_centro[1].get_text().strip()
        unidade['telefone'] = info_centro[3].get_text().strip()
        unidade['end_alt'] = info_centro[5].get_text().strip()

    except:
        print('erro ao recuperar unidade!')
    return unidade

# https://sigaa.ufma.br/sigaa/public/centro/lista_departamentos.jsf?id=966&lc=pt_BR
def get_subunidades(codigo):
    link = "https://sigaa.ufma.br/sigaa/public/centro/lista_departamentos.jsf?id=" + \
        codigo+"&lc=pt_BR"
    subunidades = []

    try:
        page_text = requests.get(link).text
        page = BS(page_text, 'lxml')
        table = page.find('table', class_="table_lt")
        rows = table.find_all('tr')
        for row in rows[1:]:
            subunidade = {}
            cols = row.find_all('td')
            href = cols[0].find("a").get('href')
            pos = href.find("id=")
            codigo = href[pos+3:]
            subunidade['codigo'] = codigo
            subunidade['nome'] = cols[0].get_text().strip()
            subunidades.append(subunidade)

    except:
        print('erro ao recuperar a subunidade!')
    return subunidades

# https://sigaa.ufma.br/sigaa/public/centro/bases_pesquisa.jsf?id=966&lc=pt_BR
def get_grupos_pesquisa(codigo):
    link = 'https://sigaa.ufma.br/sigaa/public/centro/bases_pesquisa.jsf?id='+codigo+'&lc=pt_BR'
    grupo_de_pesquisas = []

    try:
        page_text = requests.get(link).text
        page = BS(page_text, 'lxml')
        conteudo = page.find('table', class_='table_lt')
        rows = conteudo.find_all('tr')[1:]

        for row in rows:
            pesquisa = {}
            cols = row.find_all('td')
            pesquisa['tema'] = cols[0].get_text().strip()
            pesquisa['pesquisador'] = cols[1].get_text().strip()
            pesquisa['href'] = 'https://sigaa.ufma.br' + \
                cols[1].find('a').get('href')
            grupo_de_pesquisas.append(pesquisa)

    except:
        print('erro ao recuperar as bases de pesquisas!')
    return grupo_de_pesquisas


# https://sigaa.ufma.br/sigaa/public/centro/lista_cursos.jsf?id=966&lc=pt_BR
# aqui tem os codigos do curso, talvez tenha que usar https://sigaa.ufma.br/sigaa/public/curso/lista.jsf
def get_cursos_graduacao(codigo):
    link = 'https://sigaa.ufma.br/sigaa/public/centro/lista_cursos.jsf?id='+codigo+'&lc=pt_BR'
    cursos = []
    data = {}
    page_text = requests.get(link).text
    page = BS(page_text, 'lxml')
    conteudo = page.find('table', class_='table_lt')
    rows = conteudo.find_all('tr')[1:]

    try:
        for row in rows:
            curso = {}
            cols = row.find_all('td')
            curso['nome'] = cols[0].get_text().strip()
            curso['municipio'] = cols[1].get_text().strip()
            curso['modalidade'] = cols[2].get_text().strip()
            curso['coordenador'] = cols[3].get_text().strip()
            cursos.append(curso)
    except:
        print('erro ao recuperar os cursos de graduação!')
    
    data['data'] = cursos
    return data

# https://sigaa.ufma.br/sigaa/public/centro/lista_programas.jsf?id=966&lc=pt_BR

def get_cursos_pos(codigo):
    link = 'https://sigaa.ufma.br/sigaa/public/centro/lista_programas.jsf?id='+codigo+'&lc=pt_BR'
    cursos_pos = []

    page_text = requests.get(link).text
    page = BS(page_text, 'lxml')
    conteudo = page.find('table', class_='table_lt')
    rows = conteudo.find_all('tr')[1:]
    
    try:
        for row in rows:
            curso = {}
            curso['programa'] = row.find('a').get_text().strip()
            href = row.find('a').get('href')
            pos = href.find('idPrograma=')
            codigo = href[pos+11:]
            curso['id'] = codigo
            curso['href'] = 'https://sigaa.ufma.br/sigaa/public/programa/apresentacao_stricto.jsf?lc=pt_BR&idPrograma='+codigo
            cursos_pos.append(curso)
    except:
        print('erro ao recuperar os cursos de pos-graduação!')

    return cursos_pos

def get_documentos(codigo):
        pass