import json
from torch.functional import Tensor
from data_process import *
import os
from pyltp import Segmentor
import re

LTP_DATA_DIR = r"D:\Users\17614\PycharmProjects\ltp_data_v3.4.0"  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`

# text = "柳某甲 在 涟源市 第四 水泥厂 附近 帮 吸毒 人员 易某某 另 案 处理 张某 等 在 冷 满 样处 购买 冰毒"
_, d = DataProcess().get_text_tensor()
segmentor = Segmentor(model_path=cws_model_path, lexicon_path="lexicon.txt")  # 初始化实例
segmentor.segment(cws_model_path)  # 加载模型

text = "公诉 机关 指控 2014 年 5 月 被告人   <e1>   钟某某   </e1>   在 其 租住 的 乐昌市 公主 下路 屋内 多次 容留   <e2>   汪某   </e2>   余某某 戴某某 用 自制 吸毒 工具 吸食毒品 2014年9月12日 被告人 钟某某 被 抓获归案"
# text = "公诉机关指控，2014年4月某日、5月某日，被告人刘某先后两次在其位于青岛市城阳区夏庄街道某社区6号楼3单元202户暂住处，容留尹某吸食甲基苯丙胺（俗称“冰毒”），后被公安机关抓获归案。"
# text = "赵某 于 2014年 1月 10日 乘坐 福建 至 哈尔滨 的 长途 客车 行 至 烟台港 环 海路 客运站 时 民警 在 其 携带 的 手提袋 内 查获 冰毒"
# text = "2014年 6月份 8月份 期间 被告人 赵某某"
res = re.compile("[^\u4e00-\u9fa5^a-zA-Z0-9]")
text_ = res.sub(" ", text)
words = list(segmentor.segment(text_))  # 分词

input = torch.tensor([[d.get(w, 1) for w in words]]).cuda()
model = torch.load('TwoBiLSTM_CNN_TwoAttention1.pth')
y_pred = model(input)
y_pred_ = Tensor.cpu(y_pred)
f = open('label_idx.json', 'r', encoding='utf-8')
l2idx = json.loads(f.read())
id2l = dict([idx, l] for l, idx in l2idx.items())
result_np = y_pred_.detach().numpy()[0]
result = max(result_np)
for i in range(len(result_np)):
    if result_np[i] == result:
        print(id2l[i])
