#!/usr/bin/env python
# -*- coding=gbk -*-
from gensim import corpora, models, similarities
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
import jieba


"""
     ԭʼ���ݣ����ڽ���ģ��
"""
# ��ˮ���courses��ʵ�����ݵĸ�ʽӦ��Ϊ �γ���\t�γ̼��\t�γ����飬����ȥ��html�ȸ�������
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
    u'û��\��������',
    u'û��\t��������',
    u'û��\t��������',
    u'û��\t����������',
    u'û��',
    u'����û��',
    u'Ҳû��',
    u'��û��Ҳ����',
    u'Angry Birds Stella',
    u'Flappy Wings - FREE\tFly into freedom!A parody of the #1 smash hit game!',
    u'û��һ��',
    u'û��һ��2',
]

# ֻ��Ϊ�����Ĳ鿴����
# ʵ�ʵ� courses_name = [course.split('\t')[0] for course in courses]
courses_name = courses
path="G:\Dianping2017\Dianping_2016_11"
"""
    Ԥ����(easy_install nltk)
"""


def pre_process_cn(courses, low_freq_filter=True):
    """
     �򻯵� ����+Ӣ�� Ԥ����
        1.ȥ��ͣ�ô�
        2.ȥ��������
        3.����Ϊ�ʸ�
        4.ȥ����Ƶ��

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

    # ȥ��������
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    texts_filtered = [[word for word in document if not word in english_punctuations] for document in
                      texts_filtered_stopwords]

    # �ʸɻ�
    from nltk.stem.lancaster import LancasterStemmer
    st = LancasterStemmer()
    texts_stemmed = [[st.stem(word) for word in docment] for docment in texts_filtered]

    # ȥ������Ƶ��
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
    ����gensim����ʽ��ʼ����(easy_install gensim)
"""

#http://www.52nlp.cn/%E5%A6%82%E4%BD%95%E8%AE%A1%E7%AE%97%E4%B8%A4%E4%B8%AA%E6%96%87%E6%A1%A3%E7%9A%84%E7%9B%B8%E4%BC%BC%E5%BA%A6%E4%BA%8C
def train_by_lsi(lib_texts):
    """
        ͨ��LSIģ�͵�ѵ��
    """
    from gensim import corpora, models, similarities

    # Ϊ���ܿ���������־
    # import logging
    # logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    dictionary = corpora.Dictionary(lib_texts)
    dictionary.save(path+'/tmp/deerwester.dict')
    print("==token2id=")
    print(dictionary.token2id)
    #{'angry': 13, 'socy': 0, '����': 16, 'cours': 2, 'gen': 3, 'bird': 15, 'ear': 5, 'hil': 10, 'gam': 4, 'down': 12, 'fre': 14, 'wing': 6, 'fly': 7, 'һ��': 18, 'tiny': 11, 'but': 8, 'yo': 9, 'educ': 1, 'û��': 17}
    corpus = [dictionary.doc2bow(text) for text in
              lib_texts]  # doc2bow(): ��collection words תΪ�ʴ�������Ԫ��(word_id, word_frequency)��ʾ
    print(corpus)
    tfidf = models.TfidfModel(corpus)
    print(tfidf)
    corpus_tfidf = tfidf[corpus] #�������TF-IDFģ�ͣ����ǿ��Խ������ô�Ƶ��ʾ�ĵ�������ʾΪһ����tf-idfֵ��ʾ���ĵ����� Ҳ����ԭ���Ĵ�Ƶ���TF-IDFֵ
    # for doc in corpus_tfidf: #http://www.cnblogs.com/hanacode/articles/4819328.html
    #     print(doc)

    # ���Դ��ģ�ѵ��topic����Ϊ10��LSIģ��
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=11)
    for t in lsi.print_topics(11):
        print(t)#һ��һ��topic
    index = similarities.MatrixSimilarity(lsi[corpus])  # index �� gensim.similarities.docsim.MatrixSimilarity ʵ��

    return (index, dictionary, lsi)

# train_by_lsi(lib_texts)
dic = corpora.Dictionary.load(path+'/tmp/deerwester.dict')
print(dic)