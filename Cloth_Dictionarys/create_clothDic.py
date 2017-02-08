# *- coding: utf-8 -*-
import mysql.connector
import datetime
import re
import jieba
import jieba.posseg #需要另外加载一个词性标注模块
import time
import logging
import os
import  codecs
"""
get到的cwd是当前目录
用于构造用户词典（用来使分词更准确）
对于合并多个搜狗词库存进的TXT消除重复行
"""
#去某一行前后的空格 去末尾空格 消除重复行返回set
def clear_dic(filepath):
    txt_file1 = codecs.open(filepath, 'r', encoding='utf-8')
    txt_tmp1 = txt_file1.readlines()
    txt_tmp2 = ''.join(txt_tmp1).replace(' ', '').strip()#删除整个文档末尾的空格和每一行结尾的空格
    print(repr(txt_tmp2))
    txt_data1 = txt_tmp2.split('\r\n')
    txt_file1.close()
    return set(txt_data1)

"""
存储去重完毕的未写词频的字典
参数1 存储带有重复的字典路径
参数2 将要把去重完毕吃字典存储在哪
"""
def store_Dic(repeatpath,storepath):
    outfile = codecs.open(storepath, 'a', encoding='utf-8')
    sets=clear_dic(repeatpath)
    for item in sets:
        outfile.writelines(item+"\n")
    outfile.close()

"""
在去重完毕的基础加上词频
"""
def write_word_frequency(dictpath, storepath,frequency):
    # 把txt文件里面的词存储成一个数组
    txt_file = open(dictpath, 'r', encoding='utf-8')
    txt_tmp1 = txt_file.readlines()
    txt_tmp2 = ''.join(txt_tmp1)
    print(repr(txt_tmp2))
    dict_data = txt_tmp2.split('\n')
    print(dict_data)
    txt_file.close()

    # 把词频添加到txt文件中
    userdict = open(storepath, 'w', encoding='utf-8')
    for word in dict_data:
        userdict.write(word + ' '+frequency+ '\n')
    userdict.close()
def main1():
    rawpath = os.getcwd()
    store_Dic(rawpath+"\clothDic_raw.txt",rawpath+"\clothDic_filter.txt")
def main2():
    rawpath = os.getcwd()
    write_word_frequency(rawpath+"\clothDic_filter.txt",rawpath+"\clothDic_frequency.txt",'3')


if __name__ == '__main__':
    rawpath = os.getcwd()
    with open(rawpath+"\clothDic_frequency.txt",'r', encoding='utf-8') as f:
        x = f.readlines()
        print(x)
