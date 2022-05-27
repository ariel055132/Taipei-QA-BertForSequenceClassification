import requests
import pandas as pd
from bs4 import BeautifulSoup

question = []
department = ["勞動部職業安全衛生署"] * 196

for page_no in range(1, 21, 1):
    url = "https://www.osha.gov.tw/1106/1196/10101/?Page=" + str(page_no) + "&PageSize=10"
    r = requests.get(url)
    html_soup = BeautifulSoup(r.text, 'html.parser')
    qlist = html_soup.find_all("tbody")

    for data in qlist:
        td = data.find_all('td')
        for data1 in td:
            for a in data1.find_all('a'):
                question.append(a.text)
                print(a.text)

result = pd.DataFrame(zip(department, question), columns=["部門", "問題"])
print(result)
result.to_csv("20220526_勞動部職業安全衛生署整理好QA.csv", sep=" ",index=False)