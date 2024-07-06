import torch.optim as optim
from transformers import BertTokenizer
from torch.utils.data import DataLoader
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
from demo.utils import *
import torch
import torch.nn as nn
import torch.nn.functional as F

class AttBiLSTM(nn.Module):
    def __init__(self, embedding_dim, hidden_size, num_classes, vocab_size, dropout=0.5):
        super(AttBiLSTM, self).__init__()
        self.embedding_dim = embedding_dim
        self.hidden_size = hidden_size
        self.num_classes = num_classes
        # Word embedding layer
        self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
        # Bidirectional LSTM layer
        self.bilstm = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_size, batch_first=True, bidirectional=True)
        # Attention layer
        self.attention = nn.Linear(hidden_size * 2, 1)
        # Fully connected layer
        self.fc = nn.Linear(hidden_size * 2, num_classes)
        # Dropout layer
        self.dropout = nn.Dropout(dropout)

    def forward(self, input_ids, attention_mask):
        # Embedding layer
        embedded = self.embedding(input_ids)  # (batch_size, seq_length, embedding_dim)
        # Bidirectional LSTM layer
        output, _ = self.bilstm(embedded)  # (batch_size, seq_length, hidden_size*2)
        # Attention mechanism
        attention_weights = F.softmax(self.attention(output), dim=1)  # (batch_size, seq_length, 1)
        attention_output = torch.sum(output * attention_weights, dim=1)  # (batch_size, hidden_size*2)
        # Dropout
        output = self.dropout(attention_output)
        # Fully connected layer
        logits = self.fc(output)
        return logits

# Load the BERT tokenizer from a local directory
model_path = r'D:\bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_path)

# Load label to index mapping and create reverse mapping
label_to_index = load_label_to_index('label2id.json')
index_to_label = {v: k for k, v in label_to_index.items()}

# Load data and create DataLoader
dataset = load_data(r'.\WebNLG\new_train.json', label_to_index, tokenizer, 64)
dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

# Model, loss function, and optimizer
hidden_size = 768  # Since using 'bert-base-uncased'
num_of_class = len(label_to_index)
model = AttBiLSTM(128, hidden_size=hidden_size, num_classes=num_of_class, vocab_size=tokenizer.vocab_size)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Move model and criterion to CUDA device if available
model.to(device)
criterion.to(device)

# Training loop with loss, accuracy, and F1 score calculation
for epoch in range(50):
    total_loss = 0
    total_correct = 0
    total_samples = 0
    predictions = []
    true_labels = []

    for input_ids, attention_mask, label_id in dataloader:
        optimizer.zero_grad()

        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        label_id = label_id.to(device)

        output = model(input_ids, attention_mask)
        loss = criterion(output, label_id)
        total_loss += loss.item()

        _, predicted = torch.max(output, 1)
        total_correct += (predicted == label_id).sum().item()
        total_samples += label_id.size(0)

        predictions.extend(predicted.cpu().numpy())
        true_labels.extend(label_id.cpu().numpy())

        loss.backward()
        optimizer.step()

    epoch_loss = total_loss / len(dataloader)
    accuracy = total_correct / total_samples
    f1 = f1_score(true_labels, predictions, average='weighted')

    print(f"Epoch {epoch + 1}, Loss: {epoch_loss:.4f}, Accuracy: {accuracy:.4f}, F1 Score: {f1:.4f}")
