from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, f1_score, recall_score
from data_process import *
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from AttBiLSTM import *
import os

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
epochs = 100


def optimal_parameter(embedding_dim, hidden_size):
    for i in range(5):
        for j in range(6):
            model_name = "TwoBiLSTM_DoubleAttention.pth"
            model = TwoBiLSTM_DoubleAttention(vocab_size=vocab_size, embedding_dim=embedding_dim,
                                              hidden_size=hidden_size, num_of_class=5).to(device)

            # 定义损失函数criterion，使用交叉熵损失函数
            criterion = torch.nn.CrossEntropyLoss()
            # 梯度下降使用的Adam算法
            optimizer = torch.optim.Adam(model.parameters(), lr=lr)

            losses = []
            accuracies = []
            f1_scores = []
            recalls = []
            print(f"开始训练{model_name}模型......e：{embedding_dim}，h：{hidden_size}")
            for epoch in range(epochs):

                model.train()
                total_loss = 0.0
                all_pred = []
                all_labels = []

                for text, label in train_data_loader:
                    text, label = text.to(device), label.long().to(device)
                    output = model(text)
                    loss = criterion(output, label)
                    total_loss += loss.item()
                    _, pred = torch.max(output, 1)
                    all_pred.extend(pred.cpu().numpy())
                    all_labels.extend(label.cpu().numpy())
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                accuracy = accuracy_score(all_labels, all_pred)
                f1 = f1_score(all_labels, all_pred, average='weighted')
                recall = recall_score(all_labels, all_pred, average='weighted')  # 计算召回率

                losses.append(total_loss)
                accuracies.append(accuracy)
                f1_scores.append(f1)
                recalls.append(recall)  # 将召回率值添加到列表中
                if epoch % 10 == 0:
                    print(
                        f'Epoch {epoch}/{epochs}, Loss: {total_loss:.4f}, Accuracy: {accuracy:.4f}, Recall: {recall:.4f}, F1 Score: {f1:.4f}')

            # 模型测试
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

            # 保存模型
            torch.save(model, model_name)

            if f1_test >= 0.8:
                epochs_range = np.arange(1, epochs + 1)

                plt.figure(figsize=(12, 5))

                plt.subplot(1, 2, 1)
                plt.plot(epochs_range, losses, label='Training Loss')
                plt.title(f'{model_name} e{embedding_dim} h{hidden_size}')
                plt.xlabel('Epochs')
                plt.ylabel('Loss')
                plt.legend()

                plt.subplot(1, 2, 2)
                plt.plot(epochs_range, accuracies, label='Accuracy', linestyle='dashed')
                plt.plot(epochs_range, f1_scores, label='F1 Score', linestyle=':')
                plt.rcParams['font.sans-serif'] = ['SimHei']
                plt.title(f'Acc_{accuracy_test:.4f} Rec_{recall_test:.4f} F1_{f1_test:.4f}')
                plt.xlabel('Epochs')
                plt.ylabel('Score')
                plt.legend()

                plt.tight_layout()
                plt.show()
            hidden_size += 100
        embedding_dim += 100


def select_model(model_name):
    switcher = {
        "TwoBiLSTM_DoubleAttention": TwoBiLSTM_DoubleAttention(vocab_size=vocab_size, embedding_dim=embedding_dim,
                                                               hidden_size=hidden_size, num_of_class=5).to(device),
        "TwoBiLSTM_CNN_DoubleAttention": TwoBiLSTM_CNN_DoubleAttention(vocab_size=vocab_size,
                                                                       embedding_dim=embedding_dim,
                                                                       hidden_size=hidden_size, num_of_class=5).to(
            device),
        "ThreeBiLSTM_CNN_ThreeAttention": ThreeBiLSTM_CNN_ThreeAttention(vocab_size=vocab_size,
                                                                         embedding_dim=embedding_dim,
                                                                         hidden_size=hidden_size, num_of_class=5).to(
            device),
        "TwoBiLSTM_CNN_TwoAttention": TwoBiLSTM_CNN_TwoAttention(vocab_size=vocab_size,
                                                                 embedding_dim=embedding_dim,
                                                                 hidden_size=hidden_size, num_of_class=5).to(device),
        "TwoBiLSTM_CNN_Attention": TwoBiLSTM_CNN_Attention(vocab_size=vocab_size, embedding_dim=embedding_dim,
                                                           hidden_size=hidden_size, num_of_class=5).to(device),
        "Att1B2F_2CNN": Att1B2F_2CNN(vocab_size=vocab_size, embedding_dim=embedding_dim, hidden_size=hidden_size,
                                     num_of_class=5).to(device),
        "BiLSTM_CNN_Attention": BiLSTM_CNN_Attention(vocab_size=vocab_size, embedding_dim=embedding_dim,
                                                     hidden_size=hidden_size, num_of_class=5).to(device),
        "Att2B2F": Att2B2F(vocab_size=vocab_size, embedding_dim=embedding_dim, hidden_size=hidden_size,
                           num_of_class=5).to(device),
        "Att1B2F": Att1B2F(vocab_size=vocab_size, embedding_dim=embedding_dim, hidden_size=hidden_size,
                           num_of_class=5).to(device),
        "Att2B1F": Att2B1F(vocab_size=vocab_size, embedding_dim=embedding_dim, hidden_size=hidden_size,
                           num_of_class=5).to(device),
        "Att1B1F": Att1B1F(vocab_size=vocab_size, embedding_dim=embedding_dim, hidden_size=hidden_size,
                           num_of_class=5).to(device),
        "Att2B1F0D": Att2B1F0D(vocab_size=vocab_size, embedding_dim=embedding_dim, hidden_size=hidden_size,
                               num_of_class=5).to(device),
        "Att1B1F0D": Att1B1F0D(vocab_size=vocab_size, embedding_dim=embedding_dim, hidden_size=hidden_size,
                               num_of_class=5).to(device),
        "Att2B2FNA": Att2B2FNA(vocab_size=vocab_size, embedding_dim=embedding_dim, hidden_size=hidden_size,
                               num_of_class=5).to(device),
        "Att1B2FNA": Att1B2FNA(vocab_size=vocab_size, embedding_dim=embedding_dim, hidden_size=hidden_size,
                               num_of_class=5).to(device),
    }
    return switcher.get(model_name, "Invalid model name")


def circuit_training(model_name, embedding_dim, hidden_size):
    model = select_model(model_name)
    # 定义损失函数criterion，使用交叉熵损失函数
    criterion = torch.nn.CrossEntropyLoss()
    # 梯度下降使用的Adam算法
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    losses = []
    accuracies = []
    f1_scores = []
    recalls = []
    i = 1
    while (1):
        save_model = model_name + str(i) + ".pth"
        print(f"开始训练{save_model}模型......e：{embedding_dim}，h：{hidden_size}")
        for epoch in range(epochs):
            model.train()
            total_loss = 0.0
            all_pred = []
            all_labels = []

            for text, label in train_data_loader:
                text, label = text.to(device), label.long().to(device)
                output = model(text)
                loss = criterion(output, label)
                total_loss += loss.item()
                _, pred = torch.max(output, 1)
                all_pred.extend(pred.cpu().numpy())
                all_labels.extend(label.cpu().numpy())
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            accuracy = accuracy_score(all_labels, all_pred)
            f1 = f1_score(all_labels, all_pred, average='weighted')
            recall = recall_score(all_labels, all_pred, average='weighted')  # 计算召回率

            losses.append(total_loss)
            accuracies.append(accuracy)
            f1_scores.append(f1)
            recalls.append(recall)  # 将召回率值添加到列表中
            if epoch % 10 == 0:
                print(
                    f'Epoch {epoch}/{epochs}, Loss: {total_loss:.4f}, Accuracy: {accuracy:.4f}, Recall: {recall:.4f}, F1 Score: {f1:.4f}')

        # 模型测试
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

        # 判断文件夹是否存在，如果不存在则创建
        if not os.path.exists(f'model/{model_name}'):
            os.makedirs(f'model/{model_name}')
        # 保存模型到指定文件夹
        torch.save(model, f'./model/{model_name}/{save_model}')

        epochs_range = np.arange(1, i * epochs + 1)

        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, losses, label='Training Loss')
        plt.title(f'{model_name} e{embedding_dim} h{hidden_size}')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, accuracies, label='Accuracy', linestyle='dashed')
        plt.plot(epochs_range, f1_scores, label='F1 Score', linestyle=':')
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.title(f'Acc_{accuracy_test:.4f} Rec_{recall_test:.4f} F1_{f1_test:.4f}')
        plt.xlabel('Epochs')
        plt.ylabel('Score')
        plt.legend()

        plt.tight_layout()
        plt.show()
        # 保存图形到指定文件夹
        plt.savefig(f'./model/{model_name}/{model_name}.png')
        i += 1


if __name__ == '__main__':
    embedding_dim = 256
    hidden_size = 512
    model_list1 = ["TwoBiLSTM_CNN_Attention", "Att1B2F_2CNN", "BiLSTM_CNN_Attention"]
    model_list2 = ["TwoBiLSTM_CNN_DoubleAttention", "Att1B2F", "Att2B2F", "Att2B1F", "Att1B1F"]
    model_name = "ThreeBiLSTM_CNN_ThreeAttention"
    # optimal_parameter(embedding_dim, hidden_size)
    circuit_training(model_name, embedding_dim, hidden_size)
