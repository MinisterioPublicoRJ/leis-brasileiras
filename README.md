# Leis Brasileiras

Os scripts desde repositório buscam automatizar o processo de busca e download das leis
hospedadas em sites do Governo. Até o momento os seguintes documentos são baixados:

## Planalto
http://www4.planalto.gov.br/legislacao/

  - Decretos
  - Decretos Leis
  - Leis Ordinárias
  - Leis Complementares
  - Leis Delegadas
  - Medidas Provisórias

## Casa Civil
http://www.casacivil.gov.br/Secretaria-Executiva/Diretoria%20de%20Assuntos%20Legislativos/projetos-de-lei

   - Projetos de Lei
   - Projetos de Lei Complementar
   - Projetos de Lei Congresso Nacional


## Alerj
http://www3.alerj.rj.gov.br/lotus_notes/default.asp?id=144

  - Decretos
  - Leis Ordinárias
  - Leis Complementares

## Câmara Municipal do Rio de Janeiro
http://www.camara.rj.gov.br/

  - Decretos
  - Leis Ordinárias
  - Leis Complementares


As leis são salvas em um arquivo .CSV com separação das colunas por '';'' e com nome definido no momento da consulta;

### Exemplo de Uso
##### Baixando os Decretos do site do Planalto: 
```python
from leis import DecretosPlanalto

planalto = DecretosPlanalto('/caminho/para/arquivo.csv')
planalto.download()
```

### Instalando dependências

```bash
pip install -r requirements.txt
```

##### Obeservação:
Para baixar os documentos dos site do Planalto é necessário utilizar o programa
[Selenium](https://www.seleniumhq.org/) e utilizar o driver do navegador **Firefox**. O executável funciona em qualquer plataforma (Windows, Mac e Linux) e pode ser baixado a partir deste [link](https://github.com/mozilla/geckodriver/releases).

### Configuração do Ambiente
É necessário criar um arquivo **settings.ini** com a variável que irá apontar para o 
**geckodriver** apresentado anteriormente.

```
[settings]
DRIVER_PATH=/caminho/completo/para/geckodriver
```

#### Estrutura do Projeto:
```bash
.
├── commons.py
├── geckodriver
├── leis.py
├── README.md
├── requirements.txt
├── settings.ini
└── urls.py
```