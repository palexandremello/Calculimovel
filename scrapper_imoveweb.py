import requests
from bs4 import BeautifulSoup

source_code = requests.get('https://www.imovelweb.com.br/propriedades/otimo-apartamento-em-regiao-nobre-2942680787.html')

soup = BeautifulSoup(source_code.content, 'lxml')

tags = soup.find('li', attrs={"class":"icon-feature"})


print("Área total do imóvel %s " % (tags.b.text))