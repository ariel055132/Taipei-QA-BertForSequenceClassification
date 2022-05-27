import requests
import pandas as pd
from bs4 import BeautifulSoup

# (6)信用資訊的重要性, 2015/10/11, https://www.jcic.org.tw/main_ch/docDetail.aspx?uid=86&pid=86&docid=72
# (10)信用資料的查詢, 2020/1/30, https://www.jcic.org.tw/main_ch/docDetail.aspx?uid=87&pid=87&docid=411
# (6)與債協用清冊相關問題, 2015/12/15, https://www.jcic.org.tw/main_ch/docDetail.aspx?uid=88&pid=88&docid=77
# (7)與展延用清冊清冊相關問題,2016/10/4, https://www.jcic.org.tw/main_ch/docDetail.aspx?uid=89&pid=89&docid=78
# "與個人信用評分相關問題	", 2017/9/8, https://www.jcic.org.tw/main_ch/List.aspx?uid=90&pid=90  可能有問題
# 與企業信用評分相關問題,2015/12/16, https://www.jcic.org.tw/main_ch/List.aspx?uid=91&pid=91  可能有問題
# 信用資料更正, 2018/11/7, https://www.jcic.org.tw/main_ch/List.aspx?uid=95&pid=95  可能有問題
# (1)金融機構查詢信用資訊說明--符合法令規定, 2015/10/15 , https://www.jcic.org.tw/main_ch/docDetail.aspx?uid=76&pid=76&docid=82
# (8)信用資料的揭露, 2016/1/8, https://www.jcic.org.tw/main_ch/docDetail.aspx?uid=78&pid=78&docid=84

webpages = ["https://www.jcic.org.tw/main_ch/docDetail.aspx?uid=86&pid=86&docid=72",
            "https://www.jcic.org.tw/main_ch/docDetail.aspx?uid=87&pid=87&docid=411",
            "https://www.jcic.org.tw/main_ch/docDetail.aspx?uid=88&pid=88&docid=77",
            "https://www.jcic.org.tw/main_ch/docDetail.aspx?uid=89&pid=89&docid=78",
            "https://www.jcic.org.tw/main_ch/docDetail.aspx?uid=76&pid=76&docid=82",
            "https://www.jcic.org.tw/main_ch/docDetail.aspx?uid=78&pid=78&docid=84"]

department = ["財團法人金融聯合徵信中心"] * 38
question = []

for url in webpages:
    r = requests.get(url)

    html_soup = BeautifulSoup(r.text, 'html.parser')
    page_word = html_soup.find_all('ul', class_="info_disc_q")

    for data in page_word:
        data1 = data.find('span', class_="txt")
        print(data1.text)
        question.append(data1.text)

print(len(question))
result = pd.DataFrame(zip(department, question), columns=["部門", "問題"])
result.to_csv("20220525_財團法人金融聯合徵信中心整理好QA.csv", sep=" ",index=False)
