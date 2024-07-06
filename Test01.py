import json

# 读取JSON文件
j=1
with open(r"D:\train_data\step1_train.json", 'r', encoding='utf-8') as json_file:
    for i in json_file.readlines():
        f = open(f"data{j}.txt", "w", encoding="UTF-8")
        f.write(json.loads(i)['sentText'])
        j+=1


# # 提取sentText字段并写入txt文件
# with open('sentTexts.txt', 'w', encoding='utf-8') as txt_file:
#     for item in data:
#         sent_text = item.get('sentText')  # 假设'sentText'是JSON中的字段名
#         if sent_text:
#             txt_file.write(sent_text + '\n')