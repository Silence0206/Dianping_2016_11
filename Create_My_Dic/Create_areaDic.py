# *- coding: utf-8 -*-
import text_processing as tp
from itertools import chain
import  codecs


#载入基础情感词典
negdic = tp.loadTextWords("G:\Dianping\Dictionary\sentiment dictionary\positive and negative dictionary\_Negdict.txt")
posdic = tp.loadTextWords("G:\Dianping\Dictionary\sentiment dictionary\positive and negative dictionary\Posdict.txt")

#载入程度词典和否定词典
insuf = tp.loadTextWords("G:\Dianping\Dictionary\sentiment dictionary\\adverbs of degree dictionary\\0.5insufficiently.txt")
ish = tp.loadTextWords("G:\Dianping\Dictionary\sentiment dictionary\\adverbs of degree dictionary\\0.8ish.txt")
more = tp.loadTextWords("G:\Dianping\Dictionary\sentiment dictionary\\adverbs of degree dictionary\\1.2more.txt")
over = tp.loadTextWords("G:\Dianping\Dictionary\sentiment dictionary\\adverbs of degree dictionary\\1.5over.txt")
very = tp.loadTextWords("G:\Dianping\Dictionary\sentiment dictionary\\adverbs of degree dictionary\\1.25very.txt")
most = tp.loadTextWords("G:\Dianping\Dictionary\sentiment dictionary\\adverbs of degree dictionary\\2most.txt")
notDic = tp.loadTextWords("G:\Dianping\Dictionary\sentiment dictionary\\adverbs of degree dictionary\\not.txt")
stopwords = tp.loadTextWords("G:\Dianping\Dictionary\stopword\stopword.txt")

#合并上述所有词典 chain合并起来快 allWords长17108
allWords = list(chain(negdic,posdic,insuf,ish,more,over,very,most,notDic,stopwords))

Dics = tp.read_list('root', '58424716', 'dianping',"SELECT * FROM dianping.word_frequency order by word_times desc ")
newWord=[]
for item in Dics:
    if item[0] not in allWords:
        newWord.append(item)

outfile = codecs.open('My_newWords.txt', 'a', encoding='utf-8')
for item in set(newWord):
    outfile.writelines(item[0] + "\n")
outfile.close()