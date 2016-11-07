# *- coding: utf-8 -*-
import mysql.connector
import datetime
import re
import openpyxl
import jieba
import jieba.posseg #需要另外加载一个词性标注模块
import snownlp
import time
import logging
import  codecs

jieba.load_userdict("G:\Dianping\Dictionary\segmentation dictionary\segdict1.txt")
jieba.load_userdict("G:\Dianping\Dictionary\segmentation dictionary\segdict2.txt")
"""
弄出来标点还在
"""
def segmentation(sentence, para):
    if para == 'str':
        seg_list = jieba.cut(sentence)
        seg_result = ' '.join(seg_list)
        return seg_result
    elif para == 'list':
        seg_list2 = jieba.cut(sentence)
        seg_result2 = []
        for w in seg_list2:
            seg_result2.append(w)
        return seg_result2

"""
input: '这款手机大小合适。'
output:
    parameter_1: 这 r 款 m 手机 n 大小 b 合适 a 。 x
    parameter_2: [(u'\u8fd9', ['r']), (u'\u6b3e', ['m']),
    (u'\u624b\u673a', ['n']), (u'\u5927\u5c0f', ['b']),
    (u'\u5408\u9002', ['a']), (u'\u3002', ['x'])]
"""

def postagger(sentence, para):
    if para == 'list':
        pos_data1 = jieba.posseg.cut(sentence)
        pos_list = []
        for w in pos_data1:
             pos_list.append((w.word, w.flag)) #make every word and tag as a tuple and add them to a list
        return pos_list
    elif para == 'str':
        pos_data2 = jieba.posseg.cut(sentence)
        pos_list2 = []
        for w2 in pos_data2:
            pos_list2.extend([w2.word, w2.flag])
        pos_str = ' '.join(pos_list2)
        return pos_str

""" Maybe this algorithm will have bugs in it """
def cut_sentences_1(words):
    start = 0
    i = 0 #i is the position of words
    sents = []
    punt_list = ',.!?:;~，。！？：；～ … ' # Sentence cutting punctuations
    for word in words:
        if word in punt_list and token not in punt_list: #检查标点符号下一个字符是否还是标点
            sents.append(words[start:i+1])
            start = i+1
            i += 1
        else:
            i += 1
            token = list(words[start:i+2]).pop()
    # if there is no punctuations in the end of a sentence, it can still be cutted
    if start < len(words):
        sents.append(words[start:])
    return sents
"""
这钟方法分句更加稳妥
"""
def cut_sentence_2(words):
    #words = (words).decode('utf8')
    start = 0
    i = 0 #i is the position of words
    token = 'meaningless'
    sents = []
    punt_list = ',.!?;~，。！？；～… '
    for word in words:
        if word not in punt_list:
            i += 1
            token = list(words[start:i+2]).pop()
            #print token
        elif word in punt_list and token in punt_list:
            i += 1
            token = list(words[start:i+2]).pop()
        else:
            sents.append(words[start:i+1])
            start = i+1
            i += 1
    if start < len(words):
        sents.append(words[start:]) #这是为了处理文本末尾没有标点符号的情况
    return sents

"""
为下一个函数做准备
"""
def cutword(data):
    result=jieba.cut(data)
    return result

"""
第一步貌似是去标点
"""
def wordfrequency(text):
    sub_re='[a-zA-Z]+|[\s+\.\!\/_,$%^*\(\d+\"\']+|[+—；—！:\(\)：《》，。？、~@#￥%……&*（）％～\[\]\|\?\·【】“”;-]+'
    text=re.sub(sub_re,'',text)
    result={}
    words=[word for word in cutword(text)]
    for word in words:
        try:
            result[word]+=1
        except:
            result[word]=1
    return result

"""
载入停用词表、基础情感词典
"""
def loadTextWords(dic_path):
    result=[]
    for line in open(dic_path,'r',encoding='utf-8'):
        result.append(line.replace('\n',''))
    return result

#根据sql语句读列表
def read_list(usr, pwd, db,sql):
    try:
        conn1 = mysql.connector.connect(user=usr, password=pwd, database=db)
        cursor = conn1.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn1.close()
        return  rows
    except BaseException as e:
        print("取评论出问题啦", e)
        return

#访问过条目做标记
def set_flag(wordname,wordtag):
    global conn
    conn = mysql.connector.connect(user='root', password='58424716', database='dianping')
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE word_frequency SET flag=TRUE  WHERE word_name =%s and word_tag=%s',(wordname,wordtag) )
        conn.commit()
        cursor.close()
    except mysql.connector.Error as e:
        print("标记词条出问题", e)
        conn.rollback

def main1():
    words= '这家店经过好几次，一贯的印象是生意不错再加上店内外环境超赞，过年终于找到空进去尝试了一次，体验很不错。走进店内，给人的感觉是明亮，通透，宽敞，很有设计感。敞开式厨房非常大，非常干净整洁，能让食客看到自己食物制作的整个过程。服务生和厨师都是既有老外也有中国人。餐前面包好吃，第一口下去感觉好硬，用力掰下一口，沾着他们的给酱，能感觉到一股微微的香味在口中漫开。前菜之神户牛肉，牛肉好没得说，配上羊奶酪，和芝麻菜，点上柠檬汁，复合口味，很开胃。前菜之主厨精选三样，摆盘精致，还用黑醋汁裱上了calypso。味道上，就感觉西班牙火腿确实蛮好吃的。主菜之烤羊排。要求五分熟，羊排不大但肥厚，一面略焦。口感有肥嫩有焦香还有一股温和的羊肉味。配的烤虾是个惊喜，腌得入味，煎得很透。主菜之慢火炖牛脸肉。这道比较一般，牛脸肉确实炖的很酥软了但是口味上只吃的出略过头的咸味，中间那坨土豆泥倒是味道很不错，不油且醇香。甜点是巧克力熔岩。这个甜品一直有听说，第一次尝试，感觉这家店没辜负我对它的想象，醇香绵软入口即化，微甜，配上一杯意式咖啡作为一餐的收尾感觉很美好。老婆还点了个不知道什么玩意的无酒精鸡尾酒，出乎意料的好喝。我不太吃西餐，之前试过外滩的米氏和芮欧的Henkes。我觉得我更喜欢这家Calypso，因为它家菜的味道并没让我这个爱国的胃觉得不适应倒是又能确实体验到异国美食的小新奇。以后还会光顾！.'
    sentences=cut_sentence_2(words)
    for item in sentences:
        print(segmentation(item,"list"))

