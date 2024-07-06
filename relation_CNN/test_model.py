from torch.utils.data import DataLoader
from data_process import *
from sklearn.model_selection import train_test_split
from AttBiLSTM import *
from sklearn.metrics import accuracy_score, f1_score, recall_score

# 加载已保存的模型
model = torch.load(r'D:\Users\17614\PycharmProjects\relation_CNN\TwoBiLSTM_CNN_Attention.pth')
model.eval()

torch.manual_seed(2000)

data = DataProcess()
text_tensor, _ = data.get_text_tensor()

text_train, text_test, label_train, label_test = train_test_split(text_tensor, data.get_label_tensor(), test_size=0.2,
                                                                  random_state=42)

train_dataset = MyDataset(text_train, label_train)
test_dataset = MyDataset(text_test, label_test)

# 创建训练集和测试集
train_data_loader = DataLoader(train_dataset, batch_size=16, shuffle=True, num_workers=0)
test_data_loader = DataLoader(test_dataset, batch_size=16, shuffle=False, num_workers=0)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

vocab_size = 5273
lr = 0.001
epochs = 200

# 对测试数据集进行预测
with torch.no_grad():
    model.eval()
    all_preds_test = []
    all_labels_test = []

    with torch.no_grad():
        for text_test, label_test in test_data_loader:
            text_test, label_test = text_test.to(device), label_test.long().to(device)

            output_test = model(text_test)
            _, pred_test = torch.max(output_test, 1)
            all_preds_test.extend(pred_test.cpu().numpy())
            all_labels_test.extend(label_test.cpu().numpy())

    accuracy_test = accuracy_score(all_labels_test, all_preds_test)
    f1_test = f1_score(all_labels_test, all_preds_test, average='weighted')
    recall_test = recall_score(all_labels_test, all_preds_test, average='weighted')
    print(
        f'Test Accuracy: {accuracy_test * 100:.4f}%, Test Recall: {recall_test * 100:.4f}%, Test F1 Score: {f1_test:.4f}')

