# char-level-LM-error-correction
通过n-gram模型与ppl指标进行简单文本纠错实验

TODO
---

- [x] 实现n-gram语言模型 -21/12/9
- [x] 对字表进行替换 -21/12/10

# 一，项目使用

> 由于数据集小而且应用范围较大，使用效果不好，本项目仅供学习参考ngram语言模型的计算和ppl评价指标应用

## 1.下载

`git clone git@github.com:eat-or-eat/char-level-LM-error-correction.git `

## 2.运行

`python ./correct.py`

打印示例:

```bash
第7个字建议修改：哪 -> 内, ppl降低： 0.019003
原始句子: 科技部召开的哪部会议传出消息
建议修改后句子: 科技部召开的内部会议传出消息
原始句子: 小米手机现在好像卖的比较鬼了
建议修改后句子: 小米手机现在好像卖的比较鬼了
第10个字建议修改：锌 -> 新, ppl降低： 0.001071
原始句子: 中国联通向全国推出锌固定电话
建议修改后句子: 中国联通向全国推出新固定电话
总耗时: 0.009008407592773438
```



# 二，项目介绍

## 1.文件结构

```bash
│  correct.py  # 文本纠错类
│  LICENSE  
│  model.py  # ngram语言模型实现
│  README.md
│
├─data  # 数据文件夹
│      same_pinyin.txt  # 从pycorrector复制的同音字表
│      tech_corpus.txt  # 通THUCNews整合的科技类新闻文章语料
```



## 2.数据引用

文本数据集来源于：

[THUCNews中科技领域的481650~482650.txt总和]([THUCTC: 一个高效的中文文本分类工具 (thunlp.org)](http://thuctc.thunlp.org/))

同音字来源于：
[pycorrector](https://github.com/shibing624/pycorrector/tree/master/pycorrector/data)

