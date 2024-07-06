# import json
# import csv
# import re
# import os
# from pyltp import Segmentor
#
#
# def extract_relations_to_csv(json_line, csv_writer):
#     json_data = json.loads(json_line)
#
#     sent_text = json_data["sentText"]
#     relations = json_data["relationMentions"]
#
#     for relation in relations:
#         e1_text = relation["em1Text"]
#         e1_start = relation["e1start"]
#         label = relation["label"]
#         e2_text = relation["em2Text"]
#         e2_end = relation["e21start"] + len(e2_text)
#         relation_text = f"{e1_text}，{label}，{e2_text}"
#         if e1_start < e2_end:
#             relation_sent = sent_text[e1_start:e2_end]
#             res = re.compile("[^\u4e00-\u9fa5^a-zA-Z0-9]")
#             relation_sent = res.sub("", relation_sent)
#             relation_words = segmentor.segment(relation_sent)  # 分词
#             for i in relation_words:
#                 lexicon.append(i)
#             formatted_string = ' '.join(relation_words)
#             print(f"{formatted_string}\n{relation_text}\n")
#
#             # Write relation to CSV
#             csv_writer.writerow({
#                 'label': label,
#                 'text': f"{formatted_string}",
#                 'label_idx': relation_json.get(label)
#             })
#         else:
#             relation_sent = sent_text[relation["e21start"]:relation["e1start"] + len(e1_text)]
#             res = re.compile("[^\u4e00-\u9fa5^a-zA-Z0-9]")
#             relation_sent = res.sub(" ", relation_sent)
#             relation_words = segmentor.segment(relation_sent)  # 分词
#             for i in relation_words:
#                 lexicon.append(i)
#             formatted_string = ' '.join(relation_words)
#             print(f"{formatted_string}\n{relation_text}\n")
#
#             # Write relation to CSV
#             csv_writer.writerow({
#                 'label': label,
#                 'text': f"{formatted_string}",
#                 'label_idx': relation_json.get(label)
#             })
#
#
# def process_json_file(json_filename, csv_filename):
#     with open(json_filename, 'r', encoding='utf-8') as jsonfile, \
#             open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
#         fieldnames = ['label', 'text', 'label_idx']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#         # Write CSV header
#         writer.writeheader()
#
#         for json_line in jsonfile:
#             # Extract relations from each line of the JSON file
#             extract_relations_to_csv(json_line, writer)
#
#
# def write_to_lexicon(lexicon):
#     with open(r'D:\Users\17614\PycharmProjects\relation_CNN\lexicon.txt', 'w', encoding='utf-8') as f:
#         for i in set(lexicon):
#             f.write(i + "\n")
#
#
# if __name__ == '__main__':
#     relation_json = {"traffic_in": 0, "sell_drugs_to": 1, "posess": 2, "provide_shelter_for": 3, "NA": 4}
#     LTP_DATA_DIR = r"D:\Users\17614\PycharmProjects\ltp_data_v3.4.0"  # ltp模型目录的路径
#     cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
#
#     segmentor = Segmentor(model_path=cws_model_path, lexicon_path="lexicon2.txt")  # 初始化实例
#     segmentor.segment(cws_model_path)  # 加载模型
#
#     lexicon = []
#     # Specify the input JSON filename and the output CSV filename
#     json_filename = r'D:\Users\17614\PycharmProjects\relation_CNN\orig_data\step1_train.json'
#     csv_filename = r'D:\Users\17614\PycharmProjects\relation_CNN\output_relations.csv'
#
#     # Process the JSON file and write relations to CSV
#     process_json_file(json_filename, csv_filename)
#     write_to_lexicon(lexicon)


import jieba
import json
import csv
import re
import os
from pyltp import Segmentor


def extract_relations_to_csv(json_line, csv_writer):
    json_data = json.loads(json_line)

    relations = json_data["relationMentions"]

    for relation in relations:
        sent_text = json_data["sentText"]
        e1_text = relation["em1Text"]
        e1_start = relation["e1start"]
        e1_end = e1_start + len(e1_text)
        label = relation["label"]
        e2_text = relation["em2Text"]
        e2_start = relation["e21start"]
        e2_end = e2_start + len(e2_text)

        if e1_start < e2_end:
            # 标出实体1和实体2
            sent_text = sent_text[:e1_start] + ' <e1> ' + e1_text + ' </e1> ' + sent_text[e1_start + len(e1_text):]
            sent_text = sent_text[:e2_end + 13 - len(e2_text)] + ' <e2> ' + e2_text + ' </e2> ' + sent_text[
                                                                                                  e2_end + 13:]

        else:
            # 标出实体1和实体2
            sent_text = sent_text[:e2_start] + ' <e1> ' + e2_text + ' </e1> ' + sent_text[e2_start + len(e2_text):]
            sent_text = sent_text[:e1_end + 9 - len(e1_text)] + ' <e2> ' + e1_text + ' </e2> ' + sent_text[e1_end + 9:]

        # 加载自定义字典
        jieba.load_userdict("all_labels.txt")

        # 使用正则表达式过滤标点符号但保留<和>)
        filtered_text = re.sub(r'[^\w\s<>/.]', '', sent_text)

        # 将<e1>和</e1>替换为占位符
        placeholder_text = re.sub(r'<e1>', 'SPECIALTOKEN1', filtered_text)
        placeholder_text = re.sub(r'</e1>', 'SPECIALTOKEN2', placeholder_text)
        placeholder_text = re.sub(r'<e2>', 'SPECIALTOKEN3', placeholder_text)
        placeholder_text = re.sub(r'</e2>', 'SPECIALTOKEN4', placeholder_text)

        # 分词
        seg_list = jieba.cut(placeholder_text)

        # 将占位符替换回原始标记
        output_text = ' '.join(seg_list)
        output_text = re.sub(r'SPECIALTOKEN1', '<e1>', output_text)
        output_text = re.sub(r'SPECIALTOKEN2', '</e1>', output_text)
        output_text = re.sub(r'SPECIALTOKEN3', '<e2>', output_text)
        output_text = re.sub(r'SPECIALTOKEN4', '</e2>', output_text)

        # Write relation to CSV
        csv_writer.writerow({
            'label': label,
            'text': f"{output_text}",
            'label_idx': relation_json.get(label)
        })


def process_json_file(json_filename, csv_filename):
    with open(json_filename, 'r', encoding='utf-8') as jsonfile, open(csv_filename, 'w', newline='',
                                                                      encoding='utf-8') as csvfile:
        fieldnames = ['label', 'text', 'label_idx']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write CSV header
        writer.writeheader()

        for json_line in jsonfile:
            # Extract relations from each line of the JSON file
            extract_relations_to_csv(json_line, writer)


def write_to_lexicon(lexicon):
    with open(r'D:\Users\17614\PycharmProjects\relation_CNN\lexicon.txt', 'w', encoding='utf-8') as f:
        for i in set(lexicon):
            f.write(i + "\n")


if __name__ == '__main__':
    relation_json = {"traffic_in": 0, "sell_drugs_to": 1, "posess": 2, "provide_shelter_for": 3, "NA": 4}
    LTP_DATA_DIR = r"D:\Users\17614\PycharmProjects\ltp_data_v3.4.0"  # ltp模型目录的路径
    cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`

    segmentor = Segmentor(model_path=cws_model_path, lexicon_path="lexicon2.txt")  # 初始化实例
    segmentor.segment(cws_model_path)  # 加载模型

    lexicon = []
    # Specify the input JSON filename and the output CSV filename
    json_filename = r'D:\Users\17614\PycharmProjects\relation_CNN\orig_data\step1_train.json'
    csv_filename = r'D:\Users\17614\PycharmProjects\relation_CNN\sign_data.csv'

    # Process the JSON file and write relations to CSV
    process_json_file(json_filename, csv_filename)
    # write_to_lexicon(lexicon)
