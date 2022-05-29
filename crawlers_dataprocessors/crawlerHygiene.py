from selenium import webdriver
import requests
import pandas as pd
from bs4 import BeautifulSoup

question = []
department = ['衛生福利部疾病管制署'] * 366

url = "https://www.cdc.gov.tw/Category/QAPage/B5ttQxRgFUZlRFPS1dRliw"
driver = webdriver.Chrome()
driver.get(url)
element = driver.find_element_by_xpath('//*[@id="toggle_all"]/a')
element.click()

html_soup = BeautifulSoup(driver.page_source, 'html.parser')
word = html_soup.find_all('span', class_="word")
strong = html_soup.find_all('strong')
b = html_soup.find_all('b')

for q in word:
    question.append(q.getText())
    print(q.getText())

for q in b:
    question.append(q.getText())
    print(q.getText())

for q in strong:
    question.append(q.getText())
    print(q.getText())

print(len(question))
result = pd.DataFrame(zip(department, question), columns=["部門", "問題"])
result.to_csv("20220525_衛生福利部疾病管制署整理好QA.csv", sep=" ",index=False)