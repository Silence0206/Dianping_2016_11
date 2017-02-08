# -*- coding: utf-8 -*-
import os
import gensim
"""
学习迭代器
如果是对于大量的输入语料集或者需要整合磁盘上多个文件夹下的数据，我们可以以迭代器的方式而不是一次性将全部内容读取到内存中来节省 RAM 空间
http://blog.csdn.net/john_xyz/article/details/54706807
"""
class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname),encoding="utf-8"):#对于中文的话事先把每个评论分词好 用空格间隔，一行存一个txt，一共存几个txt分开读
                yield line.split()
print(os.getcwd())
sentences  = MySentences("G:\Dianping2017\Dianping_2016_11\\testtext")
model = gensim.models.Word2Vec(sentences)

for item in sentences:
    print(item)
# for line in open("G:\Dianping2017\Dianping_2016_11\\testtext\\1.txt",encoding="utf-8"):
#     print("====")
#     print(line.strip())