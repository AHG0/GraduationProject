import json

# 从JSON数据中加载句子信息
data = {
    "articleId": 2,
    "sentId": 20,
    "entityMentions": [
        {"end": 20, "start": 17, "text": "林某某", "label": "Nh"},
        {"end": 51, "start": 48, "text": "海洛因", "label": "NDR"},
        {"end": 76, "start": 63, "text": "2014年8月7日早上7时", "label": "NT"},
        {"end": 85, "start": 82, "text": "徐某某", "label": "Nh"},
        {"end": 90, "start": 87, "text": "林某某", "label": "Nh"},
        {"end": 123, "start": 120, "text": "徐某某", "label": "Nh"},
        {"end": 146, "start": 143, "text": "林某某", "label": "Nh"},
        {"end": 187, "start": 182, "text": "0.07克", "label": "NW"},
        {"end": 202, "start": 197, "text": "0.44克", "label": "NW"},
        {"end": 209, "start": 206, "text": "海洛因", "label": "NDR"}
    ],
    "sentText": "湛江市麻章区人民检察院指控，被告人林某某为了赚取利润，承诺帮一名不认识名字的青年男子将十粒毒品（海洛因）放在其养猪场代为销售。2014年8月7日早上7"
                "时许，吸毒人员徐某某来到林某某的养猪场购买毒品，当两人完成交易时，被公安民警当场抓获，并从徐某某身上扣押到可疑毒品一粒和人民币50元，从林某某处扣押到人民币100"
                "元和可疑毒品九小粒。经鉴定，查获的可疑毒品一粒，净重0.07克，可疑毒品九粒，净重0.44克，均检见海洛因成分。",
    "relationMentions": [
        {"e1start": 17, "em2Text": "海洛因", "e21start": 48, "label": "traffic_in", "em1Text": "林某某"},
        {"e1start": 17, "em2Text": "徐某某", "e21start": 82, "label": "sell_drugs_to", "em1Text": "林某某"},
        {"e1start": 17, "em1Text": "林某某", "e21start": 143, "em2Text": "林某某", "label": "NA"},
        {"e1start": 63, "em1Text": "2014年8月7日早上7时", "e21start": 182, "em2Text": "0.07克", "label": "NA"}
    ]
}

# 提取实体和关系信息
sent_text = data["sentText"]
entity_mentions = data["entityMentions"]
relation_mentions = data["relationMentions"]

# 打印句子文本
print("句子文本:")
print(sent_text)

# 打印实体信息
print("\n实体信息:")
for entity_mention in entity_mentions:
    print(f"实体文本: {entity_mention['text']}, 类别: {entity_mention['label']}")

# 打印关系信息
for relation_mention in data["relationMentions"]:
    em1_text = relation_mention.get("em1Text", "N/A")
    em2_text = relation_mention.get("em2Text", "N/A")
    relation_label = relation_mention["label"]
    print(f"em1Text: {em1_text}, 关系: {relation_label}, em2Text: {em2_text}")
