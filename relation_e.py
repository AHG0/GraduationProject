import json
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertModel
import torch
import torch.nn.functional as F


# 加载数据
def load_data():
    with open(r'D:\CAIL2018_ALL_DATA\信息抽取_第一阶段\step1_train.json', 'r', encoding='utf-8') as f:
        papers = []
        for line in f.readlines():
            dic = json.loads(line)
            papers.append(dic)
    # rel_list = []
    for i in range(len(papers) - 1):
        data = papers[i]

        # # 提取标签个数
        # for e_relation in data['relationMentions']:
        #     rel_list.append(e_relation['label'])

        # 提取文本
        text = []
        text.append(data['sentText'])

        # 提取实体
        entities = []
        for entity in data['entityMentions']:
            entities.append({
                'text': entity['text'],
                'label': entity['label']
            })

        # 提取关系
        relations = []
        for relation in data['relationMentions']:
            relations.append({
                'entity1': relation['em1Text'],
                'e_relation': relation['label'],
                'entity2': relation['em2Text']
            })

        # 输出实体和关系
        output = {
            'text': text,
            'entities': entities,
            'relations': relations
        }
    # with open('e_relation.txt', 'a', encoding='utf-8') as f:
    #     for i in list(set(rel_list)):
    #         f.write(i)
    #         f.write('\n')
    return json.dumps(output, ensure_ascii=False, indent=2)


def text_to_vector(text):
    tokenizer = BertTokenizer.from_pretrained(r'D:\bert-base-chinese')
    bert = BertModel.from_pretrained(r'D:\bert-base-chinese')
    encoded_dict = tokenizer.encode_plus(text, max_length=64,
                                         padding='max_length', truncation=True,
                                         return_attention_mask=True, return_tensors='pt')
    input_ids = encoded_dict['input_ids']
    attention_mask = encoded_dict['attention_mask']

    # Get BERT embeddings for the text
    with torch.no_grad():
        outputs = bert(input_ids, attention_mask=attention_mask)
        embeddings = outputs.last_hidden_state

    # Average embeddings across each token in the text
    embeddings_mean = torch.mean(embeddings, dim=1)

    # Print embeddings shape
    # print(embeddings_mean)  # Output: torch.Size([1, 768])
    return embeddings_mean


text_to_vector("我要考复旦")


def label_to_int(label):
    label_list = ['cat', 'dog', 'bird', 'fish']  # 标签列表
    label_to_int = {label: i for i, label in enumerate(label_list)}
    return label_to_int


def relation2id(relationPath):
    dic = []
    with open(relationPath, 'r', encoding='utf-8') as f:
        for i in f.readlines():
            temp = []
            temp.append(i[0])
            temp.append(int(i.strip().split("|||")[1]))
            dic.append(temp)
    di = dict(dic)
    return di


# relation2id(r'D:\Users\17614\PycharmProjects\BiLSTM_CRF_NER\output\e_relation.txt')


class RelationExtractionDataset(Dataset):
    def __init__(self, sentences, entity_pairs, labels):
        # self.texts = [text_to_vector(text) for text in data.texts]
        # self.labels = [label_to_int(label) for label in data.labels]
        self.sentences = sentences
        self.entity_pairs = entity_pairs
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        sentence = self.sentences[idx]
        entity_pair = self.entity_pairs[idx]
        label = self.labels[idx]
        return sentence, entity_pair, label


class BiLSTM_ATT(nn.Module):
    def __init__(self, config, embedding_pre):
        super(BiLSTM_ATT, self).__init__()
        self.batch = config['BATCH']

        self.embedding_size = config['EMBEDDING_SIZE']
        self.embedding_dim = config['EMBEDDING_DIM']

        self.hidden_dim = config['HIDDEN_DIM']
        self.tag_size = config['TAG_SIZE']

        self.pos_size = config['POS_SIZE']
        self.pos_dim = config['POS_DIM']

        self.pretrained = config['pretrained']
        if self.pretrained:
            # self.word_embeds.weight.data.copy_(torch.from_numpy(embedding_pre))
            self.word_embeds = nn.Embedding.from_pretrained(torch.FloatTensor(embedding_pre), freeze=False)
        else:
            self.word_embeds = nn.Embedding(self.embedding_size, self.embedding_dim)

        self.pos1_embeds = nn.Embedding(self.pos_size, self.pos_dim)
        self.pos2_embeds = nn.Embedding(self.pos_size, self.pos_dim)
        self.relation_embeds = nn.Embedding(self.tag_size, self.hidden_dim)

        self.lstm = nn.LSTM(input_size=self.embedding_dim + self.pos_dim * 2, hidden_size=self.hidden_dim // 2,
                            num_layers=1, bidirectional=True)
        self.hidden2tag = nn.Linear(self.hidden_dim, self.tag_size)

        self.dropout_emb = nn.Dropout(p=0.5)
        self.dropout_lstm = nn.Dropout(p=0.5)
        self.dropout_att = nn.Dropout(p=0.5)

        self.hidden = self.init_hidden()

        self.att_weight = nn.Parameter(torch.randn(self.batch, 1, self.hidden_dim))
        self.relation_bias = nn.Parameter(torch.randn(self.batch, self.tag_size, 1))

    def init_hidden(self):
        return torch.randn(2, self.batch, self.hidden_dim // 2)

    def init_hidden_lstm(self):
        return (torch.randn(2, self.batch, self.hidden_dim // 2),
                torch.randn(2, self.batch, self.hidden_dim // 2))

    def attention(self, H):
        M = F.tanh(H)
        a = F.softmax(torch.bmm(self.att_weight, M), 2)
        a = torch.transpose(a, 1, 2)
        return torch.bmm(H, a)

    def forward(self, sentence, pos1, pos2):

        self.hidden = self.init_hidden_lstm()

        embeds = torch.cat((self.word_embeds(sentence), self.pos1_embeds(pos1), self.pos2_embeds(pos2)), 2)

        embeds = torch.transpose(embeds, 0, 1)

        lstm_out, self.hidden = self.lstm(embeds, self.hidden)

        lstm_out = torch.transpose(lstm_out, 0, 1)
        lstm_out = torch.transpose(lstm_out, 1, 2)

        lstm_out = self.dropout_lstm(lstm_out)
        att_out = F.tanh(self.attention(lstm_out))
        # att_out = self.dropout_att(att_out)

        relation = torch.tensor([i for i in range(self.tag_size)], dtype=torch.long).repeat(self.batch, 1)

        relation = self.relation_embeds(relation)

        res = torch.add(torch.bmm(relation, att_out), self.relation_bias)

        res = F.softmax(res, 1)

        return res.view(self.batch, -1)

# # 定义模型和优化器
# model = BiLSTM_ATT(vocab_size, embedding_dim, hidden_dim, num_classes)
# optimizer = optim.Adam(model.parameters(), lr=0.001)
#
# # 加载数据集和进行训练
# train_dataset = RelationDataset(train_data)
# train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
#
# for epoch in range(num_epochs):
#     for inputs, labels in train_loader:
#         # 将数据传入模型进行训练
#         optimizer.zero_grad()
#         outputs = model(inputs)
#         loss = nn.CrossEntropyLoss()(outputs, labels)
#         loss.backward()
#         optimizer.step()
#
#
# # 预测新的数据
# def predict(text):
#     # 预处理输入的文本
#     input_vector = text_to_vector(text)
#
#     # 将文本转换为张量
#     input_tensor = torch.tensor(input_vector)
#
#     # 使用训练好的模型进行预测
#     model.eval()
#     with torch.no_grad():
#         output = model(input_tensor.unsqueeze(0))
#         predicted_label = torch.argmax(output).item()
#
#     # 将预测结果转换为标签
#     predicted_label = int_to_label(predicted_label)
#
#     return predicted_label
