import requests
import pandas as pd
from bs4 import BeautifulSoup

# https://www.blf.gov.tw/8812/9019/9022/?Model.PagingList.CurrentPageNumber=1
# https://www.blf.gov.tw/8812/9019/9022/?Model.PagingList.CurrentPageNumber=2

department = ['勞動部勞動基金運用局'] * 21
question = []

for page_num in range(1,3,1):
    url = "https://www.blf.gov.tw/8812/9019/9022/?Model.PagingList.CurrentPageNumber=" + str(page_num)
    r = requests.get(url)
    html_soup = BeautifulSoup(r.text, 'html.parser')
    container = html_soup.find_all('section', class_="listTb")
    for data in container:
        for tag in data.find_all('a'):
            question.append(tag.text)
            print(tag.text)

result = pd.DataFrame(zip(department, question), columns=["部門", "問題"])
result.to_csv("20220529_勞動部勞動基金運用局整理好QA.csv", sep=" ",index=False)