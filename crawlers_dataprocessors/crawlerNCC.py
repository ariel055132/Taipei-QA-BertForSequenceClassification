import requests
import pandas as pd
from bs4 import BeautifulSoup

question = []
department = ['國家通訊傳播委員會'] * 282

for page_num in range(0, 15, 1):
    url = "https://www.ncc.gov.tw/Chinese/faq.aspx?is_history=0&faq_code=0&keyword=&pages=" + str(page_num)
    r = requests.get(url)
    html_soup = BeautifulSoup(r.text, 'html.parser')

    div_list_clearfix = html_soup.find_all("div", class_="list clearfix")
    for a in div_list_clearfix:
        for data in a.find_all("div", class_="subject"):
            question.append(data.getText())
            print(data.getText())

print(len(question))

result = pd.DataFrame(zip(department, question), columns=["部門", "問題"])
result.to_csv("20220529_國家通訊傳播委員會整理好QA.csv", sep=" ",index=False)
