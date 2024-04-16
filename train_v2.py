# -*-coding:UTF-8 -*-
from preprocess_data import convert_data_to_feature
from core import makeDataset
from torch.utils.data import DataLoader
# For BERT Config
from transformers import BertConfig, BertForSequenceClassification, BertTokenizer, AdamW
# For ALBERT Config
from transformers import AlbertConfig, AlbertForSequenceClassification, AlbertTokenizer
# Evaluation Metrics
from sklearn.metrics import precision_score, recall_score, f1_score
import torch
import os
import torch.nn.functional as F     # 激励函数都在这

# 計算正確值，參考網站:https://zhuanlan.zhihu.com/p/57294358
def compute_accuracy(y_pred, y_target):
    _, y_pred_indices = y_pred.max(dim=1)
    n_correct = torch.eq(y_pred_indices, y_target).sum().item()
    return n_correct / len(y_pred_indices) * 100

# 計算Precision, Recall, F1-score
def compute_metrics(y_pred, y_target):
    # Extract the indices of the maximum values along dimension 1
    _, y_pred_indices = y_pred.max(dim=1)
    # Convert tensors to numpy arrays
    y_pred_np = y_pred_indices.cpu().numpy()
    y_target_np = y_target.cpu().numpy()
    # Compute the evaluation metrics
    precision = precision_score(y_target_np, y_pred_np)
    recall = recall_score(y_target_np, y_pred_np)
    f1 = f1_score(y_target_np, y_pred_np)
    return precision, recall, f1

# 動態調整學習率，參考網站:http://www.spytensor.com/index.php/archives/32/
def adjust_learning_rate(optimizer, epoch):
    """Sets the learning rate to the initial LR decayed by 10 every 30 epochs"""
    for param_group in optimizer.param_groups:
        param_group['lr'] = epoch

if __name__ == "__main__":
    bert_config, bert_class, bert_tokenizer = (BertConfig, BertForSequenceClassification, BertTokenizer)
    #albert_config, albert_class, albert_tokenizer = (AlbertConfig, AlbertForSequenceClassification, AlbertTokenizer)
# 设置使用的GPU用法來源:https://www.cnblogs.com/darkknightzh/p/6591923.html
    # RuntimeError: cuda runtime error (100) : no CUDA-capable device is detected at /pytorch/aten/src/
    # 0 --> Single Card
    # 1 --> Multiple Card
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    # set device，gpu用法來源:https://zhuanlan.zhihu.com/p/76604
    device = torch.device("cuda")

    train_data_feature = convert_data_to_feature('20240416_trained_models/20240319_HKU_train_data.txt')
    test_data_feature = convert_data_to_feature('20240416_trained_models/20240319_HKU_valid_data.txt')
    train_dataset = makeDataset(train_data_feature)
    test_dataset = makeDataset(test_data_feature)

    train_dataloader = DataLoader(train_dataset ,batch_size=8 ,shuffle=True)
    test_dataloader = DataLoader(test_dataset ,batch_size=8 ,shuffle=True)

    # voidful/albert_chinese_base --> 20220602_ALBERT
    #config = albert_config.from_pretrained('voidful/albert_chinese_base', num_labels = 60)
    #model = albert_class.from_pretrained('voidful/albert_chinese_base', from_tf=bool('.ckpt' in 'voidful/albert_chinese_base'), config=config)
    
    # voidful/albert_chinese_xlarge --> 20220602_ALBERT1
    #config = albert_config.from_pretrained('voidful/albert_chinese_xlarge', num_labels = 60)
    #model = albert_class.from_pretrained('voidful/albert_chinese_xlarge', from_tf=bool('.ckpt' in 'voidful/albert_chinese_xlarge'), config=config)

    # Finetuning model with BERT 
    config = bert_config.from_pretrained('bert-base-chinese',num_labels = 2)
    print(config)
    model = bert_class.from_pretrained('bert-base-chinese', from_tf=bool('.ckpt' in 'bert-base-chinese'), config=config)
    model.to(device)

    # Prepare optimizer and schedule (linear warmup and decay)
    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': 0.0},
        {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
        ]
    Learning_rate = 5e-6       # 学习率
    optimizer = AdamW(optimizer_grouped_parameters, lr=Learning_rate, eps=1e-8)

    for epoch in range(20): # 30
        # 訓練模式
        model.train()
        if epoch % 5 == 0 and epoch != 0:
            Learning_rate = Learning_rate * 0.5
            adjust_learning_rate(optimizer,Learning_rate)

        All_train_correct = 0.0
        AllTrainLoss = 0.0

        All_train_precision = 0.0
        All_train_recall = 0.0
        All_train_f1 = 0.0

        count = 0
        for batch_index, batch_dict in enumerate(train_dataloader):
            batch_dict = tuple(t.to(device) for t in batch_dict)
            #print(batch_dict)
            # print(batch_dict[0].shape)
            # print(batch_dict[3].shape)

            outputs = model(
                batch_dict[0],
                token_type_ids = batch_dict[1],
                attention_mask = batch_dict[2],
                labels = batch_dict[3]
                )
            loss, logits = outputs[:2]

            # 計算正確率
            train_correct = compute_accuracy(logits, batch_dict[3])      
            All_train_correct += train_correct
            AllTrainLoss += loss.item()

            # Precision, Recall, F1-score
            train_precision, train_recall, train_f1 = compute_metrics(logits, batch_dict[3])
            All_train_precision += train_precision
            All_train_recall += train_recall
            All_train_f1 += train_f1

            count += 1

            model.zero_grad()
            loss.backward()
            optimizer.step()
        
        Average_train_correct = round(All_train_correct/count, 3)
        Average_train_loss = round(AllTrainLoss/count, 3)
        Average_train_precision = round(All_train_precision/count, 3)
        Average_train_recall = round(All_train_recall/count, 3)
        Average_train_f1 = round(All_train_f1/count, 3)

        # 測試模式
        model.eval()
        All_test_correct = 0.0
        AllTestLoss = 0.0

        All_test_precision = 0.0
        All_test_recall = 0.0
        All_test_f1 = 0.0

        count = 0
        for batch_index, batch_dict in enumerate(test_dataloader):
            batch_dict = tuple(t.to(device) for t in batch_dict)

            outputs = model(
                batch_dict[0],
                token_type_ids = batch_dict[1],
                attention_mask = batch_dict[2],
                labels = batch_dict[3]
                )
            loss, logits = outputs[:2]

            test_correct = compute_accuracy(logits, batch_dict[3])       # 計算正確率

            # Precision, Recall, F1-score
            test_precision, test_recall, test_f1 = compute_metrics(logits, batch_dict[3])

            All_test_correct += test_correct
            AllTestLoss += loss.item()

            All_test_precision += test_precision
            All_test_recall += test_recall
            All_test_f1 += test_f1

            count += 1
        
        Average_test_correct = round(All_test_correct/count, 3)
        Average_test_loss = round(AllTestLoss/count, 3)

        Average_test_precision = round(All_test_precision/count, 3)
        Average_test_recall = round(All_test_recall/count, 3)
        Average_test_f1 = round(All_test_f1/count, 3)

        print('第' + str(epoch+1) + '次' + '訓練模式，loss為:' + str(Average_train_loss) + ' 正確率為' + str(Average_train_correct)+ '，測試模式，loss為:' + str(Average_test_loss) + ' 正確率為' + str(Average_test_correct))
        print('第' + str(epoch+1) + '次' + '訓練模式，precision為:' + str(Average_train_precision) + '，測試模式，precision為:' + str(Average_test_precision))
        print('第' + str(epoch+1) + '次' + '訓練模式，recall為:' + str(Average_train_recall) + '，測試模式，recall為:' + str(Average_test_recall))
        print('第' + str(epoch+1) + '次' + '訓練模式，f1-score為:' + str(Average_train_f1) + '，測試模式，f1-score為:' + str(Average_test_f1))

    model_to_save = model.module if hasattr(model, 'module') else model  # Take care of distributed/parallel training
    model_to_save.save_pretrained('20240416_trained_models')
    #model_to_save.save_pretrained('albert_model')
