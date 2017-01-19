#!/usr/bin/env python
# -*- coding=gbk -*-
from gensim import corpora, models, similarities
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
import jieba


"""
     原始数据，用于建立模型
"""
# 缩水版的courses，实际数据的格式应该为 课程名\t课程简介\t课程详情，并已去除html等干扰因素
courses = [
    u'Writing II: Rhetorical Composing',
    u'Genetics and Society: A Course for Educators',
    u'General Game Playing',
    u'Genes and the Human Condition (From Behavior to Biotechnology)',
    u'A Brief History of Humankind',
    u'New Models of Business in Society',
    u'Analyse Numrique pour Ingnieurs',
    u'Evolution: A Course for Educators',
    u'Coding the Matrix: Linear Algebra through Computer Science Applications',
    u'The Dynamic Earth: A Course for Educators',
    u'Tiny Wings\tYou have always dreamed of flying - but your wings are tiny. Luckily the world is full of beautiful hills. Use the hills as jumps - slide down, flap your wings and fly! At least for a moment - until this annoying gravity brings you back down to earth. But the next hill is waiting for you already. Watch out for the night and fly as fast as you can. ',
    u'Angry Birds Free',
    u'没有\它很相似',
    u'没有\t它很相似',
    u'没有\t他很相似',
    u'没有\t他不很相似',
    u'没有',
    u'可以没有',
    u'也没有',
    u'有没有也不管',
    u'Angry Birds Stella',
    u'Flappy Wings - FREE\tFly into freedom!A parody of the #1 smash hit game!',
    u'没有一个',
    u'没有一个2',
]

# 只是为了最后的查看方便
# 实际的 courses_name = [course.split('\t')[0] for course in courses]
courses_name = courses
path="G:\Dianping2017\Dianping_2016_11"
"""
    预处理(easy_install nltk)
"""


def pre_process_cn(courses, low_freq_filter=True):
    """
     简化的 中文+英文 预处理
        1.去掉停用词
        2.去掉标点符号
        3.处理为词干
        4.去掉低频词

    """
    import nltk
    import jieba.analyse
    from nltk.tokenize import word_tokenize

    texts_tokenized = []
    for document in courses:
        texts_tokenized_tmp = []
        for word in word_tokenize(document):
            texts_tokenized_tmp += jieba.analyse.extract_tags(word, 10)
        texts_tokenized.append(texts_tokenized_tmp)

    texts_filtered_stopwords = texts_tokenized

    # 去除标点符号
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    texts_filtered = [[word for word in document if not word in english_punctuations] for document in
                      texts_filtered_stopwords]

    # 词干化
    from nltk.stem.lancaster import LancasterStemmer
    st = LancasterStemmer()
    texts_stemmed = [[st.stem(word) for word in docment] for docment in texts_filtered]

    # 去除过低频词
    if low_freq_filter:
        all_stems = sum(texts_stemmed, [])
        stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
        texts = [[stem for stem in text if stem not in stems_once] for text in texts_stemmed]
    else:
        texts = texts_stemmed
    return texts

lib_texts = pre_process_cn(courses)
print(lib_texts)
"""
    引入gensim，正式开始处理(easy_install gensim)
"""

#http://www.52nlp.cn/%E5%A6%82%E4%BD%95%E8%AE%A1%E7%AE%97%E4%B8%A4%E4%B8%AA%E6%96%87%E6%A1%A3%E7%9A%84%E7%9B%B8%E4%BC%BC%E5%BA%A6%E4%BA%8C
def train_by_lsi(lib_texts):
    """
        通过LSI模型的训练
    """
    from gensim import corpora, models, similarities

    # 为了能看到过程日志
    # import logging
    # logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    dictionary = corpora.Dictionary(lib_texts)
    dictionary.save(path+'/tmp/deerwester.dict')
    print("==token2id=")
    print(dictionary.token2id)
    #{'angry': 13, 'socy': 0, '相似': 16, 'cours': 2, 'gen': 3, 'bird': 15, 'ear': 5, 'hil': 10, 'gam': 4, 'down': 12, 'fre': 14, 'wing': 6, 'fly': 7, '一个': 18, 'tiny': 11, 'but': 8, 'yo': 9, 'educ': 1, '没有': 17}
    corpus = [dictionary.doc2bow(text) for text in
              lib_texts]  # doc2bow(): 将collection words 转为词袋，用两元组(word_id, word_frequency)表示
    print(corpus)
    tfidf = models.TfidfModel(corpus)
    print(tfidf)
    corpus_tfidf = tfidf[corpus] #基于这个TF-IDF模型，我们可以将上述用词频表示文档向量表示为一个用tf-idf值表示的文档向量 也就是原来的词频变成TF-IDF值
    # for doc in corpus_tfidf: #http://www.cnblogs.com/hanacode/articles/4819328.html
    #     print(doc)

    # 拍脑袋的：训练topic数量为10的LSI模型
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=11)
    for t in lsi.print_topics(11):
        print(t)#一行一个topic
    index = similarities.MatrixSimilarity(lsi[corpus])  # index 是 gensim.similarities.docsim.MatrixSimilarity 实例

    return (index, dictionary, lsi)

# train_by_lsi(lib_texts)
dic = corpora.Dictionary.load(path+'/tmp/deerwester.dict')
print(dic)