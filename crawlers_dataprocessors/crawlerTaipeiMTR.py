import requests
from bs4 import BeautifulSoup

url = "https://www.dorts.gov.taipei/News.aspx?n=2A66A485FACB0D5B&sms=87415A8B9CE81B16&page=1&PageSize=200"
r = requests.get(url)
html_soup = BeautifulSoup(r.text, 'html.parser')
container = html_soup.find_all('div', class_="area-table rwd-straight")
for data in container:
    print(data)