import torch
import torch.nn as nn
from torchcrf import CRF
from utils import *
from model import *
import numpy as np
import matplotlib.pyplot as plt
from config import *


class BiLSTM_CRF(nn.Module):
    def __init__(self):
        super(BiLSTM_CRF, self).__init__()
        self.embed = nn.Embedding(VOCAB_SIZE, EMBEDDING_DIM)  # 单词嵌入层
        self.lstm = nn.LSTM(EMBEDDING_DIM, HIDDEN_SIZE, bidirectional=True, batch_first=True)  # 双向 LSTM 层
        self.fc1 = nn.Linear(HIDDEN_SIZE * 2, HIDDEN_SIZE)
        self.fc2 = nn.Linear(HIDDEN_SIZE, TARGET_SIZE)  # 输出层
        self.crf = CRF(TARGET_SIZE, batch_first=True)  # CRF 层

    def forward(self, x, mask):
        embedding = self.embed(x)
        lstm_out, _ = self.lstm(embedding)
        lstm_out = self.fc1(lstm_out)
        tag_space = self.fc2(lstm_out)
        return self.crf.decode(tag_space, mask)

    def loss_fn(self, input, target, mask):
        embedding = self.embed(input)
        lstm_out, _ = self.lstm(embedding)
        lstm_out = self.fc1(lstm_out)
        y_pred = self.fc2(lstm_out)
        return -self.crf.forward(y_pred, target, mask, reduction='mean')


def train():
    dataset = Dataset()
    loader = data.DataLoader(
        dataset,
        batch_size=100,
        shuffle=True,
        collate_fn=collate_fn,
        num_workers=0
    )

    num_epochs = 100

    loss_list = []
    epoch_list = []
    step = 0

    # 训练模型
    model = BiLSTM_CRF().cuda()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    for epoch in range(num_epochs):
        for b, (x, tags, mask) in enumerate(loader):
            # 前向传播
            loss = model.loss_fn(x.cuda(), tags.cuda(), mask.cuda())
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        loss_list.append(loss.item())
        epoch_list.append(step)
        step += 1
        print(f'epoch: {epoch + 1}/{num_epochs}, loss: {loss.item():.4f}')
    torch.save(model, MODEL_DIR + f'model_5_bilstm-crf.pth')

    y1 = loss_list
    # y2 = acc_list
    x = epoch_list
    plt.xlabel('epoch')

    plt.plot(x, y1, label='loss')
    # plt.plot(x, y2, label='acc')
    plt.legend()
    plt.title('BiLSTM-CRF_train')
    plt.show()


# 测试模型
def test():
    dataset = Dataset('test')
    loader = data.DataLoader(dataset, batch_size=100, collate_fn=collate_fn)

    test_epoch_list = []
    test_acc_list = []
    step = 0
    with torch.no_grad():
        model = torch.load(MODEL_DIR + 'model_5_bilstm-crf.pth')
        y_true_list = []
        y_pred_list = []

        for b, (input, target, mask) in enumerate(loader):
            input = input.cuda()
            mask = mask.cuda()
            y_pred = model(input, mask)
            # loss = model.loss_fn(input, target, mask)
            # print('>> batch:', b + 1, 'loss:', loss.item())

            # 拼接返回值
            for lst in y_pred:
                y_pred_list += lst
            for y, m in zip(target, mask):
                y_true_list += y[m == True].tolist()

        # 整体准确率
        y_true_tensor = torch.tensor(y_true_list)
        y_pred_tensor = torch.tensor(y_pred_list)
        accuracy = (y_true_tensor == y_pred_tensor).sum() / len(y_true_tensor)
        print(f'>> total: {len(y_true_tensor)}, Test accuracy: {accuracy.item():.4f}')
    #     test_epoch_list.append(step)
    #     test_acc_list.append(accuracy)
    #     step += 1
    #
    # x = test_epoch_list
    # y = test_acc_list
    # plt.plot(x, y, label='acc')
    # plt.xlabel('epoch')
    # plt.title('BiLSTM-CRF_test')
    # plt.legend()
    # plt.show()


if __name__ == '__main__':
    test()
