import xml.etree.ElementTree as et
import pandas as pd

data = []
path = "20220523_內政部常見QA.xml"

for (ev, el) in et.iterparse(path):
    inner = []

    if el.tag == 'QAITEM':
        for name, value in el.items():
            inner.append([el.tag+'-'+name, str(value).replace('\n','').replace(' ','')])
        for i in el:
            if str(i.text) != 'None':
                #inner.append([i.tag, str(i.text).replace('\n','').replace(' ','')])
                inner.append([str(i.text).replace('\n','').replace(' ','')])

            for name, value in i.items():
                inner.append([i.tag+'-'+name, str(value).replace('\n','').replace(' ','')])
        data.append(inner)

print(data[0])

dept, ques = [], []
for i in range(len(data)):
    #department = ''.join(data[i][1] + data[i][2])
    department = ''.join(data[i][1])
    department = "內政部" + department
    dept.append(department)
    question = ''.join(data[i][3])
    ques.append(question)

result = pd.DataFrame(zip(dept, ques), columns=["部門", "問題"])
print(result)
result.to_csv("20220525_內政部常見整理好QA_v3.csv", sep=" ",index=False)

