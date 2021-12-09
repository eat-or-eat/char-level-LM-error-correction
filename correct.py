import re
import time
from model import NgramLanguageModel


class Correcter:
    def __init__(self, lm):
        self.lm = lm  # 语言模型
        self.pb_dic = self.load_dic('./data/same_pinyin.txt')  # 候选字典
        self.threshold = 1e-3  # ppl提升的阈值，超过就替换

    # 加载常用的错字字典
    def load_dic(self, path):
        same_pinyin = {}
        with open(path, encoding='utf8') as f:
            for line in f:
                chars = line.split()
                if len(chars) == 3:
                    raw_char, pb_char = chars[0], chars[1] + chars[2]
                else:
                    raw_char, pb_char = chars[0], chars[1]
                same_pinyin[raw_char] = pb_char
        return same_pinyin

    # 获取更换字的ppl列表
    def predict_with_candidates(self, candidates, sentence, index):
        if not candidates:
            return [-1]
        res = []
        sentence_list = list(sentence)  # 字符串是不可变类型，转换成列表进行修改
        for char in candidates:
            sentence_list[index] = char
            sentence = ''.join(sentence_list)
            sentence_ppl = self.lm.predict(sentence)
            ppl_up = self.sentence_ppl_raw - sentence_ppl
            res.append(ppl_up)
        return res

    def change_sentence(self, correct, sentence):
        sentence = list(sentence)
        for index, pb_char in correct.items():
            sentence[index] = pb_char
        return ''.join(sentence)

    # 单个字纠错
    def correction(self, sentence):
        correct = {}
        self.sentence_ppl_raw = self.lm.predict(sentence)
        for index, char in enumerate(sentence):
            candidates = self.pb_dic.get(char, [])
            candidates_ppl = self.predict_with_candidates(candidates, sentence, index)
            if max(candidates_ppl) > self.threshold:
                # 找到最大成句概率对应的替换字符:
                pb_char = candidates[candidates_ppl.index(max(candidates_ppl))]
                print("第%d个字建议修改：%s -> %s, ppl降低： %f" % (index + 1, char, pb_char, max(candidates_ppl)))
                correct[index] = pb_char
        pb_sentence = self.change_sentence(correct, sentence)
        return pb_sentence


if __name__ == '__main__':
    corpus = open('./data/tech_corpus.txt', encoding='utf8').readlines()
    corpus = [re.sub(r'\u3000|\n', '', text) for text in corpus]  # 去除中文跟结尾换行符
    lm = NgramLanguageModel(corpus, 3)
    cor = Correcter(lm)
    raw_sentences = ['科技部召开的哪部会议传出消息',
                     '小米手机现在好像卖的比较鬼了',
                     '中国联通向全国推出锌固定电话']
    start = time.time()
    for raw_sentence in raw_sentences:
        pb_sentence = cor.correction(raw_sentence)
        print('原始句子:', raw_sentence)
        print('建议修改后句子:', pb_sentence)
    print('总耗时:', time.time() - start)
