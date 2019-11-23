
import requests
import urllib.parse
from unidecode import unidecode
import json
from unicodedata import normalize


from pymarc import JSONReader


from bs4 import BeautifulSoup as BS

def getViewState(r):
    text = r.text
    page = BS(text,'lxml')
    input = page.find('input', id='javax.faces.ViewState')
    return input.get("value")

headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,de-DE;q=0.6,de;q=0.5,en-GB;q=0.4'
            }

def get_detail (payload, cookies, id):
    payload["javax.faces.ViewState"]: id
    payload["formBuscaPublica:ClinkView"] = "formBuscaPublica:ClinkView"
    payload["idTitulo"] = "81809"    
    payload["idsBibliotecasAcervoPublicoFormatados"] = "50_39_40_30_49_37_34_32_36_47_860203_42_45_43_48_31_41_38_33_46_44_35"
    payload["apenasSituacaoVisivelUsuarioFinal"] = "true"
    url = "https://sigaa.ufma.br/sigaa/public/biblioteca/buscaPublicaAcervo.jsf"
    try:
        page_response = requests.post(url, data=payload, cookies=cookies)
        page = BS(page_response.text, 'lxml')
        #table = page.find('table', class_='visualizacao')
        print (page)
    except Exception as e:
        print("erro ao recuperar os details acervo: ", e)


def get_acervo(titulo, autor=None, limit=25):
    link = 'https://sigaa.ufma.br/sigaa/public/biblioteca/buscaPublicaAcervo.jsf'

    if not limit:
        limit = 25

    livros = []
    try:
        page_response = requests.get(link)
        page = BS(page_response.text, 'lxml')
        
        #print ("---", limit)
        id = getViewState(page_response);
        cookies = dict(JSESSIONID=page_response.cookies['JSESSIONID'])

        #payload =  { "form":"form", "form:checkAno":"on", "form:idCurso":codigo, "form:lc":"pt_BR", "form:ano":ano, "form:buscar":"Buscar", "javax.faces.ViewState":id}
        payload = {
            "formBuscaPublica": "formBuscaPublica",
            "formBuscaPublica:j_id_jsp_476315297_53": "1",
            "formBuscaPublica:j_id_jsp_476315297_55": str(limit),
            "formBuscaPublica:j_id_jsp_476315297_58": "-1",
            "formBuscaPublica:j_id_jsp_476315297_62": "-1",
            "formBuscaPublica:checkTipoMaterial": "on",
            "formBuscaPublica:j_id_jsp_476315297_66": "16",
            "formBuscaPublica:botaoPesquisarPublicaMulti": "Pesquisar",
            "javax.faces.ViewState": id
        }

        if (titulo):
            titulo = unidecode(titulo)
            titulo = urllib.parse.quote_plus(titulo)
            payload["formBuscaPublica:checkTitulo"] = "on"
            payload["formBuscaPublica:j_id_jsp_476315297_41"] = titulo,

        if (autor):
            autor = unidecode(autor)
            autor = urllib.parse.quote_plus(autor)
            payload["formBuscaPublica:checkAutor"] = "on"
            payload["formBuscaPublica:j_id_jsp_476315297_43"] = autor

          
        url ='https://sigaa.ufma.br/sigaa/public/biblioteca/buscaPublicaAcervo.jsf'
        response = requests.post(url, data=payload, cookies=cookies)

        page = BS(response.text,'lxml')
        div = page.find('div', id="formBuscaPublica:divResultadoPesquisaTitulos")
        table = div.find('table', class_='listagem')
        rowsPar = table.find_all('tr', class_='linhaPar')
        rowsImpar = table.find_all('tr', class_='linhaImpar')
        rows = rowsPar + rowsImpar
        for row in rows:
            cols = row.find_all('td')
            if (len (cols) == 7):
                jssrc = cols[5].find("a").get("onclick")
                q = "'idTitulo':'"
                idi = jssrc.find (q) + len (q)
                idf = jssrc.find ("','", idi) 
                codigo = jssrc[idi:idf]
                
                #livro = extrai_marc_to_json(codigo)
                livro = { "autor" : cols[0].text.strip(),
                        "titulo" : cols[1].text.strip(),
                        "ano" : cols[3].text.strip(),
                        "edicao" : cols[4].text.strip(),
                        "codigo" : codigo,
                        "url_marc" : "https://sigaa.ufma.br/sigaa/public/biblioteca/informacoesMarcTitulo.jsf?idTitulo="+codigo+"&exibirPaginaDadosMarc=true"
                         }
                livros.append (livro)
  
    except Exception as e:
        print("erro ao recuperar o acervo: ", e)
    

    return livros


# tratar os dados no formato marc

def getfl(l,i):
    return l[i] if i < len(l) else ' '

def to_marc_json (ls):
    dic = {}
    print (ls)
    dic["leader"] = ls[0][1]
    dic["fields"] = []
    for t in ls[1:]:
        field = {}
        s = t[0].split()
        if t[1][0] == "$":
            d = {"ind1" : " ", "ind2" : " ", "subfields" : []}
            l =  t[1].split ("$")
            #print (l)
            for sub in l[1:]:
                subf = {}
                subf[sub[0]] = sub[1:].strip()
                #print (subf)
                d["subfields"].append (subf)
                d["ind1"] = getfl(s,1)
                d["ind2"] = getfl (s,2)
            field[s[0]] = d
        else:
            field[s[0]] = t[1].strip()         
        dic["fields"].append (field)

    return (dic) 

def fieldstovalues(fields):
    l = []
    for f in fields:
        l.append(f.value())
    return l

def getfieldValue (r, n, l):
    if r[n]:
        return r[n][l]
    else:
        return ""
def extrai_marc_to_json (idtitulo):
    url = "https://sigaa.ufma.br/sigaa/public/biblioteca/informacoesMarcTitulo.jsf?idTitulo="+idtitulo+"&exibirPaginaDadosMarc=true"
    values = []
    try:
        page_response = requests.get(url)
        page = BS(page_response.text, 'lxml')
        table = page.find('table', class_='tabelaTransparete')
        rows = table.find_all('tr')
        if (len(rows) < 2):
            return None
        for r in rows[1:]:
            cols = r.find_all('td')
            c0 = cols[0].text.strip().replace ("\t","").replace("\r\n","").replace("&nbsp","")
            c1 = cols[1].text.strip().replace ("\t","").replace("\r\n","").replace("&nbsp","")
            values.append ((c0,c1))
        
    except Exception as e:
        print("erro ao extrair : ", e)

    dic = to_marc_json(values)
    jsr = json.dumps(dic)
    reader = JSONReader (jsr)

    for r in reader:
        '''
        if (r.isbn()):
            urlGoogle = "https://www.googleapis.com/books/v1/volumes?q="+r.isbn()
            google_book = requests.get(urlGoogle).json()
        else:
            google_book = {}
        '''  

        return {"title" : r.title(), "author" : r.author(), "isbn" : r.isbn(),
                "position" :  r['090']['a'] + " " + r['090']['b'], "id" : idtitulo,
                "publocation" : getfieldValue(r,'260','a'), "pubyear" : r.pubyear(), 
                "publisher" : r.publisher(), "edition" : getfieldValue(r,'250','a'),
                "subjects" : fieldstovalues (r.subjects()) }

