# *- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
"""
http://www.cnblogs.com/chenbjin/p/3851165.html
Python TF-IDF计算100份文档关键词权重
"""
vectorizer = CountVectorizer()
corpus = ["我 来到 北京 清华大学 北京 北京",  # 第一类文本切词后的结果，词之间以空格隔开
          "他 来到 了 网易 杭研 大厦",  # 第二类文本的切词结果
          "小明 硕士 毕业 与 中国 科学院",  # 第三类文本的切词结果
          "我 爱 北京 天安门"]  # 第四类文本的切词结果

transformer = TfidfTransformer()
tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
word = vectorizer.get_feature_names()  # 所有文本的关键字
weight = tfidf.toarray()  # 对应的tfidf矩阵
weigh = tfidf.todense()  # 对应的tfidf矩阵

print(weigh)
print(word)
counts = vectorizer.fit_transform(corpus).todense()
print(counts)
# print(counts[1])#矩阵的第1行
# print(vectorizer.vocabulary_)
# for x,y in[[0,1],[0,2],[1,2]]:#[x,y]
#     dist = euclidean_distances(counts[x], counts[y])
#     print('文档{}与文档{}的距离{}'.format(x, y, dist))
#     # Xarray=X.toarray()
# # print(Xarray)
# featureName=vectorizer.get_feature_names()
# print(featureName)