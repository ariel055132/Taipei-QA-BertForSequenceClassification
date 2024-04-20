# -*-coding:UTF-8 -*-

# 存檔
def save_data(FileName, data_list):
    fp = open(FileName, "w", encoding='utf-8')
    for data in data_list:
        fp.write(data)
        fp.write('\n')
    fp.close()

# 資料分割，目前只有兩個類別
def data_split():
    # 20220531_QA_v4.txt
    # 20220602_FinalDataset.txt
    morality_type = "fairness"
    with open(f'20240420_original_data_preprocess/20240420_{morality_type}_original_data.csv','r',encoding='utf-8') as f:
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
            if count % 10 == 1 or count % 10 == 3:
                test_data.append(qa_pair)
            elif count % 10 == 5 or count % 10 == 7 or count % 10 == 9:
                valid_data.append(qa_pair)
            else:
                train_data.append(qa_pair)
            before = now
        except:
            continue

    save_data(f"20240420_{morality_type}_trained_models/20240420_{morality_type}_train_data.txt", train_data)
    save_data(f"20240420_{morality_type}_trained_models/20240420_{morality_type}_test_data.txt", test_data)
    save_data(f"20240420_{morality_type}_trained_models/20240420_{morality_type}_valid_data.txt", valid_data)

if __name__ == "__main__":
   data_split()