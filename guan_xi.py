import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# 准备数据
sentences = [
    "湛江市麻章区人民检察院指控，被告人林某某为了赚取利润，承诺帮一名不认识名字的青年男子将十粒毒品（海洛因）放在其养猪场代为销售。",
    "2014年8月7日早上7时许，吸毒人员徐某某来到林某某的养猪场购买毒品，当两人完成交易时，被公安民警当场抓获，并从徐某某身上扣押到可疑毒品一粒和人民币50元，从林某某处扣押到人民币100元和可疑毒品九小粒。",
    "经鉴定，查获的可疑毒品一粒，净重0.07克，可疑毒品九粒，净重0.44克，均检见海洛因成分."
]

# 关系标签
relation_labels = ["NA", "traffic_in", "sell_drugs_to"]

# 将文本转换为词汇
word_to_idx = {}
idx_to_word = {}
words = set()

for sentence in sentences:
    for word in sentence.split():
        if word not in words:
            word_to_idx[word] = len(word_to_idx)
            idx_to_word[len(idx_to_word)] = word
            words.add(word)


# 构建关系抽取模型
class RelationExtractor(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(RelationExtractor, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, sentence):
        embedded = self.embedding(sentence)
        lstm_out, _ = self.lstm(embedded)
        output = self.fc(lstm_out)
        return output


# 创建模型实例
vocab_size = len(word_to_idx)
embedding_dim = 100
hidden_dim = 128
output_dim = len(relation_labels)

model = RelationExtractor(vocab_size, embedding_dim, hidden_dim, output_dim)

# 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)


# 数据预处理
def preprocess_text(text, word_to_idx):
    tokens = text.split()
    indexed_tokens = [word_to_idx[token] for token in tokens if token in word_to_idx]
    return torch.LongTensor(indexed_tokens)


# 准备训练数据
train_data = [(preprocess_text(sent, word_to_idx), relation_labels.index("sell_drugs_to")) for sent in sentences]

# 训练模型
num_epochs = 100

for epoch in range(num_epochs):
    total_loss = 0
    for sentence, label in train_data:
        optimizer.zero_grad()
        output = model(sentence)
        output = output[-1, :, :]  # 使用最后一个时间步的输出
        loss = criterion(output, torch.LongTensor([label]))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f'Epoch {epoch + 1}, Loss: {total_loss / len(train_data)}')


# 预测关系
def predict_relation(text, model, word_to_idx, relation_labels):
    with torch.no_grad():
        sentence = preprocess_text(text, word_to_idx)
        output = model(sentence)
        output = output[-1, :, :]  # 使用最后一个时间步的输出
        _, predicted = torch.max(output, 1)
        relation = relation_labels[predicted]
        return relation


# 示例预测
sample_text = "林某某为了赚取利润，承诺帮一名不认识名字的青年男子将十粒毒品（海洛因）放在其养猪场代为销售。"
predicted_relation = predict_relation(sample_text, model, word_to_idx, relation_labels)
print(f'Predicted Relation: {predicted_relation}')
