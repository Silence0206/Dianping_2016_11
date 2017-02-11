# -*- coding: utf-8 -*-
import gensim
from gensim.models import word2vec
import logging
import codecs
import text_processing as tp
import os
import jieba
"""
获取csv中的评论
"""
def getComments(filepath):
    with codecs.open(filepath, 'r', 'utf-8') as file:
        comments = []
        for line in file.readlines():
            comment = line.split(",")[5].strip()
            if "<b>" in comment or len(comment) < 3 or "此用户没有填写评论" in comment:
                # print(comment)
                pass
            else:
                comment = comment.replace("&hellip;", " ")
                # print(comment)
                comments.append(comment)
        return comments
"""
构建语料库，选择是否过滤停用词和标点，先分句，在对每句话分词
"""
def fenci(comments,storePath,filter= False):
    stopwords =tp.loadTextWords(os.getcwd()+"\Dictionary\stopword\stopwords.txt")
    if (filter == False):
        for comment in comments:
            seg_result = tp.segmentation(comment, 'str')
            print(seg_result)
            with codecs.open(storePath, 'a+', 'utf-8') as f:
                f.writelines(seg_result + "\n")
    else:
        for comment in comments:
            sents = tp.cut_sentence_2(comment)  # 分句
            for sent in sents:
                sent_list = tp.segmentation(sent, 'list')
                sent_filter = [word for word in sent_list if word not in stopwords and word != ' ']
                seg_result = " ".join(sent_filter)
                if len(seg_result) > 3:
                    print(seg_result)
                    with codecs.open(storePath, 'a+', 'utf-8') as f:
                        f.writelines(seg_result + "\n")


"""
整个评论分词以后过滤，不分句
"""
def fenci1(comments,storePath,filter= False):
    stopwords =tp.loadTextWords(os.getcwd()+"\Dictionary\stopword\stopwords.txt")
    for comment in comments:
        seg_result = tp.segmentation(comment,'str')
        seg_list = tp.segmentation(comment,'list')
        if(filter == True):
            seg_filter = [word for word in seg_list if word not in stopwords and word != ' ']
            seg_result = " ".join(seg_filter)
        print(seg_result)
        with codecs.open(storePath, 'a+', 'utf-8') as f:
            f.writelines(seg_result+"\n")

def createCrops():
    path = "G:\Dianping2017\Dianping_2016_11\Spider_Taobao\data\大衣_评论.csv"
    storePath = "G:\Dianping2017\Dianping_2016_11\learn\Fc_filter_sent.txt"
    comments = getComments(path)
    fenci(comments,storePath,True)

def createModel():
    logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus("G:\Dianping2017\Dianping_2016_11\learn\Fc_filter_sent.txt")  # 加载语料
    model = word2vec.Word2Vec(sentences, size=400, min_count=10)  # 训练skip-gram模型，默认window=5
    model.save(os.getcwd()+'/learn/word2vec_Fc_filter_sent.model')

def getMostSimilar(term,modelname,num):
    model = gensim.models.Word2Vec.load(os.getcwd()+'/learn/'+modelname)#加载模型
    y2 = model.most_similar(term, topn=num)
    print("=======与"+term+"相似的"+str(num)+"个词=========")
    for item in y2:
        print(item[0], item[1] )

if __name__ == '__main__':
    # createModel()
    # model = gensim.models.Word2Vec.load(os.getcwd()+'/learn/word2vec_Fc_filter_sent.model')#加载模型
    # # 计算两个词的相似度/相关程度
    # y1 = model.similarity("样子", "丑")
    # print(y1)
    # getMostSimilar("高兴","word2vec_Fc_filter_sent.model",50)
    # print(len((model["价格"])))
    # getMostSimilar("麻麻","word2vec2_withbiaodian.model",50)

    getMostSimilar("尺码","word2vec_Fc_filter_sent.model",100)
    getMostSimilar("价格","word2vec_Fc_filter_sent.model",100)
    getMostSimilar("面料","word2vec_Fc_filter_sent.model",100)
    getMostSimilar("大小","word2vec_Fc_filter_sent.model",100)
    getMostSimilar("快递","word2vec_Fc_filter_sent.model",100)
    getMostSimilar("服务","word2vec_Fc_filter_sent.model",100)











