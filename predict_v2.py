import torch
import pickle
from transformers import BertConfig, BertForSequenceClassification, BertTokenizer
import torch.nn.functional as F

def toBertIds(question_input):
    return tokenizer.build_inputs_with_special_tokens(tokenizer.convert_tokens_to_ids(tokenizer.tokenize(question_input)))

if __name__ == "__main__":
    # Load and initialize
    tokenizer = BertTokenizer(vocab_file='bert-base-chinese-vocab.txt')
    morality_type = "harm"
    with open(f'20240420_{morality_type}_trained_models/data_features.pkl', 'rb') as pkl_file:
        data_features = pickle.load(pkl_file)
    answer_dic = data_features['answer_dic']
    #print(dir(answer_dic))

    config = BertConfig.from_pretrained(f'20240420_{morality_type}_trained_models/config.json')
    model = BertForSequenceClassification.from_pretrained(f'20240420_{morality_type}_trained_models/model.safetensors', config=config)
    model.eval()

    with open(f'20240420_{morality_type}_trained_models/20240420_{morality_type}_test_data.txt', 'r', encoding='utf-8') as f:
        data = f.read()
    qa_pairs = data.split("\n")
    questions = []
    answers = []

    for qa_pair in qa_pairs:
        parts = qa_pair.split()
        if len(parts) >= 2:
            a, q = parts[0], ' '.join(parts[1:])
            questions.append(q)
            answers.append(a)

    # Initialize counters
    TP = {}
    FP = {}
    FN = {}
    total_correct = 0
    for label in answer_dic.answers_norepeat:
        TP[label] = 0
        FP[label] = 0
        FN[label] = 0

    # Evaluation
    for index, question in enumerate(questions):
        bert_ids = toBertIds(question)
        input_ids = torch.LongTensor(bert_ids).unsqueeze(0)
        outputs = model(input_ids)
        prediction = torch.max(F.softmax(outputs.logits, dim=1), dim=1)[1]
        #predict_label = answer_dic[prediction.item()]
        predict_label = answer_dic.to_text(prediction.item())

        true_label = answers[index]
        if predict_label == true_label:
            TP[true_label] += 1
            total_correct += 1
        else:
            FP[predict_label] += 1
            FN[true_label] += 1

    total_questions = len(questions)
    accuracy = total_correct / total_questions

    # Calculate precision, recall, and F1-score
    precision = {label: TP[label] / (TP[label] + FP[label]) if TP[label] + FP[label] > 0 else 0 for label in TP}
    recall = {label: TP[label] / (TP[label] + FN[label]) if TP[label] + FN[label] > 0 else 0 for label in TP}
    f1_score = {label: 2 * (precision[label] * recall[label]) / (precision[label] + recall[label]) if precision[label] + recall[label] > 0 else 0 for label in TP}

    print("Accuracy: {:.2f}%".format(accuracy * 100))
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1-Score:", f1_score)