# *- coding: utf-8 -*-
from gensim import corpora, models, similarities
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder

import  text_processing as tp
import os



# rews = ["这家店经过好几次，一贯的印象是生意不错再加上非常大，非常干净整洁，能让食客看到自己食物制作的整个过程。",
#         "地道的本帮菜，挺有特点。价格刚才一查才知道他名字后面加“精作坊”。环境不错，菜的口味还是很适应不同的人群，菜的质量可以，有不少包房，很适应一般商务用餐。",
#         "冲着面包蛤蜊汤去的～幸好是没到饭点就去抢位子,价格还行～海鲜面么无功无过～就是一股西餐的味道啦～～～"]

#从数据库读评论并调用函数进行数据清洗
results = tp.read_list_for_BusArea('root', '58424716', 'dianping','r812')
comments = []

for item in results:
    comments.append(item[11])
print("===========打印评论=========")
count = 1
for com in comments:
    print(str(count)+"    "+com)
    count+=1

commentList = tp.seg_fil_rew(comments)
def tarin1(texts):
    dictionary = corpora.Dictionary(texts)
    dictionary.save(os.getcwd()+'/tmp/deerwester.dict')  # store the dictionary, for future reference
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize(os.getcwd()+'/tmp/deerwester.mm', corpus)#将corpus持久化到磁盘中
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)
    # lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=2)
    print("=====打印LSI10个主题=====")
    lsiout=lsi.print_topics(10)
    for item in lsiout:
            print(item)
    print("=====输出多个文档的文档内容和各主题的匹配性大小关系=====")
    corpus_lsi = lsi[corpus_tfidf]
    for doc in corpus_lsi:  #######输出多个文档的文档内容和各主题的匹配性大小关系
            print(doc)  #######输出为该文档的内容和各个主题的匹配性大小关系
    index = similarities.MatrixSimilarity(lsi[corpus])
    return (index, dictionary, lsi)


(index,dictionary,lsi) =  tarin1(commentList)
#要处理的对象登场
target_courses = ['环境还行，但是感觉不是很好吃，排队的人太多了']
target_text = tp.seg_fil_rew(target_courses)
"""
对具体对象相似度匹配
"""

# 选择一个基准数据
ml_course = target_text[0]

# 词袋处理
ml_bow = dictionary.doc2bow(ml_course)
print("================词袋处理后的一句话================")
print(ml_bow)#把该查询文档（词集）更改为（词袋模型）即：字典格式，key是单词，value是该单词在该文档中出现次数。

# 在上面选择的模型数据 lsi 中，计算其他数据与其的相似度
ml_lsi = lsi[ml_bow]  # ml_lsi 形式如 (topic_id, topic_value)
print("================ml_lsi================")
print(ml_lsi)
sims = index[ml_lsi]  # sims 是最终结果了， index[xxx] 调用内置方法 __getitem__() 来计算ml_lsi

# 排序，为输出方便
sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])

# 查看结果
print(sort_sims[0:10] ) # 看下前10个最相似的，第一个是基准数据自身



