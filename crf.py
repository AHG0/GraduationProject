import torch
import torch.nn as nn
from torchcrf import CRF
from utils import *
from model import *
import numpy as np
import matplotlib.pyplot as plt
from config import *


# 定义 CRF 层
class Crf(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = nn.Embedding(VOCAB_SIZE, EMBEDDING_DIM)
        self.fc1 = nn.Linear(EMBEDDING_DIM, EMBEDDING_DIM2)
        self.fc2 = nn.Linear(EMBEDDING_DIM2, TARGET_SIZE)
        self.crf = CRF(TARGET_SIZE, batch_first=True)

    def forward(self, input, mask):
        embed = self.embed(input)
        ouput = self.fc1(embed)
        ouput = self.fc2(ouput)
        return self.crf.decode(ouput, mask)

    def loss_fn(self, input, target, mask):
        embedding = self.embed(input)
        y_pred = self.fc1(embedding)
        y_pred = self.fc2(y_pred)
        return -self.crf.forward(y_pred, target, mask, reduction='mean')


def train():
    num_epochs = 100
    model = Crf().cuda()
    optimizer = torch.optim.Adam(model.parameters())
    loss_function = nn.CrossEntropyLoss()
    dataset = Dataset()
    loader = data.DataLoader(
        dataset,
        batch_size=100,
        shuffle=True,
        collate_fn=collate_fn,
        num_workers=0
    )
    # 训练模型
    for epoch in range(num_epochs):
        for b, (x, tags, mask) in enumerate(loader):
            # 前向传播
            loss = model.loss_fn(x.cuda(), tags.cuda(), mask.cuda())
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        print(f'epoch: {epoch + 1}/{num_epochs}, loss: {loss.item():.4f}')
    torch.save(model, MODEL_DIR + f'model_8_crf.pth')


def test():
    dataset = Dataset('test')
    loader = data.DataLoader(
        dataset,
        batch_size=100,
        shuffle=True,
        collate_fn=collate_fn,
        num_workers=0
    )

    # 测试模型
    with torch.no_grad():
        model = torch.load(MODEL_DIR + 'model_8_crf.pth')
        # for b, (x, tags, mask) in enumerate(loader):
        #     y_pred = model(x.cuda(), mask.cuda())
        #     # 计算准确率
        #     accuracy = (np.array(y_pred).argmax() == tags.cuda()).float().mean()
        # print(accuracy)

        y_true_list = []
        y_pred_list = []

        for b, (input, target, mask) in enumerate(loader):
            input = input.cuda()
            mask = mask.cuda()
            y_pred = model(input, mask)
            loss = model.loss_fn(input, target, mask)

            print('>> batch:', b + 1, 'loss:', loss.item())

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


if __name__ == '__main__':
    test()
