import torch
import torch.nn as nn
import torch.nn.functional as F


class AttOneBiLSTM(nn.Module):
    def __init__(self, embedding_dim, hidden_size, num_classes, vocab_size, dropout=0.5):
        super(AttOneBiLSTM, self).__init__()
        self.embedding_dim = embedding_dim
        self.hidden_size = hidden_size
        self.num_classes = num_classes
        # 词嵌入层
        self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
        # 双向LSTM层
        self.bilstm = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_size, batch_first=True, bidirectional=True)
        # 注意力层
        self.attention = nn.Linear(hidden_size * 2, 1)
        # 全连接层
        self.fc = nn.Linear(hidden_size * 2, num_classes)
        # Dropout层
        self.dropout = nn.Dropout(dropout)

    def forward(self, input_ids, attention_mask):
        # 词嵌入层
        embedded = self.embedding(input_ids)  # (batch_size, seq_length, embedding_dim)
        # 单层双向LSTM层
        output, _ = self.bilstm(embedded)  # (batch_size, seq_length, hidden_size*2)
        # 注意力机制
        attention_weights = F.softmax(self.attention(output), dim=1)  # (batch_size, seq_length, 1)
        attention_output = torch.sum(output * attention_weights, dim=1)  # (batch_size, hidden_size*2)
        # Dropout
        output = self.dropout(attention_output)
        # 全连接层
        logits = self.fc(output)
        return logits


class AttTwoBiLSTM(nn.Module):
    def __init__(self, embedding_dim, hidden_size, num_classes, vocab_size, dropout=0.5):
        super(AttTwoBiLSTM, self).__init__()
        self.embedding_dim = embedding_dim
        self.hidden_size = hidden_size
        self.num_classes = num_classes
        # 词嵌入层
        self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
        # 双向LSTM层
        self.bilstm1 = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_size, batch_first=True, bidirectional=True)
        self.bilstm2 = nn.LSTM(input_size=hidden_size * 2, hidden_size=hidden_size, batch_first=True,
                               bidirectional=True)
        # 注意力层
        # self.attention = nn.Linear(hidden_size * 2, 1)
        self.attention = nn.Sequential(
            nn.Linear(2 * self.hidden_size, 64),
            nn.Tanh(),
            nn.Linear(64, 1),
            nn.Softmax(dim=1)
        )
        # 全连接层
        self.fc = nn.Linear(hidden_size * 2, num_classes)
        # Dropout层
        self.dropout = nn.Dropout(dropout)

    def forward(self, input_ids, attention_mask):
        # 词嵌入层
        embedded = self.embedding(input_ids)  # (batch_size, seq_length, embedding_dim)
        # 第一层双向LSTM
        output, _ = self.bilstm1(embedded)  # (batch_size, seq_length, hidden_size*2)
        # 第二层双向LSTM
        output, _ = self.bilstm2(output)
        # 注意力机制
        attention_weights = F.softmax(self.attention(output), dim=1)  # (batch_size, seq_length, 1)
        attention_output = torch.sum(output * attention_weights, dim=1)  # (batch_size, hidden_size*2)
        # Dropout
        output = self.dropout(attention_output)
        # 全连接层
        logits = self.fc(output)
        return logits


class BiLSTM_CNN_Attention(nn.Module):
    def __init__(self, embedding_dim, hidden_size, num_classes, vocab_size, dropout=0.5):
        super(BiLSTM_CNN_Attention, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.dropout = nn.Dropout(dropout)
        self.bilstm = nn.LSTM(embedding_dim, hidden_size, bidirectional=True, batch_first=True)
        # Attention mechanism
        self.attention = nn.Linear(hidden_size * 2, 1)
        # Convolutional layer
        self.conv1d = nn.Conv1d(in_channels=hidden_size * 2, out_channels=128, kernel_size=1)
        self.fc = nn.Linear(128, num_classes)

    def forward(self, x, attention_mask):
        embedded = self.embedding(x)
        embedded = self.dropout(embedded)
        # BiLSTM
        lstm_output, _ = self.bilstm(embedded)
        # Attention mechanism
        attention_weights = F.softmax(self.attention(lstm_output), dim=1)
        context_vector = torch.sum(attention_weights * lstm_output, dim=1)
        # Reshape for CNN
        context_vector = context_vector.unsqueeze(2)
        # Convolutional layer
        conv_output = F.relu(self.conv1d(context_vector))
        # Global max pooling
        pooled = F.max_pool1d(conv_output, conv_output.shape[2]).squeeze(2)
        # Fully connected layer
        output = self.fc(pooled)
        return output


class Att1B2F(nn.Module):
    def __init__(self, embedding_dim, hidden_size, num_classes, vocab_size, dropout=0.5, weights=None):
        super(Att1B2F, self).__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_of_class = num_classes
        self.embedding_dim = embedding_dim
        if weights is not None:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim, _weight=weights)
        else:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=self.hidden_size, batch_first=True,
                            bidirectional=True)
        self.dropout = nn.Dropout(dropout)
        self.attention = nn.Sequential(
            nn.Linear(2 * self.hidden_size, self.hidden_size // 2),
            nn.Tanh(),
            nn.Linear(self.hidden_size // 2, 1),
            nn.Softmax(dim=1)
        )
        self.fc2 = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.fc = nn.Linear(self.hidden_size, self.num_of_class)

    def forward(self, X, attention_mask):
        embedding = self.embedding(X)  # input : [batch_size, len_seq, embedding_dim]
        lstm_out, _ = self.lstm(embedding)
        lstm_out = self.dropout(lstm_out)
        attention_weights = self.attention(lstm_out)
        attention_output = torch.sum(attention_weights * lstm_out, dim=1)
        attention_output = F.relu(self.fc2(attention_output))
        return self.fc(attention_output)


class Att1B2F_2CNN(nn.Module):
    def __init__(self, embedding_dim, hidden_size, num_classes, vocab_size, dropout=0.5, weights=None):
        super(Att1B2F_2CNN, self).__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_of_class = num_classes
        self.embedding_dim = embedding_dim
        if weights is not None:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim, _weight=weights)
        else:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=self.hidden_size, batch_first=True,
                            bidirectional=True)
        self.dropout = nn.Dropout(dropout)
        self.attention = nn.Sequential(
            nn.Linear(2 * self.hidden_size, self.hidden_size // 2),
            nn.Tanh(),
            nn.Linear(self.hidden_size // 2, 1),
            nn.Softmax(dim=1)
        )
        self.conv1d = nn.Conv1d(in_channels=self.hidden_size * 2, out_channels=self.hidden_size, kernel_size=3,
                                padding=1)
        self.conv2d = nn.Conv1d(in_channels=self.hidden_size, out_channels=self.hidden_size // 2, kernel_size=3,
                                padding=1)
        self.fc = nn.Linear(self.hidden_size // 2, self.num_of_class)

    def forward(self, X, attention_mask):
        embedding = self.embedding(X)  # input : [batch_size, len_seq, embedding_dim]
        lstm_out, _ = self.lstm(embedding)
        lstm_out = self.dropout(lstm_out)
        attention_weights = self.attention(lstm_out)
        context_vector = torch.sum(attention_weights * lstm_out, dim=1)
        context_vector = context_vector.unsqueeze(2)
        conv_output = F.relu(self.conv1d(context_vector))
        conv_output = F.relu(self.conv2d(conv_output))
        pooled = F.max_pool1d(conv_output, conv_output.shape[2]).squeeze(2)
        output = self.fc(pooled)
        return output
