import csv
import re
import requests as req

from abc import ABCMeta, abstractmethod

from requests.exceptions import MissingSchema

from bs4 import BeautifulSoup
from decouple import config
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from tqdm import tqdm

from leis_brasileiras.commons import striphtml
from leis_brasileiras.urls import (
    urls_decretos_planalto,
    urls_leis_ordinarias_planalto,
    urls_medidas_provisorias,
    urls_projetos_leis_casa_civil,
    urls_projetos_leis_complementares_casa_civil,
    urls_projetos_leis_congresso_casa_civil)


class Planalto(metaclass=ABCMeta):
    base_url = "http://www4.planalto.gov.br/legislacao/portal-legis/"\
               "legislacao-1/"
    origin = 'Planalto'

    @abstractmethod
    def __init__(self):
        options = Options()
        options.headless = True
        print("Iniciando navegador Firefox em modo headless")
        self.driver = Firefox(
            options=options,
            executable_path=config('DRIVER_PATH')
        )

    def get_content(self, link):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X'
                   '10_10_1) Appl eWebKit/537.36 (KHTML, like Gecko)'
                   'Chrome/39.0.2171.95Safari/537.36'
                   }
        resp = req.get(link, headers=headers)
        content = resp.content.decode('latin-1')
        return BeautifulSoup(content, features='lxml').find('body').text

    def get_row_info(self, tds, year):
        try:
            link = tds[0].find_element_by_tag_name('a').get_attribute('href')
            link = link.replace('https', 'http')
            inteiro_teor = striphtml(self.get_content(link))
        except (NoSuchElementException, MissingSchema):
            inteiro_teor = ''

        info = {k: v.text for k, v in zip(('lei', 'ementa'), tds)}
        info['ano'] = year
        info['inteiro_teor'] = inteiro_teor
        return info

    def _wait_table(self):
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.presence_of_element_located(
            (By.TAG_NAME, 'table')
            )
        )

    def extract_info(self, year, url, writer):
        download_desc = 'Baixando {tipo} {origin} ({ano})'.format(
            tipo=self.tipo_lei,
            origin=self.origin,
            ano=year
        )

        self.driver.get(self.base_url + url)

        self._wait_table()
        table = self.driver.find_element_by_tag_name('table')
        rows = table.find_elements_by_tag_name('tr')

        # rows[1:] to skip table header
        for row in tqdm(rows[1:], desc=download_desc):
            tds = row.find_elements_by_tag_name('td')
            row_info = self.get_row_info(tds, year)
            writer.writerow(row_info)

    def download(self):
        with open(self.file_destination, 'w', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=self.header,
                delimiter=";",
                quotechar='"'
            )
            writer.writeheader()

            for year, url in self.urls.items():
                self.extract_info(year, url, writer)

        print('Fechando Navegador Firefox')
        self.driver.close()


class DecretosPlanalto(Planalto):
    def __init__(self, file_destination):
        super().__init__()
        self.file_destination = file_destination
        self.tipo_lei = 'decretos'
        self.urls = urls_decretos_planalto
        self.header = ['lei', 'ementa', 'ano', 'inteiro_teor']


class LeisOrdinariasPlanalto(Planalto):
    def __init__(self, file_destination):
        super().__init__()
        self.file_destination = file_destination
        self.tipo_lei = 'leis ordinárias'
        self.urls = urls_leis_ordinarias_planalto
        self.header = ['lei', 'ementa', 'ano', 'inteiro_teor']


class LeisComplementaresPlanalto(Planalto):
    def __init__(self, file_destination):
        super().__init__()
        self.file_destination = file_destination
        self.tipo_lei = 'leis complementares'
        self.urls = {
            'todos-os-anos': 'leis-complementares-1/'
                             'todas-as-leis-complementares-1'
        }
        self.header = ['lei', 'ementa', 'ano', 'inteiro_teor']


class LeisDelegadasPlanalto(Planalto):
    def __init__(self, file_destination):
        super().__init__()
        self.file_destination = file_destination
        self.tipo_lei = 'leis delegadas'
        self.header = ['lei', 'ementa', 'ano', 'inteiro_teor']


class MedidasProvisoriasPlanalto(Planalto):
    def __init__(self, file_destination):
        super().__init__()
        self.file_destination = file_destination
        self.tipo_lei = 'medidas provisórias'
        self.urls = urls_medidas_provisorias
        self.header = ['lei', 'ementa', 'ano', 'inteiro_teor']


class DecretosLeisPlanalto(Planalto):
    def __init__(self, file_destination):
        super().__init__()
        self.file_destination = file_destination
        self.tipo_lei = 'decretos-leis'
        self.urls = {'1937-1946': 'decretos-leis/1937-a-1946-decretos-leis-1',
                     '1965-1988': 'decretos-leis/1965-a-1988-decretos-leis'}
        self.header = ['lei', 'ementa', 'ano', 'inteiro_teor']


class PlanaltoProjetosReader(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    def get_row_info(self, tds, year):
        inteiro_teor = ''
        motivacao = ''
        try:
            links = tds[0].find_elements_by_tag_name('a')
            if len(links) >= 1:
                link_inteiro_teor = links[0].get_attribute('href')
                link_inteiro_teor = link_inteiro_teor.replace('https', 'http')
                inteiro_teor = striphtml(self.get_content(link_inteiro_teor))
            if len(links) == 2:
                link_motivacao = links[1].get_attribute('href')
                link_motivacao = link_motivacao.replace('https', 'http')
                motivacao = striphtml(self.get_content(link_motivacao))

        except (NoSuchElementException, MissingSchema):
            pass

        numero_lei = re.sub(r'\s+', '', tds[0].text)
        numero_lei = re.search(r'(\d\.|\d+)?\d+\/\d+', numero_lei)
        if numero_lei:
            numero_lei = numero_lei[0]
        info = {'lei': numero_lei}
        info['ementa'] = tds[1].text
        info['ano'] = year
        info['inteiro_teor'] = inteiro_teor
        info['motivacao'] = motivacao

        if len(tds) == 3:
            info['situacao'] = tds[2].text

        return info


class ProjetosPlanalto(PlanaltoProjetosReader, Planalto):
    def __init__(self, file_destination):
        super().__init__()
        self.file_destination = file_destination
        self.tipo_lei = 'projetos-lei'
        self.urls = urls_projetos_leis_casa_civil
        self.header = [
            'lei',
            'ementa',
            'ano',
            'inteiro_teor',
            'situacao',
            'motivacao'
        ]


class ProjetosLeisComplementaresPlanalto(PlanaltoProjetosReader, Planalto):
    def __init__(self, file_destination):
        super().__init__()
        self.file_destination = file_destination
        self.tipo_lei = 'projetos-lei-complementar'
        self.urls = urls_projetos_leis_complementares_casa_civil
        self.header = [
            'lei',
            'ementa',
            'ano',
            'inteiro_teor',
            'situacao',
            'motivacao'
        ]


class ProjetosLeisCongressoPlanalto(PlanaltoProjetosReader, Planalto):
    def __init__(self, file_destination):
        super().__init__()
        self.file_destination = file_destination
        self.tipo_lei = 'projetos-lei-congresso-nacional'
        self.urls = urls_projetos_leis_congresso_casa_civil
        self.header = [
            'lei',
            'ementa',
            'ano',
            'inteiro_teor',
            'situacao',
            'motivacao'
        ]


class Alerj(metaclass=ABCMeta):

    dns = "http://alerjln1.alerj.rj.gov.br"
    base_url = dns + "/contlei.nsf/{tipo}?OpenForm&Start={start}&Count=1000"
    header = ['lei', 'ano', 'autor', 'ementa']

    def __init__(self, file_destination, check_metadata_size=True):
        self.file_destination = file_destination
        self.check_metadata_size = check_metadata_size

    def visit_url(self, start):
        url = self.base_url.format(tipo=self.tipo, start=start)
        common_page = req.get(url)
        soup = BeautifulSoup(common_page.content, features='lxml')
        return soup.find_all('tr')

    def parse_metadata(self, row):
        columns = row.find_all('td')
        data = [c.text for c in columns if c.text and c.text != '*']
        return dict(
            zip(
                self.header,
                data
            )
        )

    def parse_full_content(self, row):
        # There may be links pointing to the form, which are not wanted
        links = [l for l in row.find_all('a') if l.has_attr('href') and 'OpenDocument' in l['href']]
        full_content_link = self.dns + links[0]['href']
        resp = req.get(full_content_link)
        soup = BeautifulSoup(resp.content, features='lxml')
        body = soup.find('body')
        strip_body = striphtml(body.text)

        # Documents come with noise at the end, this removes that
        end_doc_i = strip_body.find('HTML5 Canvas')
        return strip_body[:end_doc_i]

    def download(self):
        with open(self.file_destination, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=self.header + ['inteiro_teor'],
                delimiter=";",
                quotechar='"'
            )
            writer.writeheader()

            page = 1
            rows = self.visit_url(start=page)
            while len(rows) > 1:
                download_desc = 'Baixando {tipo} {orgao} - página: {page}'\
                    .format(tipo=self.tipo_lei, orgao=self.orgao, page=page)

                # Skip header
                for row in tqdm(rows[1:], desc=download_desc):
                    if not row.find_all('td'):
                        continue
                    metadata = self.parse_metadata(row)
                    if self.check_metadata_size and len(metadata) != len(self.header):
                        continue
                    metadata['inteiro_teor'] = self.parse_full_content(row)
                    writer.writerow(metadata)

                start = page * 1000 + 1
                page += 1
                rows = self.visit_url(start)


class DecretosAlerj(Alerj):
    orgao = 'Alerj'
    tipo = 'DecretoInt'
    tipo_lei = 'decretos'


class LeisOrdinariasAlerj(Alerj):
    orgao = 'Alerj'
    tipo = 'LeiOrdInt'
    tipo_lei = 'leis ordinárias'


class LeisComplementaresAlerj(Alerj):
    orgao = 'Alerj'
    tipo = 'LeiCompInt'
    tipo_lei = 'leis complementares'


class ProjetosDeLeiAlerj1923(Alerj):
    orgao = 'Alerj'
    dns = "http://alerjln1.alerj.rj.gov.br"
    base_url = dns + "/scpro1923.nsf/{tipo}?OpenView&Start={start}&Count=1000"

    tipo = 'VLeiInt'
    tipo_lei = 'leis ordinárias'
    header = ['projeto', 'ementa', 'data_publicacao', 'autor']


class ProjetosDeLeiComplementarAlerj1923(Alerj):
    orgao = 'Alerj'
    dns = "http://alerjln1.alerj.rj.gov.br"
    base_url = dns + "/scpro1923.nsf/{tipo}?OpenView&Start={start}&Count=1000"

    tipo = 'VLeiCompInt'
    tipo_lei = 'leis ordinárias'
    header = ['projeto', 'ementa', 'data_publicacao', 'autor']


class ProjetosDeDecretosAlerj1923(Alerj):
    orgao = 'Alerj'
    dns = "http://alerjln1.alerj.rj.gov.br"
    base_url = dns + "/scpro1923.nsf/{tipo}?OpenView&Start={start}&Count=1000"

    tipo = 'VDecretoInt'
    tipo_lei = 'leis ordinárias'
    header = ['projeto', 'ementa', 'data_publicacao', 'autor']


class EmendasLeiOrganicaCamaraMunicipalRJ(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/contlei.nsf/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'EmendaInt'
    tipo_lei = 'emendas a lei organica'
    header = ['emenda', 'ano', 'status', 'ementa', 'autor']


class DecretosCamaraMunicipalRJ(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/contlei.nsf/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'DecretoInt'
    tipo_lei = 'decretos'
    header = ['decreto', 'ano', 'ementa', 'autor']


class LeisOrdinariasCamaraMunicipalRJ(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/contlei.nsf/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'LeiOrdInt'
    tipo_lei = 'leis ordinárias'
    header = ['lei', 'ano', 'status', 'ementa', 'autor']


class LeisComplementaresCamaraMunicipalRJ(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/contlei.nsf/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'LeiCompInt'
    tipo_lei = 'leis complementares'
    header = ['lei_comp', 'ano', 'status', 'ementa', 'autor']


class ResolucoesPlenariasCamaraMunicipalRJ(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/contlei.nsf/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'ResolucaoInt'
    tipo_lei = 'resoluções plenárias'
    header = ['resolucao', 'ano', 'ementa', 'autor']

# Projetos de Lei 2021-2024 CamaraRJ

class ProjetosDeEmendasLeiOrganicaCamaraMunicipalRJ2124(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro2124.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'EmendaInt'
    tipo_lei = 'projetos de emenda a lei organica'
    header = ['projeto', 'ementa', 'data_publicacao', 'autor']


class ProjetosDeLeiCamaraMunicipalRJ2124(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro2124.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'LeiInt'
    tipo_lei = 'projetos de lei'
    header = ['projeto', 'ementa', 'data_publicacao', 'autor']


class ProjetosDeLeiComplementarCamaraMunicipalRJ2124(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro2124.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'LeiCompInt'
    tipo_lei = 'projetos de lei complementar'
    header = ['projeto', 'ementa', 'data_publicacao', 'autor']


class ProjetosDeDecretoCamaraMunicipalRJ2124(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro2124.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'DecretoInt'
    tipo_lei = 'projetos de decreto'
    header = ['projeto', 'ementa', 'data_publicacao', 'autor']


class ProjetosResolucaoCamaraMunicipalRJ2124(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro2124.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'ResolucaoInt'
    tipo_lei = 'projetos de resolução'
    header = ['projeto', 'ementa', 'data_publicacao', 'autor']


class IndicacoesCamaraMunicipalRJ2124(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro2124.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'IndInt'
    tipo_lei = 'indicacoes'
    header = ['indicacao', 'ementa', 'data_publicacao', 'autor']


class MocoesCamaraMunicipalRJ2124(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro2124.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'mocaoInt'
    tipo_lei = 'moções'
    header = ['mocao', 'ementa', 'data_publicacao', 'autor']


class RequerimentoInformacaoCamaraMunicipalRJ2124(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro2124.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'ReqInfInt'
    tipo_lei = 'requerimento de informação'
    header = ['requerimento', 'ementa', 'data_publicacao', 'autor']


class RequerimentoCamaraMunicipalRJ2124(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro2124.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'ReqInt'
    tipo_lei = 'requerimento'
    header = ['requerimento', 'ementa', 'data_publicacao', 'autor']


class OficioCamaraMunicipalRJ2124(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro2124.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000&Expand=1'

    tipo = 'OficioInt'
    tipo_lei = 'oficio'
    header = ['oficio', 'ementa', 'data_publicacao', 'autor']


class OficioDenunciaCamaraMunicipalRJ2124(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro2124.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000&Expand=2'

    tipo = 'OficioInt'
    tipo_lei = 'oficio denuncia'
    header = ['oficio', 'ementa', 'data_publicacao', 'autor']


class OficioOutrosCamaraMunicipalRJ2124(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro2124.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000&Expand=3'

    tipo = 'OficioInt'
    tipo_lei = 'oficio outros'
    header = ['oficio', 'ementa', 'data_publicacao', 'autor']


class OficioEditalCamaraMunicipalRJ2124(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro2124.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000&Expand=4'

    tipo = 'OficioInt'
    tipo_lei = 'oficio edital'
    header = ['oficio', 'ementa', 'data_publicacao', 'autor']


class OficioQuestaoOrdemCamaraMunicipalRJ2124(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro2124.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000&Expand=5'

    tipo = 'OficioInt'
    tipo_lei = 'oficio questão de ordem'
    header = ['oficio', 'ementa', 'data_publicacao', 'autor']


class OficioParecerNormativoCJRCamaraMunicipalRJ2124(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro2124.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000&Expand=6'

    tipo = 'OficioInt'
    tipo_lei = 'oficio parecer normativo cjr'
    header = ['oficio', 'ementa', 'data_publicacao', 'autor']


class OficioRecursoCamaraMunicipalRJ2124(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro2124.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000&Expand=7'

    tipo = 'OficioInt'
    tipo_lei = 'oficio recurso'
    header = ['oficio', 'ementa', 'data_publicacao', 'autor']


class OficioRepresentacaoCamaraMunicipalRJ2124(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro2124.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000&Expand=8'

    tipo = 'OficioInt'
    tipo_lei = 'oficio representação'
    header = ['oficio', 'ementa', 'data_publicacao', 'autor']


# Projetos de Lei 2017-2020 CamaraRJ
class ProjetosDeEmendasLeiOrganicaCamaraMunicipalRJ1720(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1720.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'EmendaInt'
    tipo_lei = 'projetos de emenda a lei organica'
    header = ['projeto', 'ementa', 'data_publicacao', 'autor']


class ProjetosDeLeiCamaraMunicipalRJ1720(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1720.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'LeiInt'
    tipo_lei = 'projetos de lei'
    header = ['projeto', 'ementa', 'data_publicacao', 'autor']


class ProjetosDeLeiComplementarCamaraMunicipalRJ1720(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1720.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'LeiCompInt'
    tipo_lei = 'projetos de lei complementar'
    header = ['projeto', 'ementa', 'data_publicacao', 'autor']


class ProjetosDeDecretoCamaraMunicipalRJ1720(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1720.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'DecretoInt'
    tipo_lei = 'projetos de decreto'
    header = ['projeto', 'ementa', 'data_publicacao', 'autor']


class ProjetosResolucaoCamaraMunicipalRJ1720(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1720.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'
		
    tipo = 'ResolucaoInt'
    tipo_lei = 'projetos de resolução'
    header = ['projeto', 'ementa', 'data_publicacao', 'autor']


class IndicacoesCamaraMunicipalRJ1720(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1720.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'
		
    tipo = 'IndInt'
    tipo_lei = 'indicacoes'
    header = ['indicacao', 'ementa', 'data_publicacao', 'autor']


class MocoesCamaraMunicipalRJ1720(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1720.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'
		
    tipo = 'mocaoInt'
    tipo_lei = 'moções'
    header = ['mocao', 'ementa', 'data_publicacao', 'autor']


class RequerimentoInformacaoCamaraMunicipalRJ1720(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1720.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'
		
    tipo = 'ReqInfInt'
    tipo_lei = 'requerimento de informação'
    header = ['requerimento', 'ementa', 'data_publicacao', 'autor']


class RequerimentoCamaraMunicipalRJ1720(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1720.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'
		
    tipo = 'ReqInt'
    tipo_lei = 'requerimento'
    header = ['requerimento', 'ementa', 'data_publicacao', 'autor']


class OficioCamaraMunicipalRJ1720(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1720.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000&Expand=1'
		
    tipo = 'OficioInt'
    tipo_lei = 'oficio'
    header = ['oficio', 'ementa', 'data_publicacao', 'autor']


class OficioDenunciaCamaraMunicipalRJ1720(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1720.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000&Expand=2'
		
    tipo = 'OficioInt'
    tipo_lei = 'oficio denuncia'
    header = ['oficio', 'ementa', 'data_publicacao', 'autor']


class OficioOutrosCamaraMunicipalRJ1720(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1720.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000&Expand=3'
		
    tipo = 'OficioInt'
    tipo_lei = 'oficio outros'
    header = ['oficio', 'ementa', 'data_publicacao', 'autor']


class OficioEditalCamaraMunicipalRJ1720(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1720.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000&Expand=4'
		
    tipo = 'OficioInt'
    tipo_lei = 'oficio edital'
    header = ['oficio', 'ementa', 'data_publicacao', 'autor']


class OficioQuestaoOrdemCamaraMunicipalRJ1720(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1720.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000&Expand=5'
		
    tipo = 'OficioInt'
    tipo_lei = 'oficio questão de ordem'
    header = ['oficio', 'ementa', 'data_publicacao', 'autor']


class OficioParecerNormativoCJRCamaraMunicipalRJ1720(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1720.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000&Expand=6'
		
    tipo = 'OficioInt'
    tipo_lei = 'oficio parecer normativo cjr'
    header = ['oficio', 'ementa', 'data_publicacao', 'autor']


class OficioRecursoCamaraMunicipalRJ1720(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1720.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000&Expand=7'
		
    tipo = 'OficioInt'
    tipo_lei = 'oficio recurso'
    header = ['oficio', 'ementa', 'data_publicacao', 'autor']


class OficioRepresentacaoCamaraMunicipalRJ1720(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1720.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000&Expand=8'
		
    tipo = 'OficioInt'
    tipo_lei = 'oficio representação'
    header = ['oficio', 'ementa', 'data_publicacao', 'autor']


# Projetos de Lei Camara 2013-2016
class ProjetosDeEmendasLeiOrganicaCamaraMunicipalRJ1316(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1316.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'EmendaInt'
    tipo_lei = 'projetos de emenda a lei organica'
    header = ['lei', 'ementa', 'data_publicacao', 'autor']


class ProjetosDeLeiCamaraMunicipalRJ1316(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1316.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'LeiInt'
    tipo_lei = 'projetos de lei'
    header = ['lei', 'ementa', 'data_publicacao', 'autor']


class ProjetosDeLeiComplementarCamaraMunicipalRJ1316(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1316.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'LeiCompInt'
    tipo_lei = 'projetos de lei complementar'
    header = ['lei', 'ementa', 'data_publicacao', 'autor']


class ProjetosDeDecretoCamaraMunicipalRJ1316(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro1316.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'DecretoInt'
    tipo_lei = 'projetos de decreto'
    header = ['lei', 'ementa', 'data_publicacao', 'autor']


# Projetos de Lei Camara 2009-2012
class ProjetosDeEmendasLeiOrganicaCamaraMunicipalRJ0912(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro0711.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'EmendaInt'
    tipo_lei = 'projetos de emenda a lei organica'
    header = ['lei', 'ementa', 'data_publicacao', 'autor']


class ProjetosDeLeiCamaraMunicipalRJ0912(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro0711.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'LeiInt'
    tipo_lei = 'projetos de lei'
    header = ['lei', 'ementa', 'data_publicacao', 'autor']


class ProjetosDeLeiComplementarCamaraMunicipalRJ0912(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro0711.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'LeiCompInt'
    tipo_lei = 'projetos de lei complementar'
    header = ['lei', 'ementa', 'data_publicacao', 'autor']


class ProjetosDeDecretoCamaraMunicipalRJ0912(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/scpro0711.nsf/Internet/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'DecretoInt'
    tipo_lei = 'projetos de decreto'
    header = ['lei', 'ementa', 'data_publicacao', 'autor']
