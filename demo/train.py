import torch.optim as optim
from transformers import BertTokenizer
from torch.utils.data import DataLoader
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
from demo.model import *
from demo.utils import *
import torch
import torch.nn as nn

plt.rcParams['font.sans-serif'] = ['SimHei']
# 从本地目录加载BERT分词器
model_path = r'D:\bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_path)

# 加载标签到索引的映射并创建反向映射
label_to_index = load_label_to_index('label2id.json')
index_to_label = {v: k for k, v in label_to_index.items()}


def train(model_name):
    print(f"开始训练{model_name}模型......")
    # 模型、损失函数和优化器
    hidden_size = 768  # 因为使用的是 'bert-base-uncased'
    embedding_dim = 128
    num_of_class = len(label_to_index)

    if model_name == "AttOneBiLSTM":
        model = AttOneBiLSTM(embedding_dim, hidden_size=hidden_size, num_classes=num_of_class,
                             vocab_size=tokenizer.vocab_size)
    if model_name == "AttTwoBiLSTM":
        model = AttTwoBiLSTM(embedding_dim, hidden_size=hidden_size, num_classes=num_of_class,
                             vocab_size=tokenizer.vocab_size)
    if model_name == "BiLSTM_CNN_Attention":
        model = BiLSTM_CNN_Attention(embedding_dim, hidden_size=hidden_size, num_classes=num_of_class,
                                     vocab_size=tokenizer.vocab_size)
    if model_name == "Att1B2F_2CNN":
        model = Att1B2F_2CNN(embedding_dim, hidden_size=hidden_size, num_classes=num_of_class,
                             vocab_size=tokenizer.vocab_size)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 检查CUDA是否可用
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 如果可用，将模型和损失函数移到CUDA设备上
    model.to(device)
    criterion.to(device)

    # 加载数据并为训练、验证和测试集创建DataLoader
    train_dataset = load_data('./WebNLG/new_train.json', label_to_index, tokenizer, max_length=64)
    valid_dataset = load_data('./WebNLG/new_valid.json', label_to_index, tokenizer, max_length=64)  # 修改了文件名
    test_dataset = load_data('./WebNLG/new_test.json', label_to_index, tokenizer, max_length=64)

    train_dataloader = DataLoader(train_dataset, batch_size=1, shuffle=True)
    valid_dataloader = DataLoader(valid_dataset, batch_size=1, shuffle=False)
    test_dataloader = DataLoader(test_dataset, batch_size=1, shuffle=False)

    # 存储绘图用的指标列表
    train_loss_list = []
    valid_loss_list = []

    accuracy_list = []
    f1_list = []
    Epochs = 20
    # 训练循环，计算损失、准确率和F1分数
    for epoch in range(Epochs):
        model.train()  # 确保模型处于训练模式
        total_loss = 0
        total_correct = 0
        total_samples = 0
        predictions = []
        true_labels = []

        for input_ids, attention_mask, label_id in train_dataloader:
            optimizer.zero_grad()

            input_ids = input_ids.to(device)
            attention_mask = attention_mask.to(device)
            label_id = label_id.to(device)

            output = model(input_ids, attention_mask)
            loss = criterion(output, label_id)
            total_loss += loss.item()

            _, predicted = torch.max(output, 1)
            total_correct += (predicted == label_id).sum().item()
            total_samples += label_id.size(0)

            predictions.extend(predicted.cpu().numpy())
            true_labels.extend(label_id.cpu().numpy())

            loss.backward()
            optimizer.step()

        epoch_train_loss = total_loss / len(train_dataloader)
        train_loss_list.append(epoch_train_loss)

        # 计算训练准确率和F1分数
        train_accuracy = total_correct / total_samples
        train_f1 = f1_score(true_labels, predictions, average='weighted')

        print(
            f"训练 -> Epoch {epoch + 1}, 损失: {epoch_train_loss:.4f}, 准确率: {train_accuracy:.4f}, F1分数: {train_f1:.4f}")

        # 验证
        model.eval()  # 确保模型处于评估模式
        total_loss = 0
        total_correct = 0
        total_samples = 0
        predictions = []
        true_labels = []

        with torch.no_grad():
            for input_ids, attention_mask, label_id in valid_dataloader:
                input_ids = input_ids.to(device)
                attention_mask = attention_mask.to(device)
                label_id = label_id.to(device)

                outputs = model(input_ids, attention_mask)
                loss = criterion(outputs, label_id)
                total_loss += loss.item()

                _, predicted = torch.max(outputs, 1)
                total_correct += (predicted == label_id).sum().item()
                total_samples += label_id.size(0)

                predictions.extend(predicted.cpu().numpy())
                true_labels.extend(label_id.cpu().numpy())

        epoch_valid_loss = total_loss / len(valid_dataloader)
        valid_loss_list.append(epoch_valid_loss)

        # 计算验证准确率和F1分数
        valid_accuracy = total_correct / total_samples
        accuracy_list.append(valid_accuracy)
        valid_f1 = f1_score(true_labels, predictions, average='weighted')
        f1_list.append(valid_f1)
        print(
            f"验证 -> Epoch {epoch + 1}, 损失: {epoch_valid_loss:.4f}, 准确率: {valid_accuracy:.4f}, F1分数: {valid_f1:.4f}")

    # 测试
    total_loss = 0
    total_correct = 0
    total_samples = 0
    predictions = []
    true_labels = []

    with torch.no_grad():
        for input_ids, attention_mask, label_id in test_dataloader:
            input_ids = input_ids.to(device)
            attention_mask = attention_mask.to(device)
            label_id = label_id.to(device)

            outputs = model(input_ids, attention_mask)
            loss = criterion(outputs, label_id)
            total_loss += loss.item()

            _, predicted = torch.max(outputs, 1)
            total_correct += (predicted == label_id).sum().item()
            total_samples += label_id.size(0)

            predictions.extend(predicted.cpu().numpy())
            true_labels.extend(label_id.cpu().numpy())

    epoch_test_loss = total_loss / len(test_dataloader)

    # 计算测试准确率和F1分数
    test_accuracy = total_correct / total_samples
    test_f1 = f1_score(true_labels, predictions, average='weighted')
    print(f"测试 -> 损失: {epoch_test_loss:.4f}, 准确率: {test_accuracy:.4f}, F1分数: {test_f1:.4f}")

    # 绘制指标
    Epochs = range(1, Epochs + 1)

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(Epochs, train_loss_list, label='训练损失', color='blue')
    plt.plot(Epochs, valid_loss_list, label='验证损失', color='green')
    plt.title(f'训练、验证loss，测试集准确率：{test_accuracy:.4f}，F1：{test_f1:.4f}')
    plt.xlabel('Epochs')
    plt.ylabel('损失')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(Epochs, accuracy_list, label='准确率', color='green')
    plt.plot(Epochs, f1_list, label='F1分数', color='orange')
    plt.title('验证集准确率和F1分数')
    plt.xlabel('Epochs')
    plt.ylabel('值')
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    train("Att1B2F_2CNN")
    train("BiLSTM_CNN_Attention")
    train("AttTwoBiLSTM")

# 开始训练AttTwoBiLSTM模型......
# 训练 -> Epoch 1, 损失: 2.1710, 准确率: 0.5015, F1分数: 0.4814
# 验证 -> Epoch 1, 损失: 0.7290, 准确率: 0.7996, F1分数: 0.7880
# 训练 -> Epoch 2, 损失: 0.6134, 准确率: 0.8513, F1分数: 0.8463
# 验证 -> Epoch 2, 损失: 0.3917, 准确率: 0.9070, F1分数: 0.9008
# 训练 -> Epoch 3, 损失: 0.3942, 准确率: 0.8952, F1分数: 0.8929
# 验证 -> Epoch 3, 损失: 0.2914, 准确率: 0.9284, F1分数: 0.9237
# 训练 -> Epoch 4, 损失: 0.3176, 准确率: 0.9130, F1分数: 0.9115
# 验证 -> Epoch 4, 损失: 0.2837, 准确率: 0.9213, F1分数: 0.9217
# 训练 -> Epoch 5, 损失: 0.3070, 准确率: 0.9203, F1分数: 0.9191
# 验证 -> Epoch 5, 损失: 0.2790, 准确率: 0.9329, F1分数: 0.9326
# 训练 -> Epoch 6, 损失: 0.2593, 准确率: 0.9269, F1分数: 0.9259
# 验证 -> Epoch 6, 损失: 0.3422, 准确率: 0.9347, F1分数: 0.9327
# 训练 -> Epoch 7, 损失: 0.2610, 准确率: 0.9296, F1分数: 0.9288
# 验证 -> Epoch 7, 损失: 0.3528, 准确率: 0.9338, F1分数: 0.9320
# 训练 -> Epoch 8, 损失: 0.2396, 准确率: 0.9305, F1分数: 0.9297
# 验证 -> Epoch 8, 损失: 0.2728, 准确率: 0.9445, F1分数: 0.9435
# 训练 -> Epoch 9, 损失: 0.2289, 准确率: 0.9335, F1分数: 0.9330
# 验证 -> Epoch 9, 损失: 0.3302, 准确率: 0.9392, F1分数: 0.9377
# 训练 -> Epoch 10, 损失: 0.2241, 准确率: 0.9370, F1分数: 0.9364
# 验证 -> Epoch 10, 损失: 0.3701, 准确率: 0.9275, F1分数: 0.9248
# 训练 -> Epoch 11, 损失: 0.2282, 准确率: 0.9359, F1分数: 0.9352
# 验证 -> Epoch 11, 损失: 0.3171, 准确率: 0.9311, F1分数: 0.9287
# 训练 -> Epoch 12, 损失: 0.1997, 准确率: 0.9427, F1分数: 0.9421
# 验证 -> Epoch 12, 损失: 0.3186, 准确率: 0.9419, F1分数: 0.9399
# 训练 -> Epoch 13, 损失: 0.1951, 准确率: 0.9428, F1分数: 0.9422
# 验证 -> Epoch 13, 损失: 0.3636, 准确率: 0.9392, F1分数: 0.9375
# 训练 -> Epoch 14, 损失: 0.2132, 准确率: 0.9384, F1分数: 0.9379
# 验证 -> Epoch 14, 损失: 0.2925, 准确率: 0.9526, F1分数: 0.9509
# 训练 -> Epoch 15, 损失: 0.2069, 准确率: 0.9398, F1分数: 0.9392
# 验证 -> Epoch 15, 损失: 0.3608, 准确率: 0.9392, F1分数: 0.9386
# 训练 -> Epoch 16, 损失: 0.2172, 准确率: 0.9378, F1分数: 0.9371
# 验证 -> Epoch 16, 损失: 0.2933, 准确率: 0.9428, F1分数: 0.9400
# 训练 -> Epoch 17, 损失: 0.2105, 准确率: 0.9359, F1分数: 0.9353
# 验证 -> Epoch 17, 损失: 0.2788, 准确率: 0.9419, F1分数: 0.9383
# 训练 -> Epoch 18, 损失: 0.2062, 准确率: 0.9399, F1分数: 0.9396
# 验证 -> Epoch 18, 损失: 0.2794, 准确率: 0.9472, F1分数: 0.9458
# 训练 -> Epoch 19, 损失: 0.2101, 准确率: 0.9375, F1分数: 0.9370
# 验证 -> Epoch 19, 损失: 0.3202, 准确率: 0.9365, F1分数: 0.9331
# 训练 -> Epoch 20, 损失: 0.2171, 准确率: 0.9397, F1分数: 0.9389
# 验证 -> Epoch 20, 损失: 0.3750, 准确率: 0.9374, F1分数: 0.9363
# 测试 -> 损失: 0.4104, 准确率: 0.9214, F1分数: 0.9208
