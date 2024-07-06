# -*- coding: utf-8 -*-

import sys
import csv
import os

# with open(r'D:\QA_train\ownthink_v2\ownthink_v2.csv', 'r', encoding='utf8') as fin:
#     reader = csv.reader(fin)
#     for index, read in enumerate(reader):
#         print(read)
#         if index > 10:
#             sys.exit(0)

import sys
import csv

# filePath = r'D:\QA_train\ownthink_v2\ownthink_v2.csv'
# all_data = []
# with open(filePath, "r", encoding="utf-8") as csvFile:
#     reader = csv.reader(csvFile)
#     # for i in reader:
#     #     print(i)
#     #     with open(r'D:\QA_train\ownthink_v2\csvTest.csv', "a", encoding='utf-8', newline='') as f:
#     #         writer = csv.writer(f)
#     #         # for row in all_data:
#     #         writer.writerow(i)
#     #
#     # sys.exit(0)
#     fileData = r'D:\QA_train\ownthink_v2\csvTest.csv'
#     if os.path.exists(filePath):
#         os.remove(fileData)
#     n_r_b_name = [":Head", "relationship", ":Tail"]
#     for index, read in enumerate(reader):
#         # print(read)
#         with open(r'D:\QA_train\ownthink_v2\csvTest.csv', "a", newline='', encoding='utf-8') as f:
#             writer = csv.writer(f)
#             writer.writerow(read)
#
#         # f = open(r'D:\QA_train\ownthink_v2\csvTest.csv', 'a+', encoding='utf-8', newline='')
#         # csv_writer = csv.writer(f, delimiter='\t')
#         # for i in all_data:
#         #     write = csv_writer.writerow(i)
#
#         # print(read)
#         if index > 1000:
#             break
#         # f.close()

import pandas as pd
import csv

from comtypes.safearray import numpy


def g():
    #
    # filePath = r"D:\QA_train\ownthink_v2\ownthink_v2.csv"
    #
    # 读取三元组文件
    n_r_b_name = [":Head", "relationship", ":Tail"]
    n_r_b = pd.read_csv(r'D:\QA_train\ownthink_v2\csvTest.csv', encoding='utf-8', sep=',',
                        names=n_r_b_name)  # 使用少量的测试数据
    # n_r_b = pd.read_csv(filePath, sep=',', names=n_r_b_name)  # 使用全量的数据
    # print(n_r_b.info())
    # print(n_r_b[':Head'].tolist())

    # # 去除重复实体
    # entity = set()
    # entity_n = n_r_b[':START_ID'].tolist()
    # entity_b = n_r_b[':END_ID'].tolist()
    # for i in entity_n:
    #     entity.add(i)
    # for i in entity_b:
    #     entity.add(i)
    # # print(entity)
    #
    head_entity = n_r_b[':Head'].tolist()
    tail_entity = n_r_b[':Tail'].tolist()
    head = numpy.array(head_entity).reshape(len(head_entity), 1)
    tail = numpy.array(tail_entity).reshape(len(tail_entity), 1)
    # 保存头节点文件-entity.csv
    csvf_entity = open(r"D:\QA_train\ownthink_v2\head_entity.csv", "a+", newline='', encoding='utf-8')
    w_entity = csv.writer(csvf_entity)
    # 实体ID，要求唯一，名称，LABEL标签，可自己不同设定对应的标签
    w_entity.writerows(head)
    csvf_entity.close()

    # 保存尾节点文件-entity.csv
    csvf_entity = open(r"D:\QA_train\ownthink_v2\tail_entity.csv", "a+", newline='', encoding='utf-8')
    w_entity = csv.writer(csvf_entity)
    # 实体ID，要求唯一，名称，LABEL标签，可自己不同设定对应的标签
    w_entity.writerows(tail)
    csvf_entity.close()


# # 保存节点文件-entity.csv
# csvf_entity = open(r"D:\QA_train\ownthink_v2\entity.csv", "w", newline='', encoding='utf-8')
# w_entity = csv.writer(csvf_entity)
# # 实体ID，要求唯一，名称，LABEL标签，可自己不同设定对应的标签
# w_entity.writerow(("entity:ID", "name", ":LABEL"))
# entity = list(entity)
# entity_dict = {}
# for i in range(len(entity)):
#     w_entity.writerow(("e" + str(i), entity[i], "my_entity"))
#     entity_dict[entity[i]] = "e" + str(i)
# csvf_entity.close()

# 生成关系文件-relationship.csv
# 起始实体ID，终点实体ID，要求与实体文件中ID对应，:TYPE即为关系
# n_r_b[':START_ID'] = n_r_b[':START_ID'].map(entity_dict)
# n_r_b['name'] = n_r_b['relationship']
# n_r_b[':END_ID'] = n_r_b[':END_ID'].map(entity_dict)
# n_r_b[":TYPE"] = n_r_b['relationship']
# n_r_b.pop('relationship')
# n_r_b.to_csv(r"D:\QA_train\ownthink_v2\relationship.csv", index=False, encoding="utf-8")


def t():
    n_r_b_name = [":Head", "relationship", ":Tail"]
    n_r_b = pd.read_csv(r'D:\QA_train\ownthink_v2\csvTest.csv', encoding='utf-8', sep=',',
                        names=n_r_b_name)  # 使用少量的测试数据
    print(n_r_b)
    n_r_b = pd.read_csv(r'D:\QA_train\ownthink_v2\head_entity.csv', encoding='utf-8', sep='\t')  # 使用少量的测试数据
    print(n_r_b)
    n_r_b = pd.read_csv(r'D:\QA_train\ownthink_v2\tail_entity.csv', encoding='utf-8', sep='\t')  # 使用少量的测试数据
    print(n_r_b)


if __name__ == '__main__':
    g()
    t()
