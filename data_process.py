import pandas as pd
import torch
import numpy as np
from torch.utils.data import Dataset


class DataProcess:
    def __init__(self):
        self.data = pd.read_csv(r'D:\Users\17614\PycharmProjects\relation_CNN\sign_data.csv')

    def get_text_tensor(self):
        word_list = ['<pad>', '<unk>']
        mean_len = 64
        text_list = []
        for i in self.data['text']:
            words_list = i.split()

            for j in words_list:
                if j not in word_list:
                    word_list.append(j)

            if len(words_list) < mean_len:
                for j in range(mean_len - len(words_list)):
                    words_list.append("<pad>")
            if len(words_list) >= mean_len:
                words_list = words_list[:mean_len]
            text_list.append(words_list)

        idx2word_dic = dict(enumerate(word_list))
        word2idx_dic = dict([word, idx] for idx, word in idx2word_dic.items())

        text_idx = []
        for k in text_list:
            sent_idx = []
            for j in k:
                if j in word2idx_dic:
                    sent_idx.append(word2idx_dic[j])
                if j not in word2idx_dic:
                    sent_idx.append(word2idx_dic['<unk>'])
            text_idx.append(sent_idx)
        return torch.from_numpy(np.array(text_idx)), word2idx_dic

    def get_label_tensor(self):
        label_list = []
        for i in self.data["label_idx"]:
            label_list.append(i)
        return torch.from_numpy(np.array(label_list))


class MyDataset(Dataset):
    def __init__(self, text_tensor, label_tensor):
        super().__init__()
        self.text = text_tensor
        self.label = label_tensor

    def __len__(self):
        return self.text.size(0)

    def __getitem__(self, item):
        return self.text[item], self.label[item]


if __name__ == '__main__':
    d = DataProcess()
    f, _ = d.get_text_tensor()
    print(len(f))
    # print(f.size(0))
