# -*- coding: utf-8 -*-
import json
import re
import jieba

# 加载自定义字典
jieba.load_userdict("all_labels.txt")
with open('orig_data/step1_train.json', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)

        for i in range(len(data["relationMentions"])):
            em1Text = data["relationMentions"][i]["em1Text"]
            em2Text = data["relationMentions"][i]["em2Text"]
            e1start = data["relationMentions"][i]["e1start"]
            e21start = data["relationMentions"][i]["e21start"]
            label = data["relationMentions"][i]["label"]
            sentText = data["sentText"]

            marked_sentText = sentText[:e1start] + " <e1> " + em1Text + " </e1> " + sentText[e1start + len(
                em1Text):e21start] + " <e2> " + em2Text + " </e2> " + sentText[e21start + len(em2Text):]

            # print(marked_sentText)

            # 使用正则表达式过滤标点符号但保留<和>)
            filtered_text = re.sub(r'[^\w\s<>/.]', '', marked_sentText)

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

            # 打印分词结果
            print(label + "，" + output_text)
