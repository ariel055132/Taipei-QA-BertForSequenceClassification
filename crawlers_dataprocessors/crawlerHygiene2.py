import requests
import pandas as pd
from bs4 import BeautifulSoup

question = []
department = ['衛生福利部社會及家庭署'] * 54
urls = ["https://www.sfaa.gov.tw/SFAA/Pages/List.aspx?nodeid=99&idx=0", "https://www.sfaa.gov.tw/SFAA/Pages/List.aspx?nodeid=99&idx=1", "https://www.sfaa.gov.tw/SFAA/Pages/List.aspx?nodeid=99&idx=2",
        "https://www.sfaa.gov.tw/SFAA/Pages/List.aspx?nodeid=99&idx=3", "https://www.sfaa.gov.tw/SFAA/Pages/List.aspx?nodeid=99&idx=4", "https://www.sfaa.gov.tw/SFAA/Pages/List.aspx?nodeid=100",
        "https://www.sfaa.gov.tw/SFAA/Pages/List.aspx?nodeid=101", "https://www.sfaa.gov.tw/SFAA/Pages/List.aspx?nodeid=102"]

for url in urls:
    r = requests.get(url)
    html_soup = BeautifulSoup(r.text, 'html.parser')
    tbody = html_soup.find_all('tbody')

    for q in tbody:
        for a in q.find_all('a'):
            question.append(a.text)
            print(a.text)

print(len(question))
result = pd.DataFrame(zip(department, question), columns=["部門", "問題"])
result.to_csv("20220529_衛生福利部社會及家庭署整理好QA.csv", sep=" ",index=False)