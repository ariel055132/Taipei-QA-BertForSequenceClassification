# TaipeiGOVDepartment-QA-BertForSequenceClassification
使用BertForSequenceClassification訓練政府部門問答資料集

大部分程式架構的參考來源 : [p208p2002/taipei-QA-BERT](https://github.com/p208p2002/taipei-QA-BERT)

貢獻 : 
- 修改了[p208p2002/taipei-QA-BERT/preprocess_data.py](https://github.com/p208p2002/taipei-QA-BERT/blob/master/preprocess_data.py)中關於input_masks的錯誤。
- 新增了其他政府部門的QA資料集，以及相關的crawlers
- 使用了ALBERT來進行Fine-tune

## 檔案說明
### Data
- data_split.py : 將Taipei_QA_new.txt切割成train、test和valid資料的程式
- core.py : 處理dataset和label的轉換
- preprocess_data.py : BertForSequenceClassification的前處理
- train.py : BertForSequenceClassification的訓練
- predict.py : BertForSequenceClassification的預測
- requestment.txt : 紀錄需要安裝的環境
## 使用說明
### train的順序
```
python data_split.py    # 如果已經存在train、test和valid資料，就可以跳過這步驟
python train.py         # 如果想用訓練好的model可以去release下載，並將資料放入trained_model內，就可以跳過這步驟
```
### Demo
```
python predict.py
```
## 環境需求
- python 3.6+
- pytorch 1.3+
- transformers 2.2+
- CUDA Version: 10.0
- BeautifulSoup
- Selenium
- (Optional) Colab / Colab pro

## 20240414 New Update
* 使用了新的電腦及環境進行訓練
* python 3.10+
* pytorch 2.2.2
* transformers 4.39.3
* CUDA Version: 12.1
* Difference: Training 的時候並不會儲存成pytorch.bin，存成model.safetensors，須在predict.py修改model的來源，如下所示
```
Before:
model = bert_class.from_pretrained('trained_model/pytorch_model.bin', from_tf=bool('.ckpt' in 'bert-base-chinese'), config=config)
After:
model = bert_class.from_pretrained('trained_model/model.safetensors', from_tf=bool('.ckpt' in 'bert-base-chinese'), config=config)
```
* 若遇到 RuntimeError: No CUDA GPUs are available，可使用nvidia-smi -L 來檢查GPU的編號，並修改train.py的GPU來源
```
# 设置使用的GPU用法來源:https://www.cnblogs.com/darkknightzh/p/6591923.html
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
```