# *- coding: utf-8 -*-

"""
http://blog.csdn.net/abcjennifer/article/details/23615947
"""
#first extract the 20 news_group dataset to /scikit_learn_data
from sklearn.datasets import fetch_20newsgroups
#all categories
#newsgroup_train = fetch_20newsgroups(subset='train')
#part categories
categories = ['comp.graphics',
 'comp.os.ms-windows.misc',
 'comp.sys.ibm.pc.hardware',
 'comp.sys.mac.hardware',
 'comp.windows.x']
newsgroup_train = fetch_20newsgroups(subset = 'train',categories = categories)

def calculate_result(actual,pred):
    m_precision = metrics.precision_score(actual,pred)
    m_recall = metrics.recall_score(actual,pred)
    print( 'predict info:')
    print ('precision:{0:.3f}'.format(m_precision))
    print( 'recall:{0:0.3f}'.format(m_recall))
    print ('f1-score:{0:.3f}'.format(metrics.f1_score(actual,pred)))
    

#print category names
from pprint import pprint
pprint(list(newsgroup_train.target_names))



#newsgroup_train.data is the original documents, but we need to extract the 
#TF-IDF vectors inorder to model the text data
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer
#vectorizer = TfidfVectorizer(sublinear_tf = True,
#                           max_df = 0.5,
#                           stop_words = 'english');
#however, Tf-Idf feather extractor makes the training set and testing set have
#divergent number of features. (Because they have different vocabulary in documents)
#So we use HashingVectorizer
vectorizer = HashingVectorizer(stop_words = 'english',non_negative = True,
                               n_features = 100)
fea_train = vectorizer.fit_transform(newsgroup_train.data)
#return feature vector 'fea_train' [n_samples,n_features]
print ('Size of fea_train:' + repr(fea_train.shape))
#11314 documents, 130107 vectors for all categories
print ('The average feature sparsity is {0:.3f}%'.format(
fea_train.nnz/float(fea_train.shape[0]*fea_train.shape[1])*100))


######################################################
#Multinomial Naive Bayes Classifier
print('*************************\nNaive Bayes\n*************************')
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
newsgroups_test = fetch_20newsgroups(subset = 'test',
                                     categories = categories)
fea_test = vectorizer.fit_transform(newsgroups_test.data)
#create the Multinomial Naive Bayesian Classifier
clf = MultinomialNB(alpha = 0.01) 
clf.fit(fea_train,newsgroup_train.target)
pred = clf.predict(fea_test)
calculate_result(newsgroups_test.target,pred)
#notice here we can see that f1_score is not equal to 2*precision*recall/(precision+recall)
#because the m_precision and m_recall we get is averaged, however, metrics.f1_score() calculates
#weithed average, i.e., takes into the number of each class into consideration.

######################################################
#KNN Classifier
from sklearn.neighbors import KNeighborsClassifier
print ('*************************\nKNN\n*************************')
knnclf = KNeighborsClassifier()#default with k=5
knnclf.fit(fea_train,newsgroup_train.target)
pred = knnclf.predict(fea_test)
calculate_result(newsgroups_test.target,pred)

######################################################
#SVM Classifier
from sklearn.svm import SVC
print ('*************************\nSVM\n*************************')
svclf = SVC(kernel = 'linear')#default with 'rbf'
svclf.fit(fea_train,newsgroup_train.target)
pred = svclf.predict(fea_test)
calculate_result(newsgroups_test.target,pred)

######################################################
#KMeans Cluster
from sklearn.cluster import KMeans
print ('*************************\nKMeans\n*************************')
pred = KMeans(n_clusters=5)
pred.fit(fea_test)
calculate_result(newsgroups_test.target,pred.labels_)
