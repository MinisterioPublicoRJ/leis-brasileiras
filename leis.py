import csv
import requests as req

from bs4 import BeautifulSoup
from decouple import config
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from tqdm import tqdm

from commons import striphtml
from urls import urls_decretos_planalto


class Planalto:
    base_url = "http://www4.planalto.gov.br/legislacao/portal-legis/"\
               "legislacao-1/"

    def __init__(self):
        self.driver = Firefox(executable_path=config('DRIVER_PATH'))

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
            inteiro_teor = striphtml(self.get_content(link))
        except NoSuchElementException:
            inteiro_teor = ''

        info = {k: v.text for k, v in zip(('lei', 'ementa'), tds)}
        info['ano'] = year
        info['inteiro_teor'] = inteiro_teor
        return info

    def dowload(self, year, url):
        download_desc = 'Baixando {tipo} {ano}'.format(
            tipo=self.tipo_lei,
            ano=year
        )
        with open(self.file_destination, 'w', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames={'lei', 'ementa', 'ano', 'inteiro_teor'},
                delimiter=";",
                quotechar='"'
            )
            writer.writeheader()

            self.driver.get(self.base_url + url)
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.presence_of_element_located(
                (By.TAG_NAME, 'table')
                )
            )
            table = self.driver.find_element_by_tag_name('table')
            rows = table.find_elements_by_tag_name('tr')

            # rows[1:] to skip table header
            for row in tqdm(rows[1:], desc=download_desc):
                tds = row.find_elements_by_tag_name('td')
                row_info = self.get_row_info(tds, year)
                writer.writerow(row_info)


class DecretosPlanalto(Planalto):
    def __init__(self, file_destination):
        super().__init__()
        self.file_destination = file_destination
        self.tipo_lei = 'decretos'
        self.urls = urls_decretos_planalto

    def start(self):
        for year, url in self.urls.items():
            self.dowload(year, url)
