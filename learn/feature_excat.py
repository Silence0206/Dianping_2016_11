# -*- coding: utf-8 -*-

"""
应用scikit-learn做文本分类
http://blog.csdn.net/abcjennifer/article/details/23615947
"""
#1 特征提取 保证训练集和测试机特征维度相同
# Method 2. CountVectorizer+TfidfTransformer
def method2(newsgroup_train,newsgroups_test):
    print('*************************\nCountVectorizer+TfidfTransformer\n*************************')
    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

    count_v1 = CountVectorizer(stop_words='english', max_df=0.5)
    counts_train = count_v1.fit_transform(newsgroup_train.data)
    print("the shape of train is " + repr(counts_train.shape))

    count_v2 = CountVectorizer(vocabulary=count_v1.vocabulary_)
    counts_test = count_v2.fit_transform(newsgroups_test.data)
    print("the shape of test is " + repr(counts_test.shape))

    tfidftransformer = TfidfTransformer()

    tfidf_train = tfidftransformer.fit(counts_train).transform(counts_train)
    tfidf_test = tfidftransformer.fit(counts_test).transform(counts_test)

#Method 3. TfidfVectorizer 让两个TfidfVectorizer共享vocabulary：
def method3(newsgroup_train,newsgroups_test):
    print('*************************\nTfidfVectorizer\n*************************')
    from sklearn.feature_extraction.text import TfidfVectorizer
    tv = TfidfVectorizer(sublinear_tf=True,
                         max_df=0.5,
                         stop_words='english')
    tfidf_train_2 = tv.fit_transform(newsgroup_train.data)
    tv2 = TfidfVectorizer(vocabulary=tv.vocabulary_)
    tfidf_test_2 = tv2.fit_transform(newsgroups_test.data)
    print("the shape of train is " + repr(tfidf_train_2.shape))
    print("the shape of test is " + repr(tfidf_test_2.shape))
    analyze = tv.build_analyzer()
    tv.get_feature_names()  # statistical features/terms