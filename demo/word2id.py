import json
import string
from nltk.tokenize import word_tokenize


# 去除标点符号的函数
def remove_punctuation(word):
    return word.translate(str.maketrans('', '', string.punctuation))


def word2id(file_list):
    total_len = 0
    total_words = 0
    word_to_idx = {}
    for i in file_list:
        with open(i, encoding='utf-8') as f:
            for line in f:
                sample = json.loads(line)
                sentText = sample["sentText"]
                tokens = word_tokenize(sentText)
                total_len += len(sentText)
                total_words += 1
                for word in tokens:
                    word = remove_punctuation(word)
                    if word:
                        if word not in word_to_idx:
                            word_to_idx[word] = len(word_to_idx)
    mean_len = total_len / total_words
    # output_file = 'word2id.json'
    # with open(output_file, 'w') as json_file:
    #     json.dump(word_to_idx, json_file)
    # print("标签到索引的映射已写入 JSON 文件:", output_file)
    print("文本的平均长度为:", mean_len)


if __name__ == '__main__':
    file_list = [r"D:\Users\17614\PycharmProjects\relation_CNN\demo\WebNLG\new_train.json",
                 r"D:\Users\17614\PycharmProjects\relation_CNN\demo\WebNLG\new_valid.json",
                 r"D:\Users\17614\PycharmProjects\relation_CNN\demo\WebNLG\new_test.json"]
    # file_list = [r"D:\Users\17614\PycharmProjects\relation_CNN\orig_data\step1_train.json"]
    word2id(file_list)
