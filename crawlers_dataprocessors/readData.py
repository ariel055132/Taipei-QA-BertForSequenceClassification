import pandas as pd

filename = "20220523_經濟部智慧財產局專利QA.csv"
question = []
department = ['經濟部智慧財產局'] * 671
data_df = pd.read_csv(filename, encoding='utf-8')
#print(data_df['標題'])
question = data_df['題目'].tolist()

print(question)
print(len(question))
result = pd.DataFrame(zip(department, question), columns=["部門", "問題"])
result.to_csv("20220523_經濟部智慧財產局專利整理好QA.csv", sep=" ",index=False)
