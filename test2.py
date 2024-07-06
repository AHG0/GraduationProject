import torch
import torch.nn as nn
from torchcrf import CRF
from utils import *
from model import *
import numpy as np
import matplotlib.pyplot as plt
from config import *


class BiLSTM(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(VOCAB_SIZE, EMBEDDING_DIM)  # 单词嵌入层
        self.lstm = nn.LSTM(EMBEDDING_DIM, HIDDEN_SIZE, bidirectional=True, batch_first=True)
        self.fc1 = nn.Linear(HIDDEN_SIZE * 2, HIDDEN_SIZE)
        self.fc2 = nn.Linear(HIDDEN_SIZE, TARGET_SIZE)

    def forward(self, x):
        # x is a tensor of shape (batch_size, sequence_length, input_dim)
        embedding = self.embedding(x)
        output, _ = self.lstm(embedding)
        # output is a tensor of shape (batch_size, sequence_length, hidden_dim * 2)
        # hidden is a tensor of shape (num_layers * 2, batch_size, hidden_dim)
        # cell is a tensor of shape (num_layers * 2, batch_size, hidden_dim)
        output = self.fc1(output)
        output = self.fc2(output)
        # output is a tensor of shape (batch_size, sequence_length, num_classes)
        return output

    def loss(self, outputs, mask):
        # Compute the loss and accuarcy
        criterion = nn.CrossEntropyLoss()
        # Compute the loss
        loss = criterion(outputs.view(-1, 6), mask.view(-1))
        return loss


def compute_accuracy(outputs, labels):
    # outputs is a tensor of shape (batch_size, sequence_length, num_classes)
    # labels is a tensor of shape (batch_size, sequence_length)
    # Get the predicted class for each word in the batch
    _, predictions = torch.max(outputs, dim=2)
    # Convert the predictions and labels to numpy arrays
    predictions = predictions.cpu().numpy()
    labels = labels.cpu().numpy()
    # Compute the accuracy for each word in the batch
    accuracy = (predictions == labels).mean()

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
    # Define the model
    model = BiLSTM().cuda()
    # Define the loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    for epoch in range(num_epochs):
        for i, (inputs, mask, labels) in enumerate(loader):
            print(mask)
            print(mask.shape)
            # Forward pass
            mask = mask.cuda()
            inputs = inputs.cuda()
            # outputs = model(inputs, labels, mask).cuda()
            outputs = model(inputs)
            # loss = criterion(outputs, mask)

            loss = model.loss(outputs, mask)

            acc = compute_accuracy(outputs, mask)

            # Backward pass and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        loss_list.append(loss.item())
        epoch_list.append(step)
        acc_list.append(acc)
        step += 1

        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}, Accuracy: {acc:.4f}')
    torch.save(model, MODEL_DIR + f'model_4_bilstm.pth')
    y1 = loss_list
    y2 = acc_list
    x = epoch_list
    plt.xlabel('epoch')
    plt.plot(x, y1, label='loss')
    plt.plot(x, y2, label='acc')
    plt.axhline(y=1, color='black')
    plt.legend()
    plt.title('BiLSTM_train')
    plt.show()


def test():
    # 测试模型

    dataset = Dataset('test')
    loader = data.DataLoader(dataset, batch_size=100, collate_fn=collate_fn)
    test_epoch_list = []
    test_acc_list = []
    step = 0
    with torch.no_grad():
        model = torch.load(MODEL_DIR + 'model_4_bilstm.pth')
        y_true_list = []
        y_pred_list = []
        for b, (x, tag, mask) in enumerate(loader):
            logits = model(x.cuda())
            logits = logits.cpu()
            tags = tag.view(-1)
            preds = logits.argmax(dim=-1).view(-1)
            accuracy = (tags == preds).sum() / len(tags)

            # acc = (preds == tags.cpu()).float().mean()
            # test_acc_list.append(accuracy)
            # test_epoch_list.append(step)
            # step += 1
        print(f'>> total: {len(tag)}, Test accuracy: {accuracy.item():.4f}')

    # x = test_epoch_list
    # y = test_acc_list
    # plt.plot(x, y, label='acc')
    # plt.xlabel('epoch')
    # plt.legend()
    # plt.title('BiLSTM_test')
    # plt.show()


if __name__ == '__main__':
    # test()
    train()