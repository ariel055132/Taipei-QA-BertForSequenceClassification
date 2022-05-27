import requests
import pandas as pd
from bs4 import BeautifulSoup

# (3)"與個人信用評分相關問題	", 2017/9/8, https://www.jcic.org.tw/main_ch/List.aspx?uid=90&pid=90  可能有問題
# 與企業信用評分相關問題,2015/12/16, https://www.jcic.org.tw/main_ch/List.aspx?uid=91&pid=91  可能有問題
# 信用資料更正, 2018/11/7, https://www.jcic.org.tw/main_ch/List.aspx?uid=95&pid=95  可能有問題

webpages = ["https://www.jcic.org.tw/main_ch/List.aspx?uid=90&pid=90", "https://www.jcic.org.tw/main_ch/List.aspx?uid=91&pid=91", "https://www.jcic.org.tw/main_ch/List.aspx?uid=95&pid=95"]

url = "https://www.jcic.org.tw/main_ch/List.aspx?uid=90&pid=90"
r = requests.get(url)
html_soup = BeautifulSoup(r.text, 'html.parser')
word = html_soup.find_all('span', style_="font-size: 1.25em;")
page_word = html_soup.find_all('div', class_="page_word")
for data in page_word:
    #data1 = data.find('strong')

    data1 = data.find_all('span', attrs={'style': 'font-size: 1.25em;'})
    for data2 in data1:
        data3 = data1.find('strong')
        print(data3)
