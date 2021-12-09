import math
import re
from collections import defaultdict


class NgramNnlm:
    def __init__(self, corpus=None, n=3):
        self.n = n
        self.unk_pb = 1e-4  # 给未知词设置个低概率免得概率连乘为0
        self.back_pb = 0.6  # 设置一个回退概率，免得没有的词没有n-gram概率
        self.ngram_count_dic = dict((x + 1, defaultdict(int)) for x in range(n))
        self.ngram_count_pb_dic = dict((x + 1, defaultdict(int)) for x in range(n))
        self.ngram_count(corpus)  # 统计预料的ngram数量
        self.calc_ngram_pb()  # 根据ngram前一阶的数量计算当前ngram的概率

    # 统计ngram词和数量
    def ngram_count(self, corpus):
        for sentence in corpus:  # 遍历每行句子
            for window_size in range(1, self.n + 1):  # 遍历n个窗口
                for index, word in enumerate(sentence):  # 获取n-gram
                    ngram = sentence[index:index + window_size]
                    if len(ngram) != window_size:  # 末尾的字不够取多gram就跳过
                        continue
                    self.ngram_count_dic[window_size][ngram] += 1
        self.ngram_count_dic[0] = sum(self.ngram_count_dic[1].values())

    # 计算ngram概率
    def calc_ngram_pb(self):
        for window_size in range(1, self.n + 1):
            for ngram, count in self.ngram_count_dic[window_size].items():
                if window_size > 1:
                    ngram_head = ngram[:-1]
                    ngram_head_count = self.ngram_count_dic[window_size - 1][ngram_head]
                else:
                    ngram_head_count = self.ngram_count_dic[0]
                self.ngram_count_pb_dic[window_size][ngram] = count / ngram_head_count

    # 计成句概率
    def get_ngram_pb(self, ngram):
        n = len(ngram)
        if ngram in self.ngram_count_dic[n]:
            return self.ngram_count_pb_dic[n][ngram]
        elif n == 1:
            return self.unk_pb
        else:
            return self.back_pb * self.get_ngram_pb(ngram[1:])

    # 预测句子概率
    def predict(self, sentence):
        sentence_pb = 0
        for i in range(len(sentence)):
            ngram = sentence[max(0, i - self.n + 1):i + 1]
            pb = self.get_ngram_pb(ngram)
            sentence_pb += pb
        sentence_pb /= len(sentence)  # 防止句子太长累加的概率太多
        return 2 ** (-1 * sentence_pb)  # 概率越大ppl应该越小，x的负指数单调递减



if __name__ == '__main__':
    corpus = open('./data/tech_corpus.txt', encoding='utf8').readlines()
    corpus = [re.sub(r'\u3000|\n', '', text) for text in corpus]  # 去除中文跟结尾换行符

    lm = NgramNnlm(corpus, 3)
    sentence1 = '中国联通向全国推出薪固定电话'
    sentence2 = '中国联通向全国推出新固定电话'
    print(lm.predict(sentence1))
    print(lm.predict(sentence2))
