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
本文件用于处理大众点评的
"""
"""
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

#调用clear_dic
#把不重重复的set写入文档
#原来195870 消除重复后194404
#segdict3.txt含有重复的
#segdict2.txt消除重复的
def main_write():
    outfile = codecs.open('G:\Dianping\Dictionary\original segmentation dictionary source\dic1.txt', 'a', encoding='utf-8')
    sets=clear_dic('G:\Dianping\Dictionary\original segmentation dictionary source\sougouDic.txt')
    for item in sets:
        outfile.writelines(item+"\n")
    outfile.close()


def write_word_frequency(dictpath, storepath):
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
        userdict.write(word + ' 3' + '\n')
    userdict.close()

if __name__ == '__main__':
    write_word_frequency("G:\Dianping\Dictionary\segmentation dictionary\segdict3.txt","G:\Dianping\Dictionary\segmentation dictionary\segdict2.txt")
