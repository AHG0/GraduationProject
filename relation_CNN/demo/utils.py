import torch
from torch.utils.data import Dataset
import json


# 用于数据加载的数据集类
class myDataset(Dataset):
    def __init__(self, data, tokenizer, label_to_index, max_length):
        self.data = data
        self.tokenizer = tokenizer
        self.label_to_index = label_to_index
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text = self.data[idx][0]
        label = self.data[idx][1]
        inputs = self.tokenizer(text, return_tensors='pt', padding='max_length', truncation=True,
                                max_length=self.max_length)
        input_ids = inputs['input_ids'].squeeze(0)  # 移除批次维度
        attention_mask = inputs['attention_mask'].squeeze(0)  # 移除批次维度
        label_id = torch.tensor(self.label_to_index[label])
        return input_ids, attention_mask, label_id


# 从JSON文件加载数据
def load_data(data_file, label_to_index, tokenizer, max_length):
    data = []
    with open(data_file, 'r', encoding='utf-8') as file:
        for line in file:
            sample = json.loads(line)
            for mention in sample["relationMentions"]:
                formatted_text = sample["sentText"].replace(mention["em1Text"],
                                                            "<e1> {} </e1>".format(mention["em1Text"])).replace(
                    mention["em2Text"], "<e2> {} </e2>".format(mention["em2Text"]))
                label = mention["label"]
                data.append((formatted_text, label))
    return myDataset(data, tokenizer, label_to_index, max_length)


# 从JSON文件加载标签到索引映射
def load_label_to_index(label2id_file):
    with open(label2id_file, 'r', encoding='utf-8') as file:
        label_to_index = json.load(file)
    return label_to_index
