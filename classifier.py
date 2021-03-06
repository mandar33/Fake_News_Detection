# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 12:58:52 2017

@author: NishitP
"""

import DataPrep
import FeatureSelection
import numpy as np
import pandas as pd
import pickle
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import  LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import KFold
from sklearn import metrics, confusion_matrix, f1_score
from sklearn.model_selection import GridSeachCV
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt



#the feature selection has been done in FeatureSelection.py module. here we will create models using those features for prediction

#first we will use bag of words techniques

#building classifier using naive bayes 
nb_pipeline = Pipeline([
        ('NBCV',FeatureSelection.countV),
        ('nb_clf',MultinomialNB())])

nb_pipeline.fit(DataPrep.train_news['Statement'],DataPrep.train_news['Label'])

predicted_nb = nb_pipeline.predict(DataPrep.test_news['Statement'])
np.mean(predicted_nb == DataPrep.test_news['Label'])
#accuracy = 0.61


#building classifier using logistic regression
logR_pipeline = Pipeline([
        ('LogRCV',FeatureSelection.countV),
        ('LogR_clf',LogisticRegression())
        ])

logR_pipeline.fit(DataPrep.train_news['Statement'],DataPrep.train_news['Label'])

predicted_LogR = logR_pipeline.predict(DataPrep.test_news['Statement'])
np.mean(predicted_LogR == DataPrep.test_news['Label'])
#accuracy = 0.61


#building Linear SVM classfier
svm_pipeline = Pipeline([
        ('svmCV',FeatureSelection.countV),
        ('svm_clf',svm.SVC())
        ])

svm_pipeline.fit(DataPrep.train_news['Statement'],DataPrep.train_news['Label'])

predicted_svm = svm_pipeline.predict(DataPrep.test_news['Statement'])
np.mean(predicted_svm == DataPrep.test_news['Label'])
#accuracy = 0.56


#using SVM Stochastic Gradient Descent on squared_hinge loss
sgd_pipeline = Pipeline([
        ('svm2CV',FeatureSelection.countV),
        ('svm2_clf',SGDClassifier(loss='squared_hinge', penalty='l2', alpha=1e-3, n_iter=5))
        ])

sgd_pipeline.fit(DataPrep.train_news['Statement'],DataPrep.train_news['Label'])

predicted_sgd = sgd_pipeline.predict(DataPrep.test_news['Statement'])
np.mean(predicted_sgd == DataPrep.test_news['Label'])
#accurary = 0.58

#random forest
random_forest = Pipeline([
        ('rfCV',FeatureSelection.countV),
        ('rf_clf',RandomForestClassifier(n_estimators=300,n_jobs=3))
        ])
    
random_forest.fit(DataPrep.train_news['Statement'],DataPrep.train_news['Label'])
predicted_rf = random_forest.predict(DataPrep.test_news['Statement'])
np.mean(predicted_rf == DataPrep.test_news['Label'])



#User defined functon for K-Fold cross validatoin
def build_confusion_matrix(classifier):
    
    k_fold = KFold(n=len(DataPrep.train_news), n_folds=5)
    scores = []
    confusion = np.array([[0,0],[0,0]])

    for train_ind, test_ind in k_fold:
        train_text = DataPrep.train_news.iloc[train_ind]['Statement'] 
        train_y = DataPrep.train_news.iloc[train_ind]['Label']
    
        test_text = DataPrep.train_news.iloc[test_ind]['Statement']
        test_y = DataPrep.train_news.iloc[test_ind]['Label']
        
        classifier.fit(train_text,train_y)
        predictions = classifier.predict(test_text)
        
        confusion += confusion_matrix(test_y,predictions)
        score = f1_score(test_y,predictions)
        scores.append(score)
    
    return (print('Total statements classified:', len(DataPrep.train_news)),
    print('Score:', sum(scores)/len(scores)),
    print('score length', len(scores)),
    print('Confusion matrix:'),
    print(confusion))
    
#K-fold cross validation for all classifiers
build_confusion_matrix(nb_pipeline)
build_confusion_matrix(logR_pipeline)
build_confusion_matrix(svm_pipeline)
build_confusion_matrix(sgd_pipeline)
build_confusion_matrix(random_forest)

#========================================================================================
#Bag of words confusion matrix and F1 scores

#Naive bayes
# [2118 2370]
# [1664 4088]
#0.669611539651

#Logistic regression
# [2252 2236]
# [1933 3819]
# 0.646909097798

#svm
# [0 4488]
# [ 0 5752]
# 0.719313230705

#sgdclassifier
# [2535 1953]
# [2502 3250]
# 0.590245654241

#random forest classifier
# [1821 2667]
# [1192 4560]
#Score: 0.702651511011
#=========================================================================================

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(DataPrep.train_news['Statement'].values)
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)

"""Usinng n-grams, stopwords etc """
##Now using n-grams
#naive-bayes classifier
nb_pipeline_ngram = Pipeline([
        #('NBCV',countV_ngram),
        ('nb_tfidf',FeatureSelection.tfidf_ngram),
        ('nb_clf',MultinomialNB())])

nb_pipeline_ngram.fit(DataPrep.train_news['Statement'],DataPrep.train_news['Label'])

predicted_nb_ngram = nb_pipeline_ngram.predict(DataPrep.test_news['Statement'])
np.mean(predicted_nb_ngram == DataPrep.test_news['Label'])
#accuracy = 0.60

#logistic regression classifier
logR_pipeline_ngram = Pipeline([
        #('LogRCV',countV_ngram),
        ('LogR_tfidf',FeatureSelection.tfidf_ngram),
        ('LogR_clf',LogisticRegression(penalty="l2",C=1))
        ])

logR_pipeline_ngram.fit(DataPrep.train_news['Statement'],DataPrep.train_news['Label'])

predicted_LogR_ngram = logR_pipeline_ngram.predict(DataPrep.test_news['Statement'])
np.mean(predicted_LogR_ngram == DataPrep.test_news['Label'])
#accuracy = 0.62

#linear SVM classifier
svm_pipeline_ngram = Pipeline([
        ('svm_tfidf',FeatureSelection.tfidf_ngram),
        ('svm_clf',svm.SVC())
        ])

svm_pipeline_ngram.fit(DataPrep.train_news['Statement'],DataPrep.train_news['Label'])

predicted_svm_ngram = svm_pipeline_ngram.predict(DataPrep.test_news['Statement'])
np.mean(predicted_svm_ngram == DataPrep.test_news['Label'])
#accuracy = 0.56

#sgd classifier
sgd_pipeline_ngram = Pipeline([
         ('sgd_tfidf',FeatureSelection.tfidf_ngram),
         ('sgd_clf',SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5))
         ])

sgd_pipeline_ngram.fit(DataPrep.train_news['Statement'],DataPrep.train_news['Label'])

predicted_sgd_ngram = sgd_pipeline_ngram.predict(DataPrep.train_news['Statement'])
np.mean(predicted_sgd_ngram == DataPrep.train_news['Label'])
#accurary = 0.57

#random forest classifier
random_forest_ngram = Pipeline([
        #('rfCV',FeatureSelection.countV),
        ('rf_tfidf',FeatureSelection.tfidf_ngram),
        ('rf_clf',RandomForestClassifier(n_estimators=100,n_jobs=3))
        ])
    
random_forest_ngram.fit(DataPrep.train_news['Statement'],DataPrep.train_news['Label'])
predicted_rf_ngram = random_forest_ngram.predict(DataPrep.test_news['Statement'])
np.mean(predicted_rf_ngram == DataPrep.test_news['Label'])
#accuracy = 0.61


#K-fold cross validation for all classifiers
build_confusion_matrix(nb_pipeline_ngram)
build_confusion_matrix(logR_pipeline_ngram)
build_confusion_matrix(svm_pipeline_ngram)
build_confusion_matrix(sgd_pipeline_ngram)
build_confusion_matrix(random_forest_ngram)

#========================================================================================
#n-grams & tfidf confusion matrix and F1 scores

#Naive bayes
# [841 3647]
# [427 5325]
# f1-Score: 0.723262051071

#Logistic regression
# [1617 2871]
# [1097 4655]
# f1-Score: 0.70113000531

#svm
# [0 4488]
# [ 0 5752]
# f1-Score: 0.719313230705

#sgdclassifier
# [  10 4478]
# [  13 5739]
# f1-Score: 0.718731637053

#random forest
# [1979 2509]
# [1630 4122]
# f1-Score: 0.665720333284
#=========================================================================================

print(metrics.classification_report(DataPrep.test_news['Label'], predicted_nb_ngram))
print(metrics.classification_report(DataPrep.test_news['Label'], predicted_LogR_ngram))
print(metrics.classification_report(DataPrep.test_news['Label'], predicted_svm_ngram))
print(metrics.classification_report(DataPrep.test_news['Label'], predicted_sgd_ngram))
print(metrics.classification_report(DataPrep.test_news['Label'], predicted_rf_ngram))


#out of all the models fitted, we would take 2 best performing model. we would call them candidate models
# from the confusion matrix, we can see that random forest and logistic regression are best performing 
# in terms of precision and recall (take a look into false positive and true negative counts which appeares
# to be low compared to rest of the models)

#grid-search parameter optimization
#random forest classifier parameters
parameters = {'rf_tfidf__ngram_range': [(1, 1), (1, 2),(1,3),(1,4),(1,5)],
               'rf_tfidf__use_idf': (True, False),
               'rf_clf__max_depth': (1,2,3,4,5,6,7,8,9,10)
}

gs_clf = GridSearchCV(random_forest_ngram, parameters, n_jobs=-1)
gs_clf = gs_clf.fit(DataPrep.train_news['Statement'][:6000],DataPrep.train_news['Label'][:6000])

gs_clf.best_score_
gs_clf.best_params_
gs_clf.cv_results_

#logistic regression parameters
parameters = {'LogR_tfidf__ngram_range': [(1, 1), (1, 2),(1,3),(1,4),(1,5)],
               'LogR_tfidf__use_idf': (True, False),
               'LogR_tfidf__smooth_idf': (True, False)
}

gs_clf = GridSearchCV(logR_pipeline_ngram, parameters, n_jobs=-1)
gs_clf = gs_clf.fit(DataPrep.train_news['Statement'][:10000],DataPrep.train_news['Label'][:10000])

gs_clf.best_score_
gs_clf.best_params_
gs_clf.cv_results_

#by running above command we can find the model with best performing parameters


#running both random forest and logistic regression models again with best parameter found with GridSearch method
random_forest_final = Pipeline([
        ('rf_tfidf',TfidfVectorizer(stop_words='english',ngram_range=(1,3),use_idf=True,smooth_idf=True)),
        ('rf_clf',RandomForestClassifier(n_estimators=400,n_jobs=3,max_depth=10))
        ])
    
random_forest_final.fit(DataPrep.train_news['Statement'],DataPrep.train_news['Label'])
predicted_rf_final = random_forest_final.predict(DataPrep.test_news['Statement'])
np.mean(predicted_rf_final == DataPrep.test_news['Label'])
print(metrics.classification_report(DataPrep.test_news['Label'], predicted_rf_final))

logR_pipeline_final = Pipeline([
        #('LogRCV',countV_ngram),
        ('LogR_tfidf',TfidfVectorizer(stop_words='english',ngram_range=(1,5),use_idf=True,smooth_idf=False)),
        ('LogR_clf',LogisticRegression(penalty="l2",C=1))
        ])

logR_pipeline_final.fit(DataPrep.train_news['Statement'],DataPrep.train_news['Label'])

predicted_LogR_final = logR_pipeline_final.predict(DataPrep.test_news['Statement'])
np.mean(predicted_LogR_final == DataPrep.test_news['Label'])
#accuracy = 0.62
print(metrics.classification_report(DataPrep.test_news['Label'], predicted_LogR_final))


"""
by running both random forest and logistic regression with GridSearch's best parameter estimation, we found that for random 
forest model with n-gram has better accuracty than with the parameter estimated. The logistic regression model with best parameter 
has almost similar performance as n-gram model so logistic regression will be out choice of model for prediction.
"""

doc_new = ["Brazil built a $300 million stadium in the Amazon rainforest that is only going to be used for four World Cup games, and theres no team that can fill it afterwards."]

logR_pipeline_ngram.predict(doc_new)

x = logR_pipeline_ngram.predict_proba(doc_new)
print(x[0][1])

#saving best model to the disk
model_file = 'final_model.sav'
pickle.dump(logR_pipeline_ngram,open(model_file,'wb'))


##np.random.seed(42)
#data = 


"""
#plottig most informative features for random forest
features = random_forest_ngram.named_steps['rf_clf'].feature_importances_
std = np.std([tree.feature_importances_ for tree in random_forest_ngram.named_steps['rf_clf'].estimators_],
             axis=0)

indices = np.argsort(features)#[-20:]

print(train["Statement"].shape[1])

plt.figure()
plt.title("Feature importances")
plt.barh(range(train["Statement"].shape[1]), features[indices],
       color="r", xerr=std[indices], align="center")

plt.yticks(range(train["Statement"].shape[1]), indices)
plt.ylim([-1, train["Statement"].shape[1]])
plt.show()
"""

