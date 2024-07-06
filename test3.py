import torch
import torch.nn as nn
from torchcrf import CRF
from utils import *
from model import *
import numpy as np
import matplotlib.pyplot as plt
from config import *


class LSTM(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(VOCAB_SIZE, EMBEDDING_DIM)  # 单词嵌入层
        self.lstm = nn.LSTM(EMBEDDING_DIM, HIDDEN_SIZE, bidirectional=False, batch_first=True)
        self.fc1 = nn.Linear(HIDDEN_SIZE, TARGET_SIZE)

    def forward(self, x):
        embedding = self.embedding(x)
        output, _ = self.lstm(embedding)
        output = self.fc1(output)
        return output

    def loss(self, outputs, mask):
        criterion = nn.CrossEntropyLoss()
        loss = criterion(outputs.view(-1, 6), mask.view(-1))
        return loss


def compute_accuracy(outputs, labels):
    _, outputs = torch.max(outputs, dim=2)
    outputs = outputs.cpu().numpy()
    labels = labels.cpu().numpy()
    accuracy = (outputs == labels).mean()

    return accuracy


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
    acc_list = []
    step = 0
    model = LSTM().cuda()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    for epoch in range(num_epochs):
        for i, (inputs, mask, labels) in enumerate(loader):
            mask = mask.cuda()
            inputs = inputs.cuda()
            outputs = model(inputs)

            loss = model.loss(outputs, mask)
            acc = compute_accuracy(outputs, mask)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        loss_list.append(loss.item())
        epoch_list.append(step)
        acc_list.append(acc)
        step += 1

        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}, Accuracy: {acc:.4f}')
    torch.save(model, MODEL_DIR + f'model_6_lstm.pth')
    y1 = loss_list
    y2 = acc_list
    x = epoch_list
    plt.xlabel('epoch')
    plt.plot(x, y1, label='loss')
    plt.plot(x, y2, label='acc')
    plt.axhline(y=1, color='black')
    plt.legend()
    plt.title('LSTM_train')
    plt.show()


def test():
    # 测试模型

    dataset = Dataset('test')
    loader = data.DataLoader(dataset, batch_size=100, collate_fn=collate_fn)
    test_epoch_list = []
    test_acc_list = []
    step = 0
    with torch.no_grad():
        model = torch.load(MODEL_DIR + 'model_6_lstm.pth')
        y_true_list = []
        y_pred_list = []
        for b, (x, tags, mask) in enumerate(loader):
            logits = model(x.cuda())
            logits = logits.cpu()
            preds = logits.argmax(dim=-1)

            acc = (preds == tags.cpu()).float().mean()
            # test_acc_list.append(acc)
            # test_epoch_list.append(step)
            # step += 1
        print(f'>> total: {len(tags)}, Test accuracy: {acc:.4f}')

    x = test_epoch_list
    y = test_acc_list
    plt.plot(x, y, label='acc')
    plt.xlabel('epoch')
    plt.legend()
    plt.title('LSTM_test')
    plt.show()


if __name__ == '__main__':
    train()
    # test()
