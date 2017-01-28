# -*- coding: utf-8 -*-
import gensim
from gensim.models import word2vec
import logging
import codecs
import text_processing as tp
import os
"""
获取csv中的评论
"""
def getComments(filepath):
    with codecs.open(filepath, 'r', 'utf-8') as file:
        comments = []
        for line in file.readlines():
            comment = line.split(",")[5].strip()
            if "<b>" in comment or len(comment) < 3:
                # print(comment)
                pass
            else:
                comment = comment.replace("&hellip;", " ")
                # print(comment)
                comments.append(comment)
        return comments
"""
构建语料库
"""
def fenci(comments,storePath):
    for comment in comments:
        seg_result = tp.segmentation(comment,'str')
        print(seg_result)
        with codecs.open(storePath, 'a+', 'utf-8') as f:
            f.writelines(seg_result+"\n")

def createCrops():
    path = "G:\Dianping2017\Dianping_2016_11\Spider_Taobao\data\羽绒服评论.csv"
    storePath = "G:\Dianping2017\Dianping_2016_11\learn\dfenci.txt"
    comments = getComments(path)
    fenci(comments,storePath)

def createModel():
    logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus("G:\Dianping2017\Dianping_2016_11\learn\dfenci.txt")  # 加载语料
    model = word2vec.Word2Vec(sentences, size=200, min_count=6)  # 训练skip-gram模型，默认window=5
    model.save(os.getcwd()+'/learn/word2vec2.model')

def getMostSimilar(term,modelname,num):
    model = gensim.models.Word2Vec.load(os.getcwd()+'/learn/'+modelname)#加载模型
    y2 = model.most_similar(term, topn=num)
    print("=======与"+term+"相似的"+str(num)+"个词=========")
    for item in y2:
        print(item[0], item[1] )

if __name__ == '__main__':
    model = gensim.models.Word2Vec.load(os.getcwd()+'/learn/word2vec2.model')#加载模型
    # 计算两个词的相似度/相关程度
    # y1 = model.similarity("样子", "样式")
    # print(y1)
    getMostSimilar("款式","word2vec2.model",20)
    getMostSimilar("价格","word2vec2.model",20)
    getMostSimilar("材质","word2vec2.model",20)



