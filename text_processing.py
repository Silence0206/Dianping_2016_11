# *- coding: utf-8 -*-
import mysql.connector
import datetime
import os
import re
import jieba
import jieba.posseg #需要另外加载一个词性标注模块
import jieba.analyse

import time
import logging
import  codecs


jieba.load_userdict(os.getcwd()+"\Dictionary\segmentation dictionary\segdict2.txt")

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
这钟方法分句更加稳妥 但是标点依然保留
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

def lexical_diversity(text):
    return len(text)/len(set(text))

def percentage(count, total):
    return 100 * count / total

def read_list_for_BusArea(usr, pwd, db,busareaId):
    try:
        conn1 = mysql.connector.connect(user=usr, password=pwd, database=db)
        cursor = conn1.cursor()
        # cursor.execute('select * from user where id = %s', ('1',))
        cursor.execute( 'SELECT * FROM dianping.comments A ,dianping.restaurants B   WHERE A.res_id=B.res_id and B.bussi_areaid = %s   order by comment_id limit 0,1000 ',(busareaId,))
        rows = cursor.fetchall()
        cursor.close()
        conn1.close()
        return  rows
    except BaseException as e:
        print("取评论出问题啦", e)
        return

#去停用词以后变成句子向量
"""
输入：reviews = ["这家店经过好几次，一贯的印象是生意不错再加上非常大，非常干净整洁，能让食客看到自己食物制作的整个过程。", "地道的本帮菜，挺有特点。价格刚才一查才知道他名字后面加“精作坊”。环境不错，菜的口味还是很适应不同的人群，菜的质量可以，有不少包房，很适应一般商务用餐。"]
输出：[['这家', '店', '好', '几次', '一贯', '印', '象是', '生意', '不错', '再', '加上', '非常大', '非', '常', '干净', '整洁', '食客', '看到', '食物', '制作', '整个', '过程'], ['地道', '帮菜', '挺', '特点', '价格', '刚才', '一查', '才', '知道', '名字', '后面', '加', '精', '作坊', '环境', '不错', '菜', '口味', '很', '适应', '不同', '人群', '菜', '质量', '不少', '包房', '很', '适应', '商务', '用餐']]

"""
def seg_fil_rew(reviews,low_freq_filter = False):
    stopwords = loadTextWords(os.getcwd()+"\Dictionary\stopword\stopwords.txt")
    review_data = []
    for review in reviews:
        review_data.append(segmentation(review,'list'))#一个人一个[]
    # print("===========review data=====")
    # print(review_data)
    # Filter stopwords from reviews
    seg_fil_result = []

    for review in review_data:  # revidw是分词完毕的每个评论如[[我们],[今天],[出去],[的]]
        fil = [word for word in review if word not in stopwords and word != ' ']
        # print("fil")
        # print(fil)
        seg_fil_result.append(fil)

     # 去除过低频词
    if low_freq_filter:
        all_words = sum(seg_fil_result, [])
        print(all_words)#含重复
        stems_once = set(stem for stem in set(all_words) if all_words.count(stem) == 1)
        texts = [[stem for stem in text if stem not in stems_once] for text in seg_fil_result]
        return texts


    # Return filtered segment reviews
    return seg_fil_result

def main1():
    words= '这家店经过好几次，一贯的印象是生意不错再加上店内外环境超赞，过年终于找到空进去尝试了一次，体验很不错。走进店内，给人的感觉是明亮，通透，宽敞，很有设计感。敞开式厨房非常大，非常干净整洁，能让食客看到自己食物制作的整个过程。服务生和厨师都是既有老外也有中国人。餐前面包好吃，第一口下去感觉好硬，用力掰下一口，沾着他们的给酱，能感觉到一股微微的香味在口中漫开。前菜之神户牛肉，牛肉好没得说，配上羊奶酪，和芝麻菜，点上柠檬汁，复合口味，很开胃。前菜之主厨精选三样，摆盘精致，还用黑醋汁裱上了calypso。味道上，就感觉西班牙火腿确实蛮好吃的。主菜之烤羊排。要求五分熟，羊排不大但肥厚，一面略焦。口感有肥嫩有焦香还有一股温和的羊肉味。配的烤虾是个惊喜，腌得入味，煎得很透。主菜之慢火炖牛脸肉。这道比较一般，牛脸肉确实炖的很酥软了但是口味上只吃的出略过头的咸味，中间那坨土豆泥倒是味道很不错，不油且醇香。甜点是巧克力熔岩。这个甜品一直有听说，第一次尝试，感觉这家店没辜负我对它的想象，醇香绵软入口即化，微甜，配上一杯意式咖啡作为一餐的收尾感觉很美好。老婆还点了个不知道什么玩意的无酒精鸡尾酒，出乎意料的好喝。我不太吃西餐，之前试过外滩的米氏和芮欧的Henkes。我觉得我更喜欢这家Calypso，因为它家菜的味道并没让我这个爱国的胃觉得不适应倒是又能确实体验到异国美食的小新奇。以后还会光顾！.'
    sentences=cut_sentence_2(words)
    print(sentences)
    for item in sentences:
        print(segmentation(item,"list"))

def test():
    print('=' * 40)
    print('3. 关键词提取')
    print('-' * 40)
    print(' TF-IDF')
    print('-' * 40)

    s = "此外，公司拟对全资子公司吉林欧亚置业有限公司增资4.3亿元，增资后，吉林欧亚置业注册资本由7000万元增加到5亿元。吉林欧亚置业主要经营范围为房地产开发及百货零售等业务。目前在建吉林欧亚城市商业综合体项目。2013年，实现营业收入0万元，实现净利润-139.13万元。"
    for x, w in jieba.analyse.extract_tags(s, withWeight=True):
        print('%s %s' % (x, w))

    print('-' * 40)
    print(' TextRank')
    print('-' * 40)

    for x, w in jieba.analyse.textrank(s, withWeight=True):
        print('%s %s' % (x, w))
test()
# rews = ["这家店经过好几次，一贯的印象是生意不错再加上店内外环境超赞，过年终于找到空进去尝试了一次，体验很不错。走进店内，给人的感觉是明亮，通透，宽敞，很有设计感。敞开式厨房非常大，非常干净整洁，能让食客看到自己食物制作的整个过程。",
#         "地道的本帮菜，挺有特点。价格要比其他上海人家要贵一些，刚才一查才知道他名字后面加“精作坊”。环境不错，菜的口味还是很适应不同的人群，菜的质量可以，有不少包房，很适应一般商务用餐。",
#         "冲着面包蛤蜊汤去的～幸好是没到饭点就去抢位子，要不然十一点半以后根本没有座位啊～蔬菜沙拉加一份烟熏三文鱼是绝配～面包蛤蜊汤味道和旧金山的渔人码头比稍微有一点点淡～海鲜面么无功无过～就是一股西餐的味道啦～～～"]
rews = ["衣衣质量还不错，就是颜色不太喜欢"]
result = segmentation("衣衣质量还不错，就是颜色不太喜欢","list")
print(result)
