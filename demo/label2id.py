import json

def label2id(file_list):
    # 初始化一个空的映射表
    label_to_index = {}
    for i in file_list:
        with open(i, encoding="utf-8") as f:
            for line in f.readlines():
                # 将 JSON 字符串转换为字典
                data = json.loads(line)

                # 提取关系标签
                relation_mentions = data["relationMentions"]
                for mention in relation_mentions:
                    label = mention["label"]
                    # 如果标签不在映射表中，则将其添加到映射表中
                    if label not in label_to_index:
                        label_to_index[label] = len(label_to_index)

        # 将映射写入 JSON 文件
        output_file = "label2id.json"
        with open(output_file, "w") as f:
            json.dump(label_to_index, f)

        print("标签到索引的映射已写入 JSON 文件:", output_file)


if __name__ == '__main__':
    file_list = [r"D:\Users\17614\PycharmProjects\relation_CNN\demo\WebNLG\new_train.json",
                 r"D:\Users\17614\PycharmProjects\relation_CNN\demo\WebNLG\new_valid.json",
                 r"D:\Users\17614\PycharmProjects\relation_CNN\demo\WebNLG\new_test.json"]

    label2id(file_list)
