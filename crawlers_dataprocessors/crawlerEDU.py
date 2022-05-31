import requests
import pandas as pd
from bs4 import BeautifulSoup

question = []
department = ['教育部'] * 154

for page_num in range(1, 9, 1):
    url = "https://www.edu.tw/News.aspx?n=BA5E856472F10901&page=" + str(page_num) + "&PageSize=20"
    r = requests.get(url)
    html_soup = BeautifulSoup(r.text, 'html.parser')
    table_csstr = html_soup.find_all("table", class_="css_tr")

    for text in table_csstr:
        for tr in text.find_all('tr'):
            for a in tr.find_all('a'):
                question.append(a.getText())
                print(a.getText())

result = pd.DataFrame(zip(department, question), columns=["部門", "問題"])
result.to_csv("20220531_教育部常見問答整理好QA.csv", sep=" ",index=False)