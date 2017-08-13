import random
from datetime import datetime
import pandas as pd
import time


validasof= time.time()

adsselected = []
reward=0
samples = 0

#list of banners -assume they are named by brandnames.
adimages =['birch','armani','chloe','prada','espirit','Doir','Diesel','Vougue','Zara','Boss']


#Depending on number of images for the slot we will initialize
numberofrewards_1 = [0] * len(adimages)
numberofrewards_0 = [0] * len(adimages)

totalrewards = 0

'''
Considering we got region, imagekey and then a value of true or false as outcome,
this function will normalize this.
:return:
'''
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
dataset = pd.read_csv("clickdata.csv", sep=",", header=None)

random.seed(random.randrange(100,200))
samples = len(dataset)
data = dataset.iloc[:, [0,2]].values

# Y = dataset.iloc[:, 5].values

labelencodeImage = LabelEncoder()
labelencodecity = LabelEncoder()
data[:, 0] = labelencodeImage.fit_transform(data[:, 0])
data[:, 1] = labelencodecity.fit_transform(data[:, 1])

onehotencoderimage = OneHotEncoder(categorical_features=[0])
data = onehotencoderimage.fit_transform(data).toarray()

'''Dummy variable issue'''
        #data = data[:, 1:]

#We will iterate through each of the samples.

for sample in range(0,samples):

    selectedad = 0
    #this is required as we take the max random draw from each ads
    max_random = 0

    #for each ad image, calculate the randombeta
    for ad in range(0,len(adimages)):
        randombeta = random.betavariate(numberofrewards_1[ad] +1,
                                    numberofrewards_0[ad]+1)
       
        #as per the thompsonsampling, we need to take the maximum of the beta dist and set the ad which needs to showup.
        if randombeta > max_random:
            max_random = randombeta
            selectedad = ad

    adsselected.append(selectedad)

    # review if the bannerselected in dataset and click= true
    reward = (data[sample,selectedad]==1 and data[sample,10])
    print("Selectedad:{0}-Excelad:{1}-clicked:{2}-reward{3}".format(
            selectedad,
            data[sample,selectedad],
            data[sample,10],
            reward
            ))
    if reward == 1:
        numberofrewards_1[selectedad] = numberofrewards_1[selectedad] + 1
    else:
        numberofrewards_0[selectedad] = numberofrewards_0[selectedad] + 1

    totalrewards = totalrewards + reward

    print(totalrewards)

tsuccess=0
tfail = 0
for index in range(0,10):
    tsuccess += numberofrewards_1[index]
    tfail+=numberofrewards_0[index]

print(tsuccess)
print(tfail)
