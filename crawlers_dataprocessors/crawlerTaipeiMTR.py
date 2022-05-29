import requests
from bs4 import BeautifulSoup
import pandas as pd

department = ["臺北市政府捷運工程局"] * 157
question = []

url = "https://www.dorts.gov.taipei/News.aspx?n=2A66A485FACB0D5B&sms=87415A8B9CE81B16&page=1&PageSize=200"
r = requests.get(url)
html_soup = BeautifulSoup(r.text, 'html.parser')
container = html_soup.find_all('div', class_="area-table rwd-straight")
#container = html_soup.find_all(name= 'table', attrs={"id": "table_0"})
for data in container:
    for tag in data.find_all('a'):
        question.append(tag.text)
        print(tag.text)

result = pd.DataFrame(zip(department, question), columns=["部門", "問題"])
result.to_csv("20220529_臺北市政府捷運工程局整理好QA.csv", sep=" ",index=False)