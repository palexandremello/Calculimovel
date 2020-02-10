import requests
from bs4 import BeautifulSoup

def parse_scrapper_data(html_to_scrapper):
    pass

source_code = requests.get('https://www.imovelweb.com.br/propriedades/apartamento-para-aluguel-bairro-alto-3-quartos-70-2948108876.html')

soup = BeautifulSoup(source_code.content, 'lxml')

## find proprety's address : h2 and class: title-location
## variables from proprety : li and class: icon-feature
tags = soup.findAll('li', attrs={"class":"icon-feature"})



print("Área total do imóvel %s " % (tags[0].b.text))

