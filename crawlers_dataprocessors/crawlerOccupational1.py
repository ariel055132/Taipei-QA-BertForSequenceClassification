import requests
import pandas as pd
from bs4 import BeautifulSoup

# https://www.wda.gov.tw/News.aspx?n=5B7D022B7B2A81BA&sms=A08B1EA8119FA444&_Query=0a842c5b-6156-4786-994a-a1612d2c2f65&rn=588589093

# https://www.wda.gov.tw/News.aspx?n=5B7D022B7B2A81BA&sms=A08B1EA8119FA444&_Query=0a842c5b-6156-4786-994a-a1612d2c2f65& page=1&PageSize=20
# https://www.wda.gov.tw/News.aspx?n=5B7D022B7B2A81BA&sms=A08B1EA8119FA444&_Query=0a842c5b-6156-4786-994a-a1612d2c2f65& page=2&PageSize=20
# https://www.wda.gov.tw/News.aspx?n=5B7D022B7B2A81BA&sms=A08B1EA8119FA444&_Query=0a842c5b-6156-4786-994a-a1612d2c2f65& page=3&PageSize=20
# https://www.wda.gov.tw/News.aspx?n=5B7D022B7B2A81BA&sms=A08B1EA8119FA444&_Query=0a842c5b-6156-4786-994a-a1612d2c2f65& page=4&PageSize=20
# https://www.wda.gov.tw/News.aspx?n=5B7D022B7B2A81BA&sms=A08B1EA8119FA444&_Query=0a842c5b-6156-4786-994a-a1612d2c2f65& page=5&PageSize=20

department = ['勞動部勞動力發展署'] * 84
question = []

for page_num in range(1,6,1):
    url = "https://www.wda.gov.tw/News.aspx?n=5B7D022B7B2A81BA&sms=A08B1EA8119FA444&_Query=0a842c5b-6156-4786-994a-a1612d2c2f65&page=" + str(page_num) + "&PageSize=20"
    r = requests.get(url)
    html_soup = BeautifulSoup(r.text, 'html.parser')
    container = html_soup.find_all('div', class_="area-table rwd-straight")

    for data in container:
        for tag in data.find_all('a'):
            question.append(tag.text)
            print(tag.text)

print(len(question))
result = pd.DataFrame(zip(department, question), columns=["部門", "問題"])
result.to_csv("20220529_勞動部勞動力發展署整理好QA.csv", sep=" ",index=False)