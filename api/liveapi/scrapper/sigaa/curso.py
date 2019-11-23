import requests
from bs4 import BeautifulSoup as BS


def getViewState(r):
    text = r.text
    page = BS(text, 'lxml')
    input = page.find('input', id='javax.faces.ViewState')
    return input.get("value")


def col2curso(cols):
    nome = cols[0].text.strip()
    sede = cols[1].text.strip()
    modalidade = cols[2].text.strip()
    coordenador = cols[3].text.strip()
    url = cols[4].find("a").get('href')
    i1, i2 = url.find("id=")+3, url.find("&lc")
    codigo = url[i1:i2]
    return {"nome": nome, "municipio": sede,  "codigo": codigo, "modalidade": modalidade, "coordenador":coordenador}


def get_cursos():
    link = 'https://sigaa.ufma.br/sigaa/public/curso/lista.jsf' 
    try:
        page_response = requests.get(link)
        page = BS(page_response.text, 'lxml')
        id = getViewState(page_response)
        cookies = dict(JSESSIONID=page_response.cookies['JSESSIONID'])
        payload = {
            "form": "form",  "nivel": "G", "form:checkModalidade": "on",
            "form:modalidadeDeEnsino": 1, "form:lc": "pt_BR",
            "form:consultarCursos": "Consultar", "javax.faces.ViewState": id
        }
        url ='https://sigaa.ufma.br/sigaa/public/curso/lista.jsf'
        response = requests.post(url, data=payload, cookies=cookies)
        page = BS(response.text, 'lxml')
        table = page.find('table', class_='listagem')
        rowsPar = table.find_all('tr', class_='linhaPar')
        rowsImpar = table.find_all('tr', class_='linhaImpar')
        cursos = []
        for r in rowsPar:
            cols = r.find_all('td')
            cursos.append(col2curso(cols))

        for r in rowsImpar:
            cols = r.find_all('td')
            cursos.append(col2curso(cols))

    except Exception as e:
        print("erro ao recuperar as monografias: ", e)

    return cursos


def get_monografias(codigo, ano):
    link = 'https://sigaa.ufma.br/sigaa/public/curso/monografias_curso.jsf?lc=pt_BR&id=' + codigo
    data = []
    monografias = {}
    try:
        page_response = requests.get(link)
        page = BS(page_response.text, 'lxml')
        id = getViewState(page_response)
        cookies = dict(JSESSIONID=page_response.cookies['JSESSIONID'])
        payload = {
            "form": "form", "form:checkAno": "on", "form:idCurso": codigo,
            "form:lc": "pt_BR", "form:ano": ano, "form:buscar": "Buscar",
            "javax.faces.ViewState": id
        }
        url = 'https://sigaa.ufma.br/sigaa/public/curso/monografias_curso.jsf'
        response = requests.post(url, data=payload, cookies=cookies)
        page = BS(response.text, 'lxml')
        table = page.find('table', class_="table_lt")
        rows = table.find_all('tr')[1:]
        for index in range(len(rows)-1):
            monografia = {}
            cols = rows[index].find_all('td')
            if len(cols) == 6:
                monografia['discente'] = cols[2].text.strip()
                monografia['orientador'] = cols[3].text.strip()
                monografia['titulo']= rows[index+1].text.strip()[7:].strip()
                data.append(monografia)
    except Exception as e:
        print("erro ao recuperar as monografias: ", e)
    monografias['data'] = data
    return monografias


def get_discentes_ativos(codigo):
    link = 'https://sigaa.ufma.br/sigaa/public/curso/alunos_curso.jsf?lc=pt_BR&id=' + codigo
    discentes = {}
    data = []
    try:
        page_text = requests.get(link).text
        page = BS(page_text, 'lxml')
        table = page.find('table', class_='table_lt')
        rows = table.find_all('tr')[1:]
        for row in rows[:-1]:
            discente = {}
            cols = row.find_all('td')
            discente['nome_curso'] = page.find_all('span', class_='portal-title-1')[0].text.strip()
            discente['codigo_curso'] = codigo
            discente['matricula'] = cols[0].text.strip()
            discente['nome'] = cols[1].text.strip()
            data.append(discente)

    except Exception as e:
        print('erro ao recuperar os alunos : ', e)
    discentes['data'] = data
    return discentes


def get_turmas(codigo, ano, periodo):
    link = 'https://sigaa.ufma.br/sigaa/public/curso/turma_curso.jsf?lc=pt_BR&id=' + codigo
    data = []
    turmas = {}
    try:
        page_response = requests.get(link)
        page = BS(page_response.text, 'lxml')
        id = getViewState(page_response);
        cookies = dict(JSESSIONID=page_response.cookies['JSESSIONID'])
        payload = {
            "form": "form", "form:inputAno": ano, "form:id": codigo,
            "form:lc": "pt_BR", "form:buscarTurmas": "Buscar", "javax.faces.ViewState": id,
            "form:inputPeriodo": periodo
        }
        url = 'https://sigaa.ufma.br/sigaa/public/curso/turma_curso.jsf?lc=pt_BR&id=' + codigo
        response = requests.post(url, data=payload, cookies=cookies)
        page = BS(response.text, 'lxml')
        divs = page.find_all('div', class_='listagem_tabela')
        n = len (divs)
        for div in divs[:n-1]:
            nome_curso = div.find ('div', id='group_lt').find("a").get_text().strip()
            tbody = div.find ('tbody')
            rows = tbody.find_all('tr')
            for row in rows:
                turma = {}
                turma["nome_curso"] = nome_curso
                turma["vagas"] = row.find ('td', class_='colVagas').get_text().strip()
                turma["horario"] = row.find ('td', class_='horario').get_text().strip()
                turma["docente"] = row.find ('td', class_='nome').get_text().strip().replace('\t', '').replace('\n', '')
                turma["numturma"] = row.find ('td', align='center').get_text().strip()
                data.append(turma)
    except Exception as e:
        print("erro ao recuperar as turmas: ", e)
    turmas['data'] = data
    return turmas
