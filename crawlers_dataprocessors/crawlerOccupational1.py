import requests
import pandas as pd
from bs4 import BeautifulSoup

# https://www.wda.gov.tw/News.aspx?n=5B7D022B7B2A81BA&sms=A08B1EA8119FA444&_Query=0a842c5b-6156-4786-994a-a1612d2c2f65&rn=588589093
# https://www.wda.gov.tw/News.aspx?n=5B7D022B7B2A81BA&sms=A08B1EA8119FA444&_Query=0a842c5b-6156-4786-994a-a1612d2c2f65& page=2&PageSize=20
# https://www.wda.gov.tw/News.aspx?n=5B7D022B7B2A81BA&sms=A08B1EA8119FA444&_Query=0a842c5b-6156-4786-994a-a1612d2c2f65& page=3&PageSize=20
# https://www.wda.gov.tw/News.aspx?n=5B7D022B7B2A81BA&sms=A08B1EA8119FA444&_Query=0a842c5b-6156-4786-994a-a1612d2c2f65& page=4&PageSize=20
# https://www.wda.gov.tw/News.aspx?n=5B7D022B7B2A81BA&sms=A08B1EA8119FA444&_Query=0a842c5b-6156-4786-994a-a1612d2c2f65& page=5&PageSize=20

url = "https://www.wda.gov.tw/News.aspx?n=5B7D022B7B2A81BA&sms=A08B1EA8119FA444&_Query=0a842c5b-6156-4786-994a-a1612d2c2f65&rn=588589093"
r = requests.get(url)
html_soup = BeautifulSoup(r.text, 'html.parser')
td = html_soup.find_all('td')


for data in td:
    span = data.find_all('span')
    print(span)
