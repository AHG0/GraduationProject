from utils import *
from model import *
from sklearn.metrics import accuracy_score, f1_score, recall_score
from test4 import BILSTM_CRF_BERT
from test3 import LSTM
from test2 import LSTM_CRF
from test1 import BiLSTM_CRF

# 加载已保存的模型
model = torch.load(r'D:\Users\17614\PycharmProjects\BiLSTM_CRF_NER\output\model\model_10_bilstm-crf_bert.pth')
model.eval()

torch.manual_seed(2000)

dataset = Dataset('test')
loader = data.DataLoader(dataset, batch_size=128, collate_fn=collate_fn)

test_epoch_list = []
test_acc_list = []
step = 0
with torch.no_grad():
    y_true_list = []
    y_pred_list = []

    for b, (input, target, mask) in enumerate(loader):
        input = input.cuda()
        mask = mask.cuda()
        y_pred = model(input, mask)
        loss = model.loss_fn(input, target, mask)

        print('>> batch:', b + 1, 'loss:', loss.item())

        # 拼接返回值
        for lst in y_pred:
            y_pred_list += lst
        for y, m in zip(target, mask):
            y_true_list += y[m == True].tolist()

    # 整体准确率
    y_true_tensor = torch.tensor(y_true_list)
    y_pred_tensor = torch.tensor(y_pred_list)
    accuracy = (y_true_tensor == y_pred_tensor).sum() / len(y_true_tensor)
    # 计算召回率和F1值
    recall = recall_score(y_true_tensor, y_pred_tensor, average='macro')
    f1 = f1_score(y_true_tensor, y_pred_tensor, average='macro')
    print(
        f'>> total: {len(y_true_tensor)}, Test accuracy: {accuracy.item():.4f}, Recall: {recall:.4f}, F1 Score: {f1:.4f}')

#     test_epoch_list.append(step)
#     test_acc_list.append(accuracy)
#     step += 1
#
# x = test_epoch_list
# y = test_acc_list
# plt.plot(x, y, label='acc')
# plt.xlabel('epoch')
# plt.title('LSTM-CRF_test')
# plt.legend()
# plt.show()