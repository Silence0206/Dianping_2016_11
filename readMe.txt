用世博源和静安寺的所有餐厅评论统计词频扩展领域情感词典


Dic_processing.py:
    构造分词时用的词典
    将网上下载下来合并在一起的搜狗词库（含重复词）sougouDic，变成不重复的set以后存入segdic3，然后再写入词频，最后存入segidc2（1994404）
    PS：segdict1为手机领域情感词典 没啥用
    最终分词词典用segdic2

Create_My_Dic：
    将基础情感词典（几个通用的合并后分成的Neg和Pos）、程度词典、否定词典、停用词典合并（共17108条）
    将dianping.word_frequency中的词与上述词典作对比，不在其中的放在My_newWords中，共13641条

wordcut/wordfrequency.py：
    打标签、分句分词、统计词频
    用于生成数据库中的word_frequency，其中的单词都是词频大于某个阈值的

===数据库表
1、comments_split
2、word_frequency
    name| word_tag |word_times| flag


考虑标点？
