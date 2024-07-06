import torch.nn as nn
from config import *
from torchcrf import CRF
import torch
from transformers import BertModel


class Model(nn.Module):
    def __init__(self, bert_config):
        super().__init__()
        self.embed = nn.Embedding(VOCAB_SIZE, EMBEDDING_DIM)
        self.bert = BertModel(config=bert_config)
        self.lstm = nn.LSTM(
            EMBEDDING_DIM,
            HIDDEN_SIZE,
            batch_first=True,
            bidirectional=True,
        )
        self.fc1 = nn.Linear(HIDDEN_SIZE * 2, TARGET_SIZE)
        # self.fc2 = nn.Linear(EMBEDDING_DIM2, TARGET_SIZE)
        # self.fc3 = nn.Linear(HIDDEN_SIZE3, TARGET_SIZE)
        self.crf = CRF(TARGET_SIZE, batch_first=True)

    def _get_lstm_feature(self, input):
        out = self.bert(input)[0]
        out, _ = self.lstm(out)
        # out = self.fc1(out)
        return self.fc1(out)

    def forward(self, input, mask):
        out = self._get_lstm_feature(input)
        return self.crf.decode(out, mask)

    def loss_fn(self, input, target, mask):
        # embedding = self.embed(input)
        embedding = self.bert(input)[0]
        lstm_out, _ = self.lstm(embedding)
        y_pred = self.fc1(lstm_out)
        return -self.crf.forward(y_pred, target, mask, reduction='mean')


class BiLSTM(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(VOCAB_SIZE, EMBEDDING_DIM)  # 单词嵌入层
        self.lstm = nn.LSTM(EMBEDDING_DIM, HIDDEN_SIZE, bidirectional=True, batch_first=True)
        self.fc1 = nn.Linear(HIDDEN_SIZE * 2, HIDDEN_SIZE)
        self.fc2 = nn.Linear(HIDDEN_SIZE, TARGET_SIZE)

    def forward(self, x):
        embedding = self.embedding(x)
        output, _ = self.lstm(embedding)
        output = self.fc1(output)
        output = self.fc2(output)
        return output


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


class LSTM_CRF(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = nn.Embedding(VOCAB_SIZE, EMBEDDING_DIM)
        self.lstm = nn.LSTM(EMBEDDING_DIM, HIDDEN_SIZE, bidirectional=False, batch_first=True)
        self.fc1 = nn.Linear(HIDDEN_SIZE, TARGET_SIZE)
        self.crf = CRF(TARGET_SIZE, batch_first=True)

    def forward(self, x, mask):
        embedding = self.embed(x)
        lstm_out, _ = self.lstm(embedding)
        tag_space = self.fc1(lstm_out)
        return self.crf.decode(tag_space, mask)

    def loss_fn(self, input, target, mask):
        embedding = self.embed(input)
        lstm_out, _ = self.lstm(embedding)
        y_pred = self.fc1(lstm_out)
        return -self.crf.forward(y_pred, target, mask, reduction='mean')


class Crf(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = nn.Embedding(VOCAB_SIZE, EMBEDDING_DIM)
        self.fc1 = nn.Linear(EMBEDDING_DIM, 1000)
        self.fc2 = nn.Linear(1000, TARGET_SIZE)
        self.crf = CRF(TARGET_SIZE, batch_first=True)

    def forward(self, input, mask):
        embed = self.embed(input)
        ouput = self.fc1(embed)
        ouput = self.fc2(ouput)
        return self.crf.decode(ouput, mask)

    def loss_fn(self, input, target, mask):
        embedding = self.embed(input)
        lstm_out, _ = self.lstm(embedding)
        y_pred = self.fc1(lstm_out)
        return -self.crf.forward(y_pred, target, mask, reduction='mean')


class BILSTM_CRF_BERT(nn.Module):
    def __init__(self, bert_config):
        super().__init__()
        # self.embed = nn.Embedding(VOCAB_SIZE, EMBEDDING_DIM)
        self.bert = BertModel(config=bert_config)
        self.lstm = nn.LSTM(EMBEDDING_DIM, HIDDEN_SIZE, bidirectional=True, batch_first=True)
        self.fc1 = nn.Linear(HIDDEN_SIZE * 2, TARGET_SIZE)
        self.crf = CRF(TARGET_SIZE, batch_first=True)

    def forward(self, x, mask):
        # embedding = self.embed(x)
        embedding = self.bert(x)
        embedding = embedding[0]
        lstm_out, _ = self.lstm(embedding)
        tag_space = self.fc1(lstm_out)
        return self.crf.decode(tag_space, mask)

    def loss_fn(self, input, target, mask):
        # embedding = self.embed(input)
        embedding = self.bert(input)[0]
        lstm_out, _ = self.lstm(embedding)
        y_pred = self.fc1(lstm_out)
        return -self.crf.forward(y_pred, target, mask, reduction='mean')


class LSTM_CRF_BERT(nn.Module):
    def __init__(self, bert_config):
        super().__init__()
        self.embed = nn.Embedding(VOCAB_SIZE, EMBEDDING_DIM)
        self.bert = BertModel(config=bert_config)
        self.lstm = nn.LSTM(EMBEDDING_DIM, HIDDEN_SIZE, batch_first=True)
        self.fc1 = nn.Linear(HIDDEN_SIZE, TARGET_SIZE)
        self.crf = CRF(TARGET_SIZE, batch_first=True)

    def forward(self, x, mask):
        # embedding = self.embed(x)
        embedding = self.bert(x)
        embedding = embedding[0]
        lstm_out, _ = self.lstm(embedding)
        tag_space = self.fc1(lstm_out)
        return self.crf.decode(tag_space, mask)

    def loss_fn(self, input, target, mask):
        # embedding = self.embed(input)
        embedding = self.bert(input)[0]
        lstm_out, _ = self.lstm(embedding)
        y_pred = self.fc1(lstm_out)
        return -self.crf.forward(y_pred, target, mask, reduction='mean')


if __name__ == '__main__':
    model1 = Model()
    input = torch.randint(0, 3000, (100, 50))
    print(model1)
