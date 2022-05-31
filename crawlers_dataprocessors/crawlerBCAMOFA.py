import requests
import pandas as pd
from bs4 import BeautifulSoup

question = []
department = ['外交部領事事務局'] * 149

urls = ["https://www.boca.gov.tw/lp-35-1-1-20.html", "https://www.boca.gov.tw/lp-35-1-2-20.html",
        "https://www.boca.gov.tw/lp-35-1-3-20.html", "https://www.boca.gov.tw/lp-35-1-4-20.html",
        "https://www.boca.gov.tw/lp-215-1-1-20.html", "https://www.boca.gov.tw/lp-215-1-2-20.html",
        "https://www.boca.gov.tw/lp-215-1-3-20.html", "https://www.boca.gov.tw/lp-43-1-1-20.html",
        "https://www.boca.gov.tw/lp-43-1-2-20.html"]

for url in urls:
    r = requests.get(url)
    html_soup = BeautifulSoup(r.text, 'html.parser')
    class01 = html_soup.find_all("section", class_="list01")
    for text in class01:
        for a in text.find_all('a'):
            question.append(a.getText())
            print(a.getText())

print(len(question))
result = pd.DataFrame(zip(department, question), columns=["部門", "問題"])
result.to_csv("20220531_外交部領事事務局常見問答整理好QA.csv", sep=" ",index=False)