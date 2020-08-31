# -*- coding: utf-8 -*-

import re
import json
import cn2an      # 阿拉伯数字 <=> 中文数字
import string
import unicodedata


all_flag = string.punctuation + u'“《》「」』『·—□〈〉•’●‘×”・∫,?!.♪:⦆⦆╮╭〜😂👏💨✨◤◢☀€😍🙀ノ♥★⋯⋯σ≪≫♡⎢◊.|:—.↓∩'
pattern_flag = re.compile('[%s]' % re.escape(all_flag))
alpha_char = string.punctuation + u'abcdefghijklmnopqrstuvwxyz'
pattern_alpha = re.compile('[%s]' % re.escape(alpha_char))

trantab = str.maketrans('，。！？【】（）〔〕％＃＠＆１２３４５６７８９０、', ',.!?[]()[]%#@&1234567890,')


def is_all_chinese1(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


def is_all_chinese2(strs):
    if all(map(lambda c: '\u4e00' <= c <= '\u9fa5', strs)):
        return True
    return False


def filter_emoji(desstr,restr=''):
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


def data_clean1(str_in):
    text_a = str_in.strip().replace(" ", "").replace("alink", "").replace("°C", "度")
    text_b = filter_emoji(text_a, restr='')
    text_1 = unicodedata.normalize('NFKC', text_b.lower().replace(" ", ""))      # 中文标点转换为英文标点
    text_2 = text_1.translate(trantab)  # 漏网之鱼手动修改对应
    text_3 = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", text_2)   # 去掉小括号(), {}, []里的内容
    text_4 = cn2an.transform(text_3, "an2cn")                   # 阿拉伯数字转中文
    text_5 = pattern_flag.sub(u'', text_4)                      # 去掉标点符号
    if not is_all_chinese1(text_5):
        text_6 = pattern_alpha.sub(u'', text_5)
        if not is_all_chinese1(text_6):
            # print(text_5)
            return ""
    return text_3


if __name__ == "__main__":
    # s = "回家来第一顿餐太巴适了撒"           # "猫儿本❤❤好漂亮的国度"      "🎤唱吧你还我妻子😭😭😭"   回家来第一顿餐太巴适了撒     猫儿本❤❤好漂亮的国度
    # print(filter_emoji(s, restr=''))
    # exit()

    data_file = "/home/psc/Desktop/code/conv/sentence-transformers/examples/training/quora_duplicate_questions/data/STC.json"
    train_samples = []
    discard_num = 0
    use_num = 0
    with open(data_file, "r", encoding="utf-8") as f:
        dataset = json.loads(f.read())
        for k, v in dataset.items():
            for cur_dialg in v:
                query_sent = data_clean1(cur_dialg[0])
                content_sent = data_clean1(cur_dialg[1])
                if len(query_sent)==0 or len(content_sent)==0:
                    discard_num += 1
                    continue
                else:
                    use_num += 1
    print("discard_num / all_num = %d / %d" % (discard_num, discard_num + use_num))









'''
data/STC.json
discard_num / all_num = 114146 / 4414798 == 2.5%
'''