# *- coding: utf-8 -*-
import jieba
import  wordcloud
import re
import string
import  xlwt
import mysql.connector
import datetime
import jieba.posseg #需要另外加载一个词性标注模块
"""
构造自己的情感词典初步--统计词频
"""
jieba.load_userdict("G:\Dianping\Dictionary\segmentation dictionary\segdict1.txt")
jieba.load_userdict("G:\Dianping\Dictionary\segmentation dictionary\segdict2.txt")

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
    sub_re='[a-zA-Z]+|[\s+\.\!\/_,$%^*\(\d+\"\']+|[+—；—！:\(\)：《》，。？、~@#￥%……&*（）％～\[\]\|\?\·【】“”;-]+'
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


