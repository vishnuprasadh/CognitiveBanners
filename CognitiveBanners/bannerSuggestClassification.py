import random
from datetime import datetime

import pandas as pd

import CognitiveBanners.utils as utils
from CognitiveBanners.bannermodel import BannerModel


class BannerSuggestClassification:
    '''
    A Suggestion classifier which uses Reinforcement learning technique to suggest a better appropriate ads.
    '''
    _adsselected = []
    _reward=0

    def __init__(self,platform='ajio',slotname='hero',validasof=datetime.now()):
        self._samples = 0
        self._adimages =[]
        bannerDAO = BannerModel()
        slots= bannerDAO.getSlotBanners(platform,slotname, utils.datetimeInFormat(validasof))
        for slot in slots:
            self._adimages.append(slot[4])

        #Depending on number of images for the slot we will initialize
        self._numberofrewards_1 = [0] * len(self._adimages)
        self._numberofrewards_0 = [0] * len(self._adimages)
        self._totalrewards = 0


    def loadnormalizetestdata(self):
        '''
        Considering we got region, imagekey and then a value of true or false as outcome,
        this function will normalize this.
        :return:
        '''
        from sklearn.preprocessing import OneHotEncoder, LabelEncoder
        dataset = pd.read_csv("../resources/clickdata.csv", sep=",", header=None)
        self._samples = len(dataset)
        self.data = dataset.iloc[:, [3, 4, 5]].values
        # Y = dataset.iloc[:, 5].values

        labelencodeImage = LabelEncoder()
        labelencodecity = LabelEncoder()
        self.data[:, 0] = labelencodeImage.fit_transform(self.data[:, 0])
        self.data[:, 1] = labelencodecity.fit_transform(self.data[:, 1])

        onehotencoderimage = OneHotEncoder(categorical_features=[0])
        self.data = onehotencoderimage.fit_transform(self.data).toarray()
        '''Dummy variable issue'''
        #self.data = self.data[:, 1:]

    def classify(self):
        #We will iterate through each of the samples.
        for sample in range(0,self._samples):

            self._selectedad = 0
            #this is required as we take the max random draw from each ads
            max_random = 0

            #for each ad image, calculate the randombeta
            for ad in range(0,len(self._adimages)):
                randombeta = random.betavariate(self._numberofrewards_1[ad] +1,
                                            self._numberofrewards_0[ad]+1)
                #as per the thompsonsampling, we need to take the maximum of the beta dist and set the ad which needs to showup.
                if randombeta > max_random:
                    max_random = randombeta
                    self._selectedad = ad

            self._adsselected.append(self._selectedad)

            self._reward = self.data[sample,self._selectedad]

            if self._reward == 1:
                self._numberofrewards_1[self._selectedad] = self._numberofrewards_1[self._selectedad] + 1
            else:
                self._numberofrewards_0[self._selectedad] = self._numberofrewards_0[self._selectedad] + 1

            self._totalrewards = self._totalrewards + self._reward

            print(self._totalrewards)

        tsuccess=0
        tfail = 0
        for index in range(0,9):
            tsuccess += self._numberofrewards_1[index]
            tfail+=self._numberofrewards_0[index]

        print("Total of {} records, {} success, {} fails.".format(self._samples,
                                                                    tsuccess,
                                                                      tfail))




if __name__=='__main__':
    suggest = BannerSuggestClassification()
    suggest.loadnormalizetestdata()
    suggest.classify()