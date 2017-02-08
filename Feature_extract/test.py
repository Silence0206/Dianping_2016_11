# *- coding: utf-8 -*-
import os
from gensim import corpora, models, similarities
from pprint import pprint
from matplotlib import pyplot as plt
import  text_processing as tp


import logging

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def PrintDictionary(dictionary):
    token2id = dictionary.token2id  #diction.token2id 存放的是单词-id key-value对 eg{'虾米': 6152, '窗边': 3306}
    dfs = dictionary.dfs     # diction.dfs 存放的是单词的出现频率 eg{0: 396, 1: 403}

    token_info = {}
    for word in token2id:
        token_info[word] = dict(
            word = word,
            id = token2id[word],
            freq = dfs[token2id[word]]
        )#token_info形如{'自动扶梯': {'freq': 1, 'id': 4608, 'word': '自动扶梯'}, '摇头': {'freq': 1, 'id': 2344, 'word': '摇头'}}

    token_items = token_info.values()
    token_items = sorted(token_items, key = lambda x:x['id'])#按照id排序
    print('The info of dictionary: ')
    pprint(token_items)
    print('--------------------------')

def Show2dCorpora(corpus):
    nodes = list(corpus)#里面存放的是id和频率 eg[[(0, 1.0), (1, 1.0), (2, 1.0), (3, 1.0)],[ (4, 1.0), (5, 1.0), (6, 1.0), (7, 1.0), (8, 1.0)]]
    ax0 = [x[0][1] for x in nodes] # 绘制各个doc代表的点
    ax1 = [x[1][1] for x in nodes]
    # print(ax0)
    # print(ax1)
    plt.plot(ax0,ax1,'o')
    plt.show()

#======================开始执行==========================
dicPath = os.getcwd()+"/tmp/deerwester.dict"
if (os.path.exists(dicPath)):
    dictionary = corpora.Dictionary.load(dicPath)
    corpus = corpora.MmCorpus(os.getcwd()+'/tmp/deerwester.mm')
    print("Used files generated from first tutorial")
else:
    print("Please run first tutorial to generate data set")

PrintDictionary(dictionary)

# 尝试将corpus(bow形式) 转化成tf-idf形式
tfidf_model = models.TfidfModel(corpus) # step 1 -- initialize a model 将文档由按照词频表示 转变为按照tf-idf格式表示
doc_bow = [(0, 1), (1, 1),[4,3]]
doc_tfidf = tfidf_model[doc_bow]

# 将整个corpus转为tf-idf格式
corpus_tfidf = tfidf_model[corpus]
# pprint(list(corpus_tfidf))
# print("==========pppppcorpus====================")
# pprint(list(corpus))

## LSI模型 **************************************************
# 转化为lsi模型, 可用作聚类或分类
lsi_model = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
corpus_lsi = lsi_model[corpus_tfidf]
nodes = list(corpus_lsi)
# print("==========pppppcoNodes====================")
pprint(nodes)
lsiout = lsi_model.print_topics(2) # 打印各topic的含义
# print("==========两个topic====================")
print (lsiout[0])
print (lsiout[1])

ax0 = [x[0][1] for x in nodes] # 绘制各个doc代表的点
ax1 = [x[1][1] for x in nodes]
# print(ax0)
# print(ax1)
# plt.plot(ax0,ax1,'o')
# plt.show()
#
lsi_model.save(os.getcwd()+'/tmp/model.lsi') # same for tfidf, lda, ...
lsi_model = models.LsiModel.load(os.getcwd()+'/tmp/model.lsi')
# # #  *********************************************************
# #
# # ## LDA模型 **************************************************
# lda_model = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=2)
# corpus_lda = lda_model[corpus_tfidf]
# # Show2dCorpora(corpus_lsi)
# print("===========corpus_ldacorpus_lda")
# nodes = list(corpus_lda)
# pprint(list(corpus_lda))
# #
# # # 此外，还有Random Projections, Hierarchical Dirichlet Process等模型

corpus_simi_matrix = similarities.MatrixSimilarity(corpus_lsi)
# 计算一个新的文本与既有文本的相关度
#要处理的对象登场
target_courses = ['环境还行，但是感觉不是很好吃，排队的人太多了']
target_text = tp.seg_fil_rew(target_courses)
print(target_text)
test_bow = dictionary.doc2bow(target_text[0])#转换成次数
test_tfidf = tfidf_model[test_bow]
test_lsi = lsi_model[test_tfidf]
test_simi = corpus_simi_matrix[test_lsi]
print(list(enumerate(test_simi)))
# 排序，为输出方便
sort_sims = sorted(enumerate(test_simi), key=lambda item: -item[1])

# 查看结果
print(sort_sims[0:10] ) # 看下前10个最相似的，第一个是基准数据自身