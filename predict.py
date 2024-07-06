# -*- coding: UTF-8 -*-
import sys
from utils import *
from model import *
from config import *
import torch
import sys
from e_relation import test6

sys.path.append(r'D:\Users\17614\PycharmProjects\BiLSTM_Attention\predict_rlt.py')


def model(text):
    _, word2id = get_vocab()
    input = torch.tensor([[word2id.get(w, WORD_UNK_ID) for w in text]])
    # print(len(text))
    # print(input.size())
    # print(input)
    mask = torch.tensor([[1] * len(text)]).bool()

    input = input.cuda()
    mask = mask.cuda()

    # model = torch.load(MODEL_DIR + 'model_ner.pth', map_location=torch.device('cuda'))
    model = torch.load(r"D:\Users\17614\PycharmProjects\BiLSTM_CRF_NER\output\model\model_ner.pth",
                       map_location=torch.device('cuda'))
    y_pred = model(input, mask)
    id2label, _ = get_label()
    # print(id2label)
    # print(y_pred[0])
    # label = y_pred[0].detach().cpu().numpy().tolist()
    label = y_pred[0]
    label = [id2label[l - 1] for l in label]
    # print(text)
    print(label)

    info = extract1(label, text)
    info_ = ["实体类1", "实体类2", "实体类3"]
    dic_info = dict(zip(info_, info))

    for key, value in dic_info.items():
        print("".join(key) + "：" + ",".join(value))


# def model(text):
#     _, word2id = get_vocab()
#     input = torch.tensor([[word2id.get(w, WORD_UNK_ID) for w in text]])
#     mask = torch.tensor([[1] * len(text)]).bool()
#
#     input = input.cuda()
#     mask = mask.cuda()
#
#     model = torch.load(MODEL_DIR + 'model_ner.pth')
#     y_pred = model(input, mask)
#     id2label, _ = get_label()
#     label = [id2label[l] for l in y_pred[0]]
#     print(text)
#     # print(label)
#
#     info = extract1(label, text)
#     info_ = ["人物", "时间", "物品", "数量", "地点"]
#     dic_info = dict(zip(info_, info))
#
#     for key, value in dic_info.items():
#         print("".join(key) + "：" + ",".join(value))


def bilstm_crf_bert(text):
    _, word2id = get_vocab()
    input = torch.tensor([[word2id.get(w, WORD_UNK_ID) for w in text]])
    mask = torch.tensor([[1] * len(text)]).bool()

    input = input.cuda()
    mask = mask.cuda()

    model = torch.load(MODEL_DIR + 'model_5_bilstm-crf_bert.pth')
    y_pred = model(input, mask)
    id2label, _ = get_label()
    label = [id2label[l] for l in y_pred[0]]
    print(text)
    # print(label)

    info = extract(label, text)
    info_ = ["人物", "时间", "物品", "数量", "地点"]
    dic_info = dict(zip(info_, info))

    for key, value in dic_info.items():
        print("".join(key) + "：" + ",".join(value))


def bilstm_crf(text):
    _, word2id = get_vocab()
    input = torch.tensor([[word2id.get(w, WORD_UNK_ID) for w in text]])
    mask = torch.tensor([[1] * len(text)]).bool()

    input = input.cuda()
    mask = mask.cuda()

    model = torch.load(MODEL_DIR + 'model_5_bilstm-crf.pth')
    y_pred = model(input, mask)
    id2label, _ = get_label()
    label = [id2label[l] for l in y_pred[0]]
    print(text)
    # print(label)

    info = extract(label, text)
    info_ = ["人物", "时间", "物品", "数量", "地点"]
    dic_info = dict(zip(info_, info))

    for key, value in dic_info.items():
        print("".join(key) + "：" + ",".join(value))


def bilstm(text):
    _, word2id = get_vocab()
    input = torch.tensor([[word2id.get(w, WORD_UNK_ID) for w in text]])
    # mask = torch.tensor([[1] * len(text)]).bool()

    input = input.cuda()

    model = torch.load(MODEL_DIR + '/model/model_4_bilstm.pth')
    y_pred = model(input)
    id2label, _ = get_label()
    y_pred = y_pred.argmax(dim=2).cpu()
    y_pred = y_pred.tolist()

    label = [id2label[l] for l in y_pred[0]]

    info = []

    for i in extract(label, text):
        # 去除实体长度为1的
        list1 = []
        for j in list(set(i)):
            if len(j) == 1:
                continue
            else:
                list1.append(j)
        info.append(list1)

    info_ = ["people", "time", "thing", "num", "place"]
    dic_info = dict(zip(info_, info))
    dic_info.update(test6.find_entity_positions(label, text))
    print(dic_info)

    # for key, value in dic_info.items():
    #     print("".join(key) + "：" + ",".join(value))


def lstm(text):
    _, word2id = get_vocab()
    input = torch.tensor([[word2id.get(w, WORD_UNK_ID) for w in text]])
    # mask = torch.tensor([[1] * len(text)]).bool()

    input = input.cuda()

    model = torch.load(MODEL_DIR + 'model_6_lstm.pth')
    y_pred = model(input)
    id2label, _ = get_label()
    y_pred = y_pred.argmax(dim=2).cpu()
    y_pred = y_pred.tolist()

    label = [id2label[l] for l in y_pred[0]]
    print(text)
    # print(label)

    info = extract(label, text)
    info_ = ["人物", "时间", "物品", "数量", "地点"]
    dic_info = dict(zip(info_, info))

    for key, value in dic_info.items():
        print("".join(key) + "：" + ",".join(value))


def lstm_crf(text):
    _, word2id = get_vocab()
    input = torch.tensor([[word2id.get(w, WORD_UNK_ID) for w in text]])
    mask = torch.tensor([[1] * len(text)]).bool()

    input = input.cuda()
    mask = mask.cuda()

    model = torch.load(MODEL_DIR + 'model_7_lstm-crf.pth')
    y_pred = model(input, mask)
    id2label, _ = get_label()
    label = [id2label[l] for l in y_pred[0]]
    print(text)
    # print(label)

    info = extract(label, text)
    info_ = ["人物", "时间", "物品", "数量", "地点"]
    dic_info = dict(zip(info_, info))

    for key, value in dic_info.items():
        print("".join(key) + "：" + ",".join(value))


def crf(text):
    _, word2id = get_vocab()
    input = torch.tensor([[word2id.get(w, WORD_UNK_ID) for w in text]])
    mask = torch.tensor([[1] * len(text)]).bool()

    input = input.cuda()
    mask = mask.cuda()

    model = torch.load(MODEL_DIR + 'model_8_crf.pth')
    y_pred = model(input, mask)
    id2label, _ = get_label()
    label = [id2label[l] for l in y_pred[0]]
    print(text)
    # print(label)

    info = extract(label, text)
    info_ = ["人物", "时间", "物品", "数量", "地点"]
    dic_info = dict(zip(info_, info))
    print(dic_info)

    # for key, value in dic_info.items():
    #     print("".join(key) + "：" + ",".join(value))


class BiLSTM_CRF(nn.Module):
    def __init__(self, bert_config):
        super().__init__()
        self.embed = nn.Embedding(VOCAB_SIZE, EMBEDDING_DIM)
        self.lstm = nn.LSTM(
            EMBEDDING_DIM,
            HIDDEN_SIZE,
            batch_first=True,
            bidirectional=True,
        )
        self.fc1 = nn.Linear(HIDDEN_SIZE * 2, 1000)
        self.fc2 = nn.Linear(1000, 6)
        self.crf = CRF(TARGET_SIZE, batch_first=True)

    def _get_lstm_feature(self, input):
        out = self.embed(input)
        out, _ = self.lstm(out)
        out = self.fc1(out)
        return self.fc2(out)

    def forward(self, input, mask):
        out = self._get_lstm_feature(input)
        return self.crf.decode(out, mask)

    def loss_fn(self, input, target, mask):
        y_pred = self._get_lstm_feature(input)
        return -self.crf.forward(y_pred, target, mask, reduction='mean')


if __name__ == '__main__':
    # text = """经审理查明：2014年6月至8月期间，被告人喻某经事先电话联系后，在无锡市新区南星苑六区380号、泰伯花园一期南门等地附近，向黄某、杨某贩卖毒品6次，计贩卖甲基苯丙胺约1.8克。具体事实如下："""
    # bilstm(text)
    bilstm(sys.argv[1])
    # model(text)