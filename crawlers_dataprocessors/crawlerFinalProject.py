import requests
from bs4 import BeautifulSoup

url = "https://www.mol.gov.tw/1607/28162/28652/28656/28660/28662/"
r = requests.get(url)
html_soup = BeautifulSoup(r.text, 'html.parser')
#print(html_soup.prettify())
question = []
container = html_soup.find_all('div', class_="accordionblock")
for ele in container:
    answer = ele.find('ul', class_= "answer_list")
    info = answer.find_all('li')
    for data in info:
        print(data.a.text)





