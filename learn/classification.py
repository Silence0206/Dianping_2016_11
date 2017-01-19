#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
import time
from sklearn import metrics
import pickle as pickle
import pandas as pd

"""
学姐的
"""


# Multinomial Naive Bayes Classifier
def naive_bayes_classifier(train_x, train_y):
    from sklearn.naive_bayes import MultinomialNB
    model = MultinomialNB(alpha=0.01)
    model.fit(train_x, train_y)
    return model


# KNN Classifier
def knn_classifier(train_x, train_y):
    from sklearn.neighbors import KNeighborsClassifier
    model = KNeighborsClassifier()
    model.fit(train_x, train_y)
    return model


# Logistic Regression Classifier
def logistic_regression_classifier(train_x, train_y):
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(penalty='l2')
    model.fit(train_x, train_y)
    return model


# Random Forest Classifier
def random_forest_classifier(train_x, train_y):
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=8)
    model.fit(train_x, train_y)
    return model


# Decision Tree Classifier
def decision_tree_classifier(train_x, train_y):
    from sklearn import tree
    model = tree.DecisionTreeClassifier()
    model.fit(train_x, train_y)
    return model


# GBDT(Gradient Boosting Decision Tree) Classifier
def gradient_boosting_classifier(train_x, train_y):
    from sklearn.ensemble import GradientBoostingClassifier
    model = GradientBoostingClassifier(n_estimators=200)
    model.fit(train_x, train_y)
    return model


# SVM Classifier
def svm_classifier(train_x, train_y):
    from sklearn.svm import SVC
    model = SVC(kernel='rbf', probability=True)
    model.fit(train_x, train_y)
    return model

# SVM Classifier using cross validation
def svm_cross_validation(train_x, train_y):
    from sklearn.grid_search import GridSearchCV
    from sklearn.svm import SVC
    model = SVC(kernel='rbf', probability=True)
    param_grid = {'C': [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000], 'gamma': [0.001, 0.0001]}
    grid_search = GridSearchCV(model, param_grid, n_jobs = 1, verbose=1)
    grid_search.fit(train_x, train_y)
    best_parameters = grid_search.best_estimator_.get_params()
    for para, val in list(best_parameters.items()):
        print(para, val)
    model = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True)
    model.fit(train_x, train_y)
    return model

def read_data(data_file):
    X = []
    Y = []
    data = pd.read_csv(data_file)
    for avg_sentiment,sales in zip(data['avg_sentiment'],data['sales']):
        X.append([float(avg_sentiment)])
        Y.append(float(sales))
    # train_y = Y[:int(len(data)*0.9)]
    # test_y = Y[int(len(data)*0.9):]
    # train_x = X[:int(len(data)*0.9)]
    # test_x = X[int(len(data)*0.9):]
    # train_x = np.array(train_x)
    # test_y=np.array(test_y)
    # train_x=np.array(train_x)
    # test_x=np.array(test_x)
    # return train_x, train_y, test_x, test_y
    return X,Y

if __name__ == '__main__':
    data_file = "shuju_liangye.csv"
    thresh = 0.5
    model_save_file = None
    model_save = {}

    # test_classifiers = ['NB', 'KNN', 'LR', 'RF', 'DT', 'SVM','SVMCV', 'GBDT']
    # classifiers = {'NB':naive_bayes_classifier,
    #               'KNN':knn_classifier,
    #                'LR':logistic_regression_classifier,
    #                'RF':random_forest_classifier,
    #                'DT':decision_tree_classifier,
    #               'SVM':svm_classifier,
    #             'SVMCV':svm_cross_validation,
    #              'GBDT':gradient_boosting_classifier
    # }
    test_classifiers = ['NB', 'KNN', 'LR', 'RF', 'DT', 'SVM', 'GBDT']
    classifiers = {'NB':naive_bayes_classifier,
                  'KNN':knn_classifier,
                   'LR':logistic_regression_classifier,
                   'RF':random_forest_classifier,
                   'DT':decision_tree_classifier,
                  'SVM':svm_classifier,
                 'GBDT':gradient_boosting_classifier
    }




    print('reading training and testing data...')
    X, Y = read_data(data_file)
    train_y = Y[:int(len(Y)*0.7)]
    test_y = Y[int(len(Y)*0.7):]
    train_x = X[:int(len(X)*0.7)]
    test_x = X[int(len(X)*0.7):]

    # test_x = [[7.711538462],[6.094339623],[8.108333333]]
    # test_y = [1,-1,-1]

    for classifier in test_classifiers:
        print('******************* %s ********************' % classifier)
        start_time = time.time()
        model = classifiers[classifier](train_x, train_y)
        # print('training took %fs!' % (time.time() - start_time))
        predict = model.predict(test_x)
        if model_save_file != None:
            model_save[classifier] = model
        precision = metrics.precision_score(test_y, predict)
        recall = metrics.recall_score(test_y, predict)
        print('precision: %.2f%%, recall: %.2f%%' % (100 * precision, 100 * recall))
        accuracy = metrics.accuracy_score(test_y, predict)
        # print('accuracy: %.2f%%' % (100 * accuracy))
        # 打点，画图
        plt.scatter(train_x,train_y,c='k',label='data')
        plt.hold('on')
        plt.plot(train_x, model.predict(train_x), c='g', label='classification model')
        plt.xlabel('avg_sentiment')
        plt.ylabel('sales')
        plt.title('classification')
        plt.legend()
        plt.show()

    if model_save_file != None:
        pickle.dump(model_save, open(model_save_file, 'wb'))




# data_file = "shuju_banye.csv"
# # train_x, train_y, test_x, test_y = read_data(data_file)
# X,Y=read_data(data_file)
# model = naive_bayes_classifier(X,Y)
# predict = model.predict([400])
# print predict