# -*-coding:UTF-8 -*-

# 存檔
def save_data(FileName, data_list):
    fp = open(FileName, "w", encoding='utf-8')
    for data in data_list:
        fp.write(data)
        fp.write('\n')
    fp.close()

# 資料分割，因為有149個類別，所以為了公正，要確保切割時，train_data要有每個類別的資料
def data_split():
    # 20220531_QA_v4.txt
    # 20220602_FinalDataset.txt
    with open('Binary/20240319_BinaryPredAll.csv','r',encoding='utf-8') as f:
        data = f.read()
    qa_pairs = data.split("\n")

    before = ""
    now = ""
    count = 0
    train_data = []
    test_data = []
    valid_data = []
    for qa_pair in qa_pairs:
        try:
            a,q = qa_pair.split()
            now = a

            if before != now:
                count = 0
            count += 1
            '''
            if count % 5 == 3:
                test_data.append(qa_pair)
            elif count % 5 == 4:
                valid_data.append(qa_pair)
            else:
                train_data.append(qa_pair)
            '''
            if count % 10 == 0 or count % 10 == 2:
                test_data.append(qa_pair)
            elif count % 10 == 4 or count % 10 == 6 or count % 10 == 8:
                valid_data.append(qa_pair)
            else:
                train_data.append(qa_pair)
            before = now
        except:
            continue

    save_data("Binary/20240319_HKU_train_data.txt", train_data)
    save_data("Binary/20240319_HKU_test_data.txt", test_data)
    save_data("Binary/20240319_HKU_valid_data.txt", valid_data)

if __name__ == "__main__":
   data_split()