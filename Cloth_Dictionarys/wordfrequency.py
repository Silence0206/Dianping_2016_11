# *- coding: utf-8 -*-
import jieba
# import  wordcloud
import re
import string
import  xlwt
import mysql.connector
import datetime
import jieba.posseg #需要另外加载一个词性标注模块
import text_processing as tp
import os
"""
构造自己的情感词典初步--统计词频
"""
# jieba.load_userdict("G:\Dianping\Dictionary\segmentation dictionary\segdict1.txt")
jieba.load_userdict(os.getcwd()+"\Cloth_Dictionarys\clothDic_frequency.txt")

"""用来存储词频统计结果"""
result = {}


def cutword(data):
    seg_list2=jieba.cut(data)
    seg_result2 = []
    for w in seg_list2:
        seg_result2.append(w)
    print(seg_result2)
    return seg_result2

def postagger(sentence):
    pos_data1 = jieba.posseg.cut(sentence)
    pos_list = []
    for w in pos_data1:
        pos_list.append((w.word, w.flag)) #make every word and tag as a tuple and add them to a list
    return pos_list

"""
去标点以后分词 再统计词频
加词性标签
"""
def wordfrequency_tag(text):
    #不应该把英文过滤、此处去了标点
    sub_re='[\s+\.\!\/_,$%^*\(\d+\"\']+|[+—；—！:\(\)：《》，。？、~@#￥%……&*（）％～\[\]\|\?\·【】“”;-]+'
    text=re.sub(sub_re,' ',text)
    textlist=text.split()
    print("=======")
    print(textlist)
    for item in textlist:
        words=[word for word in postagger(item)]
        for word in words:
            try:
                result[word]+=1
            except:
                result[word]=1
    return result


"""
第一步貌似是去标点
对每一条评论做处理
"""
def wordfrequency(text):
    sub_re='[a-zA-Z]+|[\s+\.\!\/_,$%^*\(\d+\"\']+|[+—；—！:\(\)：《》，。？、~@#￥%……&*（）％～\[\]\|\?\·【】“”;-]+'
    text=re.sub(sub_re,' ',text)
    textlist=text.split()
    print("=======")
    print(textlist)
    for item in textlist:
        words=[word for word in cutword(item)]
        for word in words:
            try:
                result[word]+=1
            except:
                result[word]=1
    return result

def loadFunctionWords():
    result=[]
    for line in open('','r',encoding='utf-8'):
        result.append(line.replace(' 3\n',''))
    return result


def read_list(usr, pwd, db):
    try:
        conn1 = mysql.connector.connect(user=usr, password=pwd, database=db)
        cursor = conn1.cursor()
        cursor.execute( 'SELECT * FROM dianping.comments_split order by comment_id  ')
        rows = cursor.fetchall()
        cursor.close()
        conn1.close()
        return  rows
    except BaseException as e:
        print("取评论出问题啦", e)
        return

"""
不带词性标签写入EXcel
"""
def main1():
    filename = "frequency"
    f = xlwt.Workbook()
    sheet = f.add_sheet('sheet')
    a = read_list('root', '58424716', 'dianping')
    for remark in a:
        wordfrequency(remark[11])
    results = sorted(result.items(), key=lambda x: x[1], reverse=True)  # 排序
    count = 0
    for item in results:
        sheet.write(count, 0, item[0])
        sheet.write(count, 1, item[1])
        count += 1
        print(count)
    f.save('%s.xls' % filename)

"""
带标签写入excel
"""
def main2():
    filename = "frequency2"
    f = xlwt.Workbook()
    sheet = f.add_sheet('sheet')
    a = read_list('root', '58424716', 'dianping')
    for remark in a:
        wordfrequency_tag(remark[11])
    results = sorted(result.items(), key=lambda x: x[1], reverse=True)  # 排序
    count = 0
    for item in results:
        # print(item[0][0],item[0][1],item[1])
        sheet.write(count, 0, item[0][0])
        sheet.write(count, 1, item[0][1])
        sheet.write(count, 2, item[1])
        count += 1
    f.save('%s.xls' % filename)


def create_database(usr, pwd, db):
    global conn
    try:
        conn = mysql.connector.connect(user=usr, password=pwd, database=db)
        cursor = conn.cursor()
        cursor.execute(
            'create table word_frequency (word_name varchar(255), word_tag varchar(20),'
            '  word_times  INT,'
            'flag bool ,primary key (word_name,word_tag)  ) ')
        conn.commit()
        cursor.close()
    except mysql.connector.Error as e:
        print("创建数据库出问题啦", e)

def insert_frequency(word_name, word_tag, word_times):
    global conn2
    conn2 = mysql.connector.connect(user='root', password='58424716', database='dianping', charset='utf8mb4')
    cursor = conn2.cursor()
    cursor.execute(
        'INSERT INTO word_frequency (word_name , word_tag ,word_times,flag )'
        'VALUES (%s, %s, %s, %s);',
        (word_name, word_tag, word_times,False))
    conn2.commit()
    cursor.close()
    print(word_name , word_tag ,word_times,"插入成功")


"""
带标签写入mysql
"""
def main3():
    create_database('root', '58424716', 'dianping')
    a = read_list('root', '58424716', 'dianping')
    for remark in a:
        wordfrequency_tag(remark[11])
    results = sorted(result.items(), key=lambda x: x[1], reverse=True)  # 排序
    count = 0
    for item in results:
        # print(item[0][0],item[0][1],item[1])
        try:
            insert_frequency(item[0][0],item[0][1],item[1])
        except BaseException as e:
            print("存储词频出错啦", item[0][0],item[0][1],item[1],e)
            with open('error_word.txt', 'a') as error_wordLog:
                error_wordLog.writelines("时间：" + datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S") + item[0][0]+item[0][1]+str(item[1]) + "\n")
    conn2.close()

def single_review_sentiment_score(review):
    single_review_senti_score = []
    cuted_review = tp.cut_sentence_2(review)
    print(cuted_review)

#
# 	for sent in cuted_review:
# 		seg_sent = tp.segmentation(sent, 'list')
# 		i = 0 # word position counter
# 		s = 0 # sentiment word position
# 		poscount = 0 # count a positive word
# 		negcount = 0 # count a negative word
#
# 		for word in seg_sent:
# 			if word in posdict:
# 				poscount += 1
# 				for w in seg_sent[s:i]:
# 					poscount = match(w, poscount)
# 				a = i + 1
#
# 			elif word in negdict:
# 				negcount += 1
# 				for w in seg_sent[s:i]:
# 					negcount = match(w, negcount)
# 				a = i + 1
#
# 			# Match "!" in the review, every "!" has a weight of +2
# 			elif word == "！".decode('utf8') or word == "!".decode('utf8'):
# 				for w2 in seg_sent[::-1]:
# 					if w2 in posdict:
# 						poscount += 2
# 						break
# 					elif w2 in negdict:
# 						negcount += 2
# 						break
# 			i += 1
#
# 		single_review_senti_score.append(transform_to_positive_num(poscount, negcount))
# 		review_sentiment_score = sumup_sentence_sentiment_score(single_review_senti_score)
#
# 	return review_sentiment_score

if __name__ == '__main__':
    rew="强烈建议不要在only官网买衣服。官网都是在各个门店调货，衣服质量不敢恭维 ，好多衣服都是门店卖不出去的给发出来了吧。而且客服你推我我推你，有了问题咨询，至于的来回转客服吗？！每个都说不归自己管，要转其他客服。给大家发图，大家看吧，这件衣服少了胸针，没有胸针的大衣，简直&hellip;&hellip;而且胸针没有，还不给补发。反正以后是不会在官网买了"
    single_review_sentiment_score(rew)