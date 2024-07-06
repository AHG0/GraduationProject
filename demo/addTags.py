import json

from demo.utils import load_label_to_index

# 输入的JSON数据
json_data = '{"sentText": "Alan Bean , who was part of Apollo 12 , was born in Wheeler , Texas on March 15th , 1932 and is now retired .", "relationMentions": [{"em1Text": "Bean", "em2Text": "12", "label": "was a crew member of"}, {"em1Text": "Bean", "em2Text": "Texas", "label": "birthPlace"}]}'

# 解析JSON数据
data = json.loads(json_data)

# 定义label与数字索引的映射关系
label_to_index = {"was a crew member of": 0, "birthPlace": 1}

# 替换文本中的实体
formatted_texts = []
for mention in data["relationMentions"]:
    formatted_text = data["sentText"].replace(mention["em1Text"], "<e1> {} </e1>".format(mention["em1Text"])) \
        .replace(mention["em2Text"], "<e2> {} </e2>".format(mention["em2Text"]))
    formatted_texts.append(formatted_text + " (" + str(label_to_index[mention["label"]]) + ")")

for text in formatted_texts:
    print(text)


def load_data(data_file, label_to_index):
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
        return data


if __name__ == '__main__':
    label_to_index = load_label_to_index('label2id.json')
    data = load_data('./WebNLG/new_train.json', label_to_index)
    for i in data:
        print(i)
