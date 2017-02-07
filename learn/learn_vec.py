# *- coding: utf-8 -*-
from gensim import corpora, models, similarities
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder

import  text_processing as tp
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer

#从数据库读评论并调用函数进行数据清洗
results = tp.read_list_for_BusArea('root', '58424716', 'dianping','r812')
comments = []

for item in results:
    comments.append(item[11])
commentList = tp.seg_fil_rew(comments)
corpus = []
for comment in commentList:
    corpus.append(" ".join(comment))
vectorizer = CountVectorizer()

transformer = TfidfTransformer()
tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
word = vectorizer.get_feature_names()  # 所有文本的关键字
weight = tfidf.toarray()  # 对应的tfidf矩阵
weigh = tfidf.todense()  # 对应的tfidf矩阵
names = vectorizer.get_feature_names()
print(len(names))
# print(word)
# counts = vectorizer.fit_transform(corpus).todense()
# print(counts)
