# -*- encoding: utf-8 -*-
import torch.nn as nn
import torch
import torch.nn.functional as F


class AttBiLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class, weights=None):
        super(AttBiLSTM, self).__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_of_class = num_of_class
        self.embedding_dim = embedding_dim
        if weights is not None:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim, _weight=weights)
        else:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=self.hidden_size, batch_first=True,
                            bidirectional=True)
        self.lstm2 = nn.LSTM(input_size=2 * self.hidden_size, hidden_size=self.hidden_size, batch_first=True,
                             bidirectional=True)
        self.dropout = nn.Dropout(0.5)
        self.attention = nn.Sequential(
            nn.Linear(2 * self.hidden_size, 64),
            nn.Tanh(),
            nn.Linear(64, 1),
            nn.Softmax(dim=1)
        )
        self.fc2 = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.fc = nn.Linear(self.hidden_size, self.num_of_class)

    def forward(self, X):
        embedding = self.embedding(X)  # input : [batch_size, len_seq, embedding_dim]
        lstm_out, _ = self.lstm(embedding)
        lstm_out2, _ = self.lstm2(lstm_out)
        lstm_out2 = self.dropout(lstm_out)
        attention_weights = self.attention(lstm_out2)
        attention_output = torch.sum(attention_weights * lstm_out2, dim=1)
        attention_output = F.relu(self.fc2(attention_output))
        return self.fc(attention_output)


class Att2B2F(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class, weights=None):
        super(Att2B2F, self).__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_of_class = num_of_class
        self.embedding_dim = embedding_dim
        if weights is not None:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim, _weight=weights)
        else:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=self.hidden_size, batch_first=True,
                            bidirectional=True)
        self.lstm2 = nn.LSTM(input_size=2 * self.hidden_size, hidden_size=self.hidden_size, batch_first=True,
                             bidirectional=True)
        self.dropout = nn.Dropout(0.5)
        self.attention = nn.Sequential(
            nn.Linear(2 * self.hidden_size, 64),
            nn.Tanh(),
            nn.Linear(64, 1),
            nn.Softmax(dim=1)
        )
        self.fc2 = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.fc = nn.Linear(self.hidden_size, self.num_of_class)

    def forward(self, X):
        embedding = self.embedding(X)  # input : [batch_size, len_seq, embedding_dim]
        lstm_out, _ = self.lstm(embedding)
        lstm_out = self.dropout(lstm_out)
        lstm_out2, _ = self.lstm2(lstm_out)
        lstm_out2 = self.dropout(lstm_out)
        attention_weights = self.attention(lstm_out2)
        attention_output = torch.sum(attention_weights * lstm_out2, dim=1)
        attention_output = F.relu(self.fc2(attention_output))
        return self.fc(attention_output)


class Att1B2F(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class, weights=None):
        super(Att1B2F, self).__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_of_class = num_of_class
        self.embedding_dim = embedding_dim
        if weights is not None:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim, _weight=weights)
        else:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=self.hidden_size, batch_first=True,
                            bidirectional=True)
        self.dropout = nn.Dropout(0.5)
        self.attention = nn.Sequential(
            nn.Linear(2 * self.hidden_size, self.hidden_size // 2),
            nn.Tanh(),
            nn.Linear(self.hidden_size // 2, 1),
            nn.Softmax(dim=1)
        )
        self.fc2 = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.fc = nn.Linear(self.hidden_size, self.num_of_class)

    def forward(self, X):
        embedding = self.embedding(X)  # input : [batch_size, len_seq, embedding_dim]
        lstm_out, _ = self.lstm(embedding)
        lstm_out = self.dropout(lstm_out)
        attention_weights = self.attention(lstm_out)
        attention_output = torch.sum(attention_weights * lstm_out, dim=1)
        attention_output = F.relu(self.fc2(attention_output))
        return self.fc(attention_output)


class Att1B2F_2CNN(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class, weights=None):
        super(Att1B2F_2CNN, self).__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_of_class = num_of_class
        self.embedding_dim = embedding_dim
        if weights is not None:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim, _weight=weights)
        else:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=self.hidden_size, batch_first=True,
                            bidirectional=True)
        self.dropout = nn.Dropout(0.5)
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

    def forward(self, X):
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


class Att2B1F(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class, weights=None):
        super(Att2B1F, self).__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_of_class = num_of_class
        self.embedding_dim = embedding_dim
        if weights is not None:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim, _weight=weights)
        else:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
        self.lstm1 = nn.LSTM(input_size=embedding_dim, hidden_size=self.hidden_size, batch_first=True,
                             bidirectional=True)
        self.lstm2 = nn.LSTM(input_size=self.hidden_size * 2, hidden_size=self.hidden_size, batch_first=True,
                             bidirectional=True)

        self.dropout = nn.Dropout(0.5)

        self.attention = nn.Sequential(
            nn.Linear(2 * self.hidden_size, self.hidden_size // 2),
            nn.Tanh(),
            nn.Linear(self.hidden_size // 2, 1),
            nn.Softmax(dim=1)
        )

        self.fc = nn.Linear(self.hidden_size * 2, self.num_of_class)

    def forward(self, X):
        embedding = self.embedding(X)  # input : [batch_size, len_seq, embedding_dim]

        lstm_out1, _ = self.lstm1(embedding)
        lstm_out1 = self.dropout(lstm_out1)

        lstm_out2, _ = self.lstm2(lstm_out1)
        lstm_out2 = self.dropout(lstm_out2)

        attention_weights = self.attention(lstm_out2)
        attention_output = torch.sum(attention_weights * lstm_out2, dim=1)
        attention_output = self.dropout(attention_output)
        return self.fc(attention_output)


class Att1B1F(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class, weights=None):
        super(Att1B1F, self).__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_of_class = num_of_class
        self.embedding_dim = embedding_dim
        if weights is not None:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim, _weight=weights)
        else:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
        self.lstm1 = nn.LSTM(input_size=embedding_dim, hidden_size=self.hidden_size, batch_first=True,
                             bidirectional=True)
        self.lstm2 = nn.LSTM(input_size=self.hidden_size * 2, hidden_size=self.hidden_size, batch_first=True,
                             bidirectional=True)
        self.dropout = nn.Dropout(0.5)
        self.attention = nn.Sequential(
            nn.Linear(2 * self.hidden_size, 64),
            nn.Tanh(),
            nn.Linear(64, 1),
            nn.Softmax(dim=1)
        )
        self.fc = nn.Linear(self.hidden_size * 2, self.num_of_class)

    def forward(self, X):
        embedding = self.embedding(X)  # input : [batch_size, len_seq, embedding_dim]
        lstm_out1, _ = self.lstm1(embedding)
        # lstm_out1 = self.dropout(lstm_out1)
        lstm_out1 = torch.tanh(lstm_out1)
        attention_weights = self.attention(lstm_out1)
        attention_output = torch.sum(attention_weights * lstm_out1, dim=1)
        return self.fc(attention_output)


class Att2B1F0D(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class, weights=None):
        super(Att2B1F0D, self).__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_of_class = num_of_class
        self.embedding_dim = embedding_dim
        if weights is not None:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim, _weight=weights)
        else:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
        self.lstm1 = nn.LSTM(input_size=embedding_dim, hidden_size=self.hidden_size, batch_first=True,
                             bidirectional=True)
        self.lstm2 = nn.LSTM(input_size=self.hidden_size * 2, hidden_size=self.hidden_size, batch_first=True,
                             bidirectional=True)
        self.dropout = nn.Dropout(0.5)
        self.attention = nn.Sequential(
            nn.Linear(2 * self.hidden_size, 64),
            nn.Tanh(),
            nn.Linear(64, 1),
            nn.Softmax(dim=1)
        )
        self.fc = nn.Linear(self.hidden_size * 2, self.num_of_class)

    def forward(self, X):
        embedding = self.embedding(X)  # input : [batch_size, len_seq, embedding_dim]
        lstm_out1, _ = self.lstm1(embedding)
        lstm_out2, _ = self.lstm2(lstm_out1)
        attention_weights = self.attention(lstm_out2)
        attention_output = torch.sum(attention_weights * lstm_out2, dim=1)
        return self.fc(attention_output)


class Att1B1F0D(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class, weights=None):
        super(Att1B1F0D, self).__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_of_class = num_of_class
        self.embedding_dim = embedding_dim
        if weights is not None:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim, _weight=weights)
        else:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
        self.lstm1 = nn.LSTM(input_size=embedding_dim, hidden_size=self.hidden_size, batch_first=True,
                             bidirectional=True)
        self.lstm2 = nn.LSTM(input_size=self.hidden_size * 2, hidden_size=self.hidden_size, batch_first=True,
                             bidirectional=True)
        self.dropout = nn.Dropout(0.5)
        self.attention = nn.Sequential(
            nn.Linear(2 * self.hidden_size, 64),
            nn.Tanh(),
            nn.Linear(64, 1),
            nn.Softmax(dim=1)
        )
        self.fc = nn.Linear(self.hidden_size * 2, self.num_of_class)

    def forward(self, X):
        embedding = self.embedding(X)  # input : [batch_size, len_seq, embedding_dim]
        lstm_out1, _ = self.lstm1(embedding)
        attention_weights = self.attention(lstm_out1)
        attention_output = torch.sum(attention_weights * lstm_out1, dim=1)
        return self.fc(attention_output)


class Att2B2FNA(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class, weights=None):
        super(Att2B2FNA, self).__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_of_class = num_of_class
        self.embedding_dim = embedding_dim
        if weights is not None:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim, _weight=weights)
        else:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=self.hidden_size, batch_first=True,
                            bidirectional=True)
        self.lstm2 = nn.LSTM(input_size=2 * self.hidden_size, hidden_size=self.hidden_size, batch_first=True,
                             bidirectional=True)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.fc = nn.Linear(self.hidden_size, self.num_of_class)

    def forward(self, X):
        embedding = self.embedding(X)  # input : [batch_size, len_seq, embedding_dim]
        lstm_out, _ = self.lstm(embedding)
        lstm_out = self.dropout(lstm_out)
        lstm_out2, _ = self.lstm2(lstm_out)
        lstm_out2 = self.dropout(lstm_out)
        lstm_output = torch.sum(lstm_out2, dim=1)  # Sum over the sequence dimension
        lstm_output = F.relu(self.fc2(lstm_output))
        return self.fc(lstm_output)


class Att1B2FNA(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class, weights=None):
        super(Att1B2FNA, self).__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_of_class = num_of_class
        self.embedding_dim = embedding_dim
        if weights is not None:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim, _weight=weights)
        else:
            self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=self.hidden_size, batch_first=True,
                            bidirectional=True)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.fc = nn.Linear(self.hidden_size, self.num_of_class)

    def forward(self, X):
        embedding = self.embedding(X)  # input : [batch_size, len_seq, embedding_dim]
        lstm_out, _ = self.lstm(embedding)
        lstm_out = self.dropout(lstm_out)
        lstm_output = torch.sum(lstm_out, dim=1)  # Sum over the sequence dimension
        lstm_output = F.relu(self.fc2(lstm_output))
        return self.fc(lstm_output)


class BiLSTM_CNN_Attention(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class):
        super(BiLSTM_CNN_Attention, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.dropout = nn.Dropout(0.5)
        self.bilstm = nn.LSTM(embedding_dim, hidden_size, bidirectional=True, batch_first=True)
        # Attention mechanism
        self.attention = nn.Linear(hidden_size * 2, 1)
        # Convolutional layer
        self.conv1d = nn.Conv1d(in_channels=hidden_size * 2, out_channels=128, kernel_size=1)
        self.fc = nn.Linear(128, num_of_class)

    def forward(self, x):
        embedded = self.embedding(x)
        # BiLSTM
        lstm_output, _ = self.bilstm(embedded)
        lstm_output = self.dropout(lstm_output)
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


class TwoBiLSTM_CNN_Attention(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class):
        super(TwoBiLSTM_CNN_Attention, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.dropout = nn.Dropout(0.5)
        # self.bilstm = nn.LSTM(embedding_dim, hidden_size, bidirectional=True, batch_first=True)
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_size, batch_first=True,
                            bidirectional=True)
        self.lstm2 = nn.LSTM(input_size=2 * hidden_size, hidden_size=hidden_size, batch_first=True,
                             bidirectional=True)
        # Attention mechanism
        self.attention = nn.Linear(hidden_size * 2, 1)
        # Convolutional layer
        self.conv1d = nn.Conv1d(in_channels=hidden_size * 2, out_channels=hidden_size, kernel_size=3, padding=1)
        self.conv2d = nn.Conv1d(in_channels=hidden_size, out_channels=hidden_size // 2, kernel_size=3,
                                padding=1)
        self.fc2 = nn.Linear(hidden_size // 2, hidden_size // 4)
        self.fc = nn.Linear(hidden_size // 2, num_of_class)

    def forward(self, x):
        embedding = self.embedding(x)
        # TwoBiLSTM
        lstm_out, _ = self.lstm(embedding)
        lstm_out = self.dropout(lstm_out)
        lstm_out2, _ = self.lstm2(lstm_out)
        lstm_out2 = self.dropout(lstm_out)
        # Attention mechanism
        attention_weights = F.softmax(self.attention(lstm_out2), dim=1)
        context_vector = torch.sum(attention_weights * lstm_out2, dim=1)
        # Reshape for CNN
        context_vector = context_vector.unsqueeze(2)
        # Convolutional layer
        conv_output = F.relu(self.conv1d(context_vector))
        conv_output = F.relu(self.conv2d(conv_output))
        # Global max pooling
        pooled = F.max_pool1d(conv_output, conv_output.shape[2]).squeeze(2)
        # Fully connected layer
        # attention_output = F.relu(self.fc2(pooled))
        return self.fc(pooled)


class TwoBiLSTM_CNN_Attention(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class):
        super(TwoBiLSTM_CNN_Attention, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.dropout = nn.Dropout(0.5)
        # self.bilstm = nn.LSTM(embedding_dim, hidden_size, bidirectional=True, batch_first=True)
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_size, batch_first=True,
                            bidirectional=True)
        self.lstm2 = nn.LSTM(input_size=2 * hidden_size, hidden_size=hidden_size, batch_first=True,
                             bidirectional=True)
        # Attention mechanism
        self.attention = nn.Linear(hidden_size * 2, 1)
        # Convolutional layer
        self.conv1d = nn.Conv1d(in_channels=hidden_size * 2, out_channels=hidden_size, kernel_size=3, padding=1)
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.fc = nn.Linear(hidden_size // 2, num_of_class)

    def forward(self, x):
        embedding = self.embedding(x)
        # TwoBiLSTM
        lstm_out, _ = self.lstm(embedding)
        lstm_out = self.dropout(lstm_out)
        lstm_out2, _ = self.lstm2(lstm_out)
        lstm_out2 = self.dropout(lstm_out)
        # Attention mechanism
        attention_weights = F.softmax(self.attention(lstm_out2), dim=1)
        context_vector = torch.sum(attention_weights * lstm_out2, dim=1)
        # Reshape for CNN
        context_vector = context_vector.unsqueeze(2)
        # Convolutional layer
        conv_output = F.relu(self.conv1d(context_vector))
        # Global max pooling
        pooled = F.max_pool1d(conv_output, conv_output.shape[2]).squeeze(2)
        # Fully connected layer
        output = F.relu(self.fc2(pooled))
        return self.fc(output)


class TwoBiLSTM_CNN_DoubleAttention(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class):
        super(TwoBiLSTM_CNN_DoubleAttention, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.dropout = nn.Dropout(0.5)
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_size, batch_first=True, bidirectional=True)
        self.lstm2 = nn.LSTM(input_size=2 * hidden_size, hidden_size=hidden_size, batch_first=True, bidirectional=True)
        self.attention1 = nn.Linear(hidden_size * 2, 1)
        self.attention2 = nn.Linear(hidden_size * 2, 1)
        self.conv1d = nn.Conv1d(in_channels=hidden_size * 4, out_channels=hidden_size, kernel_size=3, padding=1)
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.fc = nn.Linear(hidden_size // 2, num_of_class)

    def forward(self, x):
        embedding = self.embedding(x)
        lstm_out, _ = self.lstm(embedding)
        lstm_out = self.dropout(lstm_out)
        lstm_out2, _ = self.lstm2(lstm_out)
        lstm_out2 = self.dropout(lstm_out2)
        lstm_out = torch.tanh(lstm_out)
        lstm_out2 = torch.tanh(lstm_out2)
        attention_weights1 = F.softmax(self.attention1(lstm_out), dim=1)
        context_vector1 = torch.sum(attention_weights1 * lstm_out, dim=1)
        attention_weights2 = F.softmax(self.attention2(lstm_out2), dim=1)
        context_vector2 = torch.sum(attention_weights2 * lstm_out2, dim=1)
        avg_context_vector = torch.cat((context_vector1, context_vector2), dim=1)
        avg_context_vector = avg_context_vector.unsqueeze(2)
        conv_output = F.relu(self.conv1d(avg_context_vector))
        pooled = F.max_pool1d(conv_output, conv_output.shape[2]).squeeze(2)
        output = F.relu(self.fc2(pooled))
        return self.fc(output)


class TwoBiLSTM_CNN_TwoAttention(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class):
        super(TwoBiLSTM_CNN_TwoAttention, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.dropout = nn.Dropout(0.5)
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_size, batch_first=True, bidirectional=True)
        self.lstm2 = nn.LSTM(input_size=2 * hidden_size, hidden_size=hidden_size, batch_first=True, bidirectional=True)
        self.attention1 = nn.Linear(hidden_size * 2, 1)
        self.attention2 = nn.Linear(hidden_size * 2, 1)
        self.conv1d = nn.Conv1d(in_channels=hidden_size * 4, out_channels=hidden_size, kernel_size=3, padding=1)
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.fc = nn.Linear(hidden_size // 2, num_of_class)

    def forward(self, x):
        embedding = self.embedding(x)
        lstm_out, _ = self.lstm(embedding)
        lstm_out = self.dropout(lstm_out)
        lstm_out2, _ = self.lstm2(lstm_out)
        lstm_out2 = self.dropout(lstm_out2)
        lstm_out = torch.tanh(lstm_out)
        lstm_out2 = torch.tanh(lstm_out2)
        attention_weights1 = F.softmax(self.attention1(lstm_out), dim=1)
        context_vector1 = torch.sum(attention_weights1 * lstm_out, dim=1)
        attention_weights2 = F.softmax(self.attention2(lstm_out2), dim=1)
        context_vector2 = torch.sum(attention_weights2 * lstm_out2, dim=1)
        avg_context_vector = torch.cat((context_vector1, context_vector2), dim=1)
        avg_context_vector = avg_context_vector.unsqueeze(2)
        conv_output = F.relu(self.conv1d(avg_context_vector))
        pooled = F.max_pool1d(conv_output, conv_output.shape[2]).squeeze(2)
        output = F.relu(self.fc2(pooled))
        return self.fc(output)


class TwoBiLSTM_CNN_TwoAtt(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class):
        super(TwoBiLSTM_CNN_TwoAtt, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.dropout = nn.Dropout(0.5)
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_size, batch_first=True, bidirectional=True)
        self.conv1d = nn.Conv1d(in_channels=hidden_size * 2, out_channels=hidden_size, kernel_size=3, padding=1)
        self.attention = nn.Linear(hidden_size * 2, 1)
        self.fc = nn.Linear(hidden_size, num_of_class)

    def forward(self, x):
        embedding = self.embedding(x)
        lstm_out, _ = self.lstm(embedding)
        lstm_out = self.dropout(lstm_out)
        lstm_out = lstm_out.permute(0, 2, 1)
        conv_output = F.relu(self.conv1d(lstm_out))
        conv_output = conv_output.permute(0, 2, 1)
        attention_weights = F.softmax(self.attention(conv_output), dim=1)
        context_vector = torch.sum(attention_weights * conv_output, dim=1)
        output = F.relu(context_vector)
        output = self.fc(output)
        return output


class TwoBiLSTM_DoubleAttention(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class):
        super(TwoBiLSTM_DoubleAttention, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.dropout = nn.Dropout(0.5)
        self.hidden_size = hidden_size
        self.lstm1 = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_size, batch_first=True, bidirectional=True)
        self.lstm2 = nn.LSTM(input_size=2 * hidden_size, hidden_size=hidden_size, batch_first=True, bidirectional=True)
        # First Attention mechanism
        self.attention1 = nn.Linear(hidden_size * 2, 1)
        # Second Attention mechanism
        self.attention2 = nn.Linear(hidden_size * 2, 1)
        self.fc2 = nn.Linear(hidden_size * 4, hidden_size)
        self.fc = nn.Linear(hidden_size, num_of_class)

    def forward(self, x):
        embedding = self.embedding(x)
        # 第一层BiLSTM层
        lstm_out1, _ = self.lstm1(embedding)
        lstm_out1 = self.dropout(lstm_out1)
        # 第二层BiLSTM层
        lstm_out2, _ = self.lstm2(lstm_out1)
        lstm_out2 = self.dropout(lstm_out2)
        # 第一层注意力
        attention_weights1 = F.softmax(self.attention1(lstm_out1), dim=1)
        context_vector1 = torch.sum(attention_weights1 * lstm_out1, dim=1)
        # 第二层注意力
        attention_weights2 = F.softmax(self.attention2(lstm_out2), dim=1)
        context_vector2 = torch.sum(attention_weights2 * lstm_out2, dim=1)
        # 拼接
        context_vectors = torch.cat((context_vector1, context_vector2), dim=1)
        output = F.relu(self.fc2(context_vectors))
        return self.fc(output)


class ThreeBiLSTM_CNN_ThreeAttention(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class):
        super(ThreeBiLSTM_CNN_ThreeAttention, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.dropout = nn.Dropout(0.5)
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_size, batch_first=True, bidirectional=True)
        self.lstm2 = nn.LSTM(input_size=2 * hidden_size, hidden_size=hidden_size, batch_first=True, bidirectional=True)
        self.lstm3 = nn.LSTM(input_size=2 * hidden_size, hidden_size=hidden_size, batch_first=True, bidirectional=True)
        self.attention1 = nn.Linear(hidden_size * 2, 1)
        self.attention3 = nn.Linear(hidden_size * 2, 1)
        self.conv1d = nn.Conv1d(in_channels=hidden_size * 4, out_channels=hidden_size, kernel_size=3, padding=1)
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.fc = nn.Linear(hidden_size // 2, num_of_class)

    def forward(self, x):
        embedding = self.embedding(x)
        lstm_out, _ = self.lstm(embedding)
        lstm_out = self.dropout(lstm_out)
        lstm_out2, _ = self.lstm2(lstm_out)
        lstm_out2 = self.dropout(lstm_out2)
        lstm_out3, _ = self.lstm3(lstm_out2)
        lstm_out3 = self.dropout(lstm_out3)
        lstm_out = torch.tanh(lstm_out)
        lstm_out3 = torch.tanh(lstm_out3)
        attention_weights1 = F.softmax(self.attention1(lstm_out), dim=1)
        context_vector1 = torch.sum(attention_weights1 * lstm_out, dim=1)
        attention_weights3 = F.softmax(self.attention3(lstm_out3), dim=1)
        context_vector3 = torch.sum(attention_weights3 * lstm_out3, dim=1)
        avg_context_vector = torch.cat((context_vector1, context_vector3), dim=1)
        avg_context_vector = avg_context_vector.unsqueeze(2)
        conv_output = F.relu(self.conv1d(avg_context_vector))
        pooled = F.max_pool1d(conv_output, conv_output.shape[2]).squeeze(2)
        output = F.relu(self.fc2(pooled))
        return self.fc(output)
