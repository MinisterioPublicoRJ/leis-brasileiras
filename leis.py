import csv
import re
import requests as req

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

from commons import striphtml
from urls import (urls_decretos_planalto,
                  urls_leis_ordinarias_planalto,
                  urls_medidas_provisorias,
                  urls_projetos_leis_casa_civil,
                  urls_projetos_leis_complementares_casa_civil,
                  urls_projetos_leis_congresso_casa_civil)


class Planalto:
    base_url = "http://www4.planalto.gov.br/legislacao/portal-legis/"\
               "legislacao-1/"
    origin = 'Planalto'

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

    def extract_info(self, year, url):
        download_desc = 'Baixando {tipo} {origin} ({ano})'.format(
            tipo=self.tipo_lei,
            origin=self.origin,
            ano=year
        )
        with open(self.file_destination, 'w', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=self.header,
                delimiter=";",
                quotechar='"'
            )
            writer.writeheader()

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
        for year, url in self.urls.items():
            self.extract_info(year, url)

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


class DecretosLeisPlanato(Planalto):
    def __init__(self, file_destination):
        super().__init__()
        self.file_destination = file_destination
        self.tipo_lei = 'decretos-leis'
        self.urls = {'1937-1946': 'decretos-leis/1937-a-1946-decretos-leis-1',
                     '1965-1988': 'decretos-leis/1965-a-1988-decretos-leis'}
        self.header = ['lei', 'ementa', 'ano', 'inteiro_teor']


class CasaCivil:
    base_url = 'http://www.casacivil.gov.br/Secretaria-Executiva/'\
               'Diretoria%20de%20Assuntos%20Legislativos/projetos-de-lei/'
    origin = 'Casa Civil'

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
        numero_lei = re.search(r'(\d\.|\d+)\d+\/\d+', numero_lei)
        info = {'lei': numero_lei}
        info['ementa'] = tds[1].text
        info['ano'] = year
        info['inteiro_teor'] = inteiro_teor
        info['motivacao'] = motivacao

        if len(tds) == 3:
            info['situacao'] = tds[2].text

        return info


class ProjetosCasaCivil(CasaCivil, Planalto):
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


class ProjetosLeisComplementaresCasaCivil(CasaCivil, Planalto):
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


class ProjetosLeisCongressoCasaCivil(CasaCivil, Planalto):
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


class Alerj:

    dns = "http://alerjln1.alerj.rj.gov.br"
    base_url = dns + "/contlei.nsf/{tipo}?OpenForm&Start={start}&Count=1000"
    header = ['lei', 'ano', 'autor', 'ementa']

    def __init__(self, file_destination):
        self.file_destination = file_destination

    def visit_url(self, start):
        url = self.base_url.format(tipo=self.tipo, start=start)
        common_page = req.get(url)
        soup = BeautifulSoup(common_page.content, features='lxml')
        return soup.find_all('tr')

    def parse_metadata(self, row):
        columns = row.find_all('td')
        return dict(
            zip(
                self.header,
                [c.text for c in columns if c.text and c.text != '*']
            )
        )

    def parse_full_content(self, row):
        # There may be links pointing to the form, which are not wanted
        links = [l for l in row.find_all('a') if 'OpenDocument' in l['href']]
        full_content_link = self.dns + links[0]['href']
        resp = req.get(full_content_link)
        soup = BeautifulSoup(resp.content, features='lxml')
        body = soup.find('body')
        strip_body = striphtml(body.text)

        # Documents come with noise at the end, this removes that
        end_doc_i = strip_body.find('HTML5 Canvas')
        return strip_body[:end_doc_i]

    def download(self):
        with open(self.file_destination, 'w', newline='') as csvfile:
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


class DecretosCamaraMunicipalRJ(Alerj):
    orgao = 'Camara Municipal'
    dns = 'http://mail.camara.rj.gov.br'
    base_url = dns + '/APL/Legislativos/contlei.nsf/'\
        '{tipo}?OpenForm&Start={start}&Count=1000'

    tipo = 'DecretoInt'
    tipo_lei = 'decretos'
    header = ['lei', 'ano', 'ementa', 'autor']


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
    tipo_lei = 'leis ordinárias'
    header = ['lei', 'ano', 'status', 'ementa', 'autor']
