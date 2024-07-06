# -*- encoding: utf-8 -*-
import torch.nn as nn
import torch
import torch.nn.functional as F


# class AttBiLSTM(nn.Module):
#     def __init__(self, vocab_size, embedding_dim, hidden_size, num_of_class, weights=None):
#         super(AttBiLSTM, self).__init__()
#         self.vocab_size = vocab_size
#         self.hidden_size = hidden_size
#         self.num_of_class = num_of_class
#         self.embedding_dim = embedding_dim
#         if weights is not None:
#             self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim, _weight=weights)
#         else:
#             self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
#
#         self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=self.hidden_size, batch_first=True,
#                             bidirectional=True)
#         self.self_attention = nn.MultiheadAttention(embed_dim=2 * self.hidden_size, num_heads=1)
#         self.dropout = nn.Dropout(0.2)
#
#         self.attention = nn.Sequential(
#             nn.Linear(2 * self.hidden_size, 1),
#             nn.Tanh(),
#             nn.Softmax(dim=1)
#         )
#         self.fc = nn.Linear(self.hidden_size * 2, self.num_of_class)
#
#     def forward(self, X):
#         input = self.embedding(X)  # input : [batch_size, len_seq, embedding_dim]
#         batch_size = len(X)
#         hidden_state = torch.zeros(1 * 2, batch_size, self.hidden_size).to(input.device)
#         cell_state = torch.zeros(1 * 2, batch_size, self.hidden_size).to(input.device)
#         lstm_out, _ = self.lstm(input, (hidden_state, cell_state))
#         lstm_out = self.dropout(lstm_out)
#         attention_weights = self.attention(lstm_out)
#         attention_output = torch.sum(attention_weights * lstm_out, dim=1)
#         return self.fc(attention_output)


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

        # Additional LSTM layer
        self.lstm2 = nn.LSTM(input_size=2 * self.hidden_size, hidden_size=self.hidden_size, batch_first=True,
                             bidirectional=True)

        # Increase dropout rate
        self.dropout = nn.Dropout(0.5)

        # Batch normalization layer
        self.batch_norm = nn.BatchNorm1d(2 * self.hidden_size)

        # Adjusted attention mechanism
        self.attention = nn.Sequential(
            nn.Linear(2 * self.hidden_size, 64),
            nn.Tanh(),
            nn.Linear(64, 1),
            nn.Softmax(dim=1)
        )

        # Additional fully connected layer
        self.fc2 = nn.Linear(self.hidden_size * 2, self.hidden_size)

        self.fc = nn.Linear(self.hidden_size, self.num_of_class)

    def forward(self, X):
        input = self.embedding(X)  # input : [batch_size, len_seq, embedding_dim]
        lstm_out, _ = self.lstm(input)
        lstm_out2, _ = self.lstm2(lstm_out)

        # Apply dropout
        lstm_out2 = self.dropout(lstm_out2)
        lstm_out2 = lstm_out2.permute(0, 2, 1)
        # Batch normalization
        lstm_out2 = self.batch_norm(lstm_out2)
        lstm_out2 = lstm_out2.permute(0, 2, 1)

        # Adjusted attention mechanism
        attention_weights = self.attention(lstm_out2)

        # Additional fully connected layer
        attention_output = torch.sum(attention_weights * lstm_out2, dim=1)
        attention_output = F.relu(self.fc2(attention_output))

        return self.fc(attention_output)