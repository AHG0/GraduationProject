import numpy as np
from transformers import BertConfig
from utils import *
from model import *
from config import *
import matplotlib.pyplot as plt
import torch
from sklearn.metrics import recall_score, f1_score

if __name__ == '__main__':
    dataset = Dataset()
    loader = data.DataLoader(
        dataset,
        batch_size=16,
        shuffle=True,
        collate_fn=collate_fn,
        num_workers=0
    )

    losses = []
    step = 0

    bert_config = BertConfig.from_pretrained(r'D:\chinese_L-12_H-768_A-12\bert_config.json')
    model = BILSTM_CRF_BERT(bert_config).cuda()
    optimizer = torch.optim.SGD(model.parameters(), lr=LR)

    accuracies, recalls, f1_scores = [], [], []

    for e in range(EPOCH):
        y_true_list = []
        y_pred_list = []
        for b, (input, target, mask) in enumerate(loader):
            input = input.cuda()
            target = target.cuda()
            mask = mask.cuda()

            y_pred = model(input, mask)

            optimizer.zero_grad()
            loss = model.loss_fn(input, target, mask)
            loss.backward()
            optimizer.step()

            # Concatenate predictions
            for lst in y_pred:
                y_pred_list += lst
            for y, m in zip(target, mask):
                y_true_list += y[m == True].tolist()

        # Calculate overall accuracy
        y_true_tensor = torch.tensor(y_true_list)
        y_pred_tensor = torch.tensor(y_pred_list)
        accuracy = (y_true_tensor == y_pred_tensor).sum() / len(y_true_tensor)
        accuracies.append(accuracy)

        # Calculate recall and F1 score
        recall = recall_score(y_true_tensor, y_pred_tensor, average='macro', zero_division=1)  # Specify zero_division
        recalls.append(recall)
        f1 = f1_score(y_true_tensor, y_pred_tensor, average='macro')
        f1_scores.append(f1)
        losses.append(loss.item())
        print(
            f' >> epoch:{e + 1}/{EPOCH}, loss:{loss.item()}, accuracy:{accuracy.item():.4f}, recall:{recall:.4f}, F1 Score:{f1:.4f}')

    # Save the model
    torch.save(model, MODEL_DIR + f'model/model_10_bilstm-crf_bert.pth')

    epochs_range = np.arange(1, EPOCH + 1)

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, losses, label='Training Loss')
    plt.title(f'Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, accuracies, label='Accuracy', linestyle='dashed')
    plt.plot(epochs_range, recalls, label='Recall', linestyle='dashdot')
    plt.plot(epochs_range, f1_scores, label='F1 Score', linestyle=':')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title(f'Acc Rec F1')
    plt.xlabel('Epochs')
    plt.ylabel('Score')
    plt.legend()

    plt.tight_layout()
    plt.show()
