#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 13:02:50 2017

@author: vishnuhari
"""
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
dataset = pd.read_csv("../resources/clickdata.csv", sep=",", header=None)

from sklearn.model_selection import train_test_split
data= dataset.iloc[:, [3,4,5]].values
#Y = dataset.iloc[:, 5].values

labelencodeImage = LabelEncoder()
labelencodeCity = LabelEncoder()
labelclicked = LabelEncoder()

#data= labelencodeImage.fit_transform(data)

data[:,0] = labelencodeImage.fit_transform(data[:,0])
data[:,1] = labelencodeCity.fit_transform(data[:,1])

#data[:,1]= labelencodeImage.fit_transform(data[:, 1])
#data[:, 2] = labelclicked.fit_transform(data[:, 2])

onehotencoderimage = OneHotEncoder(categorical_features=[0])
data= onehotencoderimage.fit_transform(data).toarray()
'''Dummy variable issue'''
data = data[:, 1:]

#onehotencodercity = OneHotEncoder(categorical_features=[9])
#data = onehotencodercity.fit_transform(data).toarray()
#data = data[:,1:]





from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(X,Y, random_state=0,test_size=0.2)



from sklearn.decomposition import KernelPCA
kpca = KernelPCA(n_components=5,kernel='rbf',random_state=0)
X_train = kpca.fit_transform(X_train)
X_test = kpca.fit_transform(X_test)


from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state=0)
classifier.fit(X_train,Y_train)

Y_pred = classifier.predict(Y_test)

from sklearn.metrics import confusion_matrix

cm = confusion_matrix(Y_test,Y_pred)
print(cm)



labelencodeY = LabelEncoder()
Y = labelencodeY.fit_transform(Y)

