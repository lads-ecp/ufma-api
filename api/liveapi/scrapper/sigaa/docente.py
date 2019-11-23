import requests
import json
from bs4 import BeautifulSoup as BS


def get_docente(siape):
        link = 'https://sigaa.ufma.br/sigaa/public/docente/portal.jsf?siape='+siape
        docente = {}

        try:
                page_text = requests.get(link).text

                
                page = BS(page_text, 'lxml')

                info = page.find_all('div', class_='secao-pagina')


                docente['nome'] = page.find('p', class_='span outstanding-title').text.strip()
                docente['subunidade'] = page.find('span', class_='outstanding-subtitle').text.strip()
                docente['descricao'] = info[0].text.split('\n')[-2].strip()
                docente['formacao'] = info[1].text.split('\n')[-2].strip()
                docente['areas_interesse'] = info[2].text.split('\n')[-2].strip()
                docente['lattes'] = page.find(
                    'a', id='endereco-lattes').get('href').strip()
                docente['email'] = page.find_all('span')[-5].text.strip()
                docente['telefone'] = page.find_all(
                    'span')[-6].text.strip()

                imgurl = "https://sigaa.ufma.br/" + page.find("div", class_="span2").find("img").get("src")
                docente["urlimg"] = imgurl
                
        except Exception as e:
                print('erro ao recuperar o docente: ', e)

        return docente


# https://sigaa.ufma.br/sigaa/public/docente/disciplinas.jsf?siape=407686&lc=pt_BR

def get_turmas(siape):
        link = 'https://sigaa.ufma.br/sigaa/public/docente/disciplinas.jsf?siape='+siape
        turmas = {}
        data = []

        try:
                page_text = requests.get(link).text
                page = BS(page_text, 'lxml')

                tables = page.find_all('div', class_='listagem_tabela')

                for tb in tables:
                        rows = tb.find_all('tr')
                        for i in range(len(rows)-1):
                                disciplina = {}
                                if i%2 != 0:
                                        cols = rows[i].find_all('td')
                                        disciplina['codigo'] = cols[0].text.strip()
                                        disciplina['nome'] = cols[1].a.text.strip()
                                        disciplina['ano'] = cols[2].text.strip()
                                        disciplina['ch'] = cols[3].text.strip()
                                        data.append(disciplina)

                turmas['data'] = data
        except Exception as e:
                print("erro ao recuperar turmas: ", e)

        return turmas  


# https://sigaa.ufma.br/sigaa/public/docente/pesquisa.jsf?siape=407686&lc=pt_BR
def get_projetos(siape):
        link = 'https://sigaa.ufma.br/sigaa/public/docente/pesquisa.jsf?siape='+siape
        projetos = {}
        data = []

        try:
                page_text = requests.get(link).text
                page = BS(page_text, 'lxml')

                tables = page.find_all('div', 'listagem_tabela')

                for tb in tables:
                        rows = tb.find_all('tr')[1:]
                        for row in rows:
                                projeto = {}
                                cols = row.find_all('td')
                                projeto['codigo'] = cols[0].text.strip()
                                projeto['nome'] = cols[1].text.strip()
                                projeto['area'] = cols[2].text.strip()
                                projeto['ano'] = cols[3].text.strip()
                                data.append(projeto)
                projetos['data'] = data
        
        except Exception as e:
                print('erro ao recuperar os projetos: ', e)
        
        return projetos

#https://sigaa.ufma.br/sigaa/public/docente/producao.jsf?siape=1763530&lc=pt_BR
def get_producao (siape):
        link = 'https://sigaa.ufma.br/sigaa/public/docente/producao.jsf?siape='+siape
        producao = {}

        try:
                page_text = requests.get(link).text
                page = BS(page_text, 'lxml')
                tables = page.find_all('div', 'listagem_tabela')
                artigos = []
                publicacoes = []
                capitulos= []
                tecnologias = []
                tccs = []

                for index in range(len(tables)):
                        rows = tables[index].find_all('tr')
                        if rows[0].find('td').text.strip()[:7] == 'Artigos': #Artigos
                                
                                for row in rows[1:]:
                                        cols = row.find('td')
                                        artigo = {}
                                        artigo['autor'] = page.find('h4', class_='span outstanding-title').text.strip()
                                        artigo['tema'] = cols.b.text.strip()
                                        artigo['ano'] = cols.text.split(',')[0].strip()
                                        artigo['issn'] = cols.text.split(',')[-1].strip()[6:]
                                        artigos.append(artigo)

                        if rows[0].find('td').text.strip()[:7] == 'Publica': #Publicações em Eventos
                                
                                for row in rows[1:]:
                                        cols = row.find('td')
                                        publicacao = {}
                                        publicacao['tema'] = cols.b.text.strip()
                                        info = cols.text.replace(publicacao['tema'],'#')
                                        publicacao['autores'] = info.split('#')[0].split(',')[1:-1]
                                        publicacao['autores'][0] = publicacao['autores'][0].strip()
                                        publicacao['ano'] = cols.text[:4]
                                        publicacao['evento'] = info.split('#')[1].split(',')[1].strip()
                                        publicacoes.append(publicacao)
                        
                        if rows[0].find('td').text.strip()[:3] == 'Cap':

                                for row in rows[1:]:
                                        cols = row.find('td')
                                        capitulo = {}
                                        capitulo['titulo'] = cols.b.text.strip()
                                        info = cols.text.replace(capitulo['titulo'],'#')
                                        capitulo['livro'] = info.split('#')[1].split(',')[1].strip()
                                        capitulo['autores'] = info.strip().split('#')[1].split(',')[2:]
                                        capitulo['ano']= cols.text[:4]
                                        capitulos.append(capitulo)
                
                        if rows[0].find('td').text.strip()[:5] == 'Produ':

                                for row in rows[1:]:
                                        cols = row.find('td')
                                        producao = {}
                                        producao['titulo'] = cols.b.text.strip()
                                        info = cols.text.replace(producao['titulo'],'#')
                                        producao['autores'] = info.strip().split('#')[1].split(',')[1:]
                                        producao['ano']= cols.text[:4]
                                        tecnologias.append(producao)
                        
                        if rows[0].find('td').text.strip()[:8] == 'Trabalho':

                                for row in rows[1:]:
                                        cols = row.find('td')
                                        tcc = {}
                                        tcc['titulo'] = cols.b.text.strip()
                                        info = cols.text.replace(tcc['titulo'],'#')
                                        tcc['autor'] = info.split('#')[1].split(',')[1].strip()
                                        tcc['data'] = info.split('#')[1].split(',')[2].strip()
                                        print(tcc)
                                        tccs.append(tcc)
                
                producao['artigos'] = artigos
                producao['publicacoes'] = publicacoes
                producao['capitulos_livros'] = capitulos
                producao['producao_tecnologica'] = tecnologias
                producao['orientandos'] = tccs
                                        
                
        except Exception as e:
                print('erro ao recuperar as produções: ', e)

        return producao
                        

#print (get_docente ("1763530"))