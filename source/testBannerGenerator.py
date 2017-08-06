import random
from source.setslotconfiguration import SetSlotConfiguration
from source.bannercontext import BannerContext
from source.bannermodel import BannerModel
import source.utils as utils
import datetime
import csv

import numpy as np


class TestBannerGenerator:

    _imagekey=list()
    _locations = {'Bangalore': 0.06,
                    'Mumbai':0.1,
                  'Pune':0.03
                  }

    _banners = list()

    _coldstart=False

    def _initalizecustomer(self,customercount=1000):
        '''

        :return:
        '''
        random.seed(random.randrange(2,10))
        with open('../resources/clickdata.csv', mode='w') as wfile:
            writer = csv.writer(wfile, delimiter=',')
            loclist = list(self._locations.keys())
            mumbai =0
            bangalore =0
            pune = 0
            falsemum=0
            truemum=0
            falseblr=0
            trueblr=0
            falsepun=0
            truepun=0
            for customer in range(1,customercount+1):
                location = random.choice(loclist)
                banner = BannerContext('hero',location,
                                       random.choice(self._imagekey),
                                       utils.currentimeInFormat(),
                                       customer,np.random.rand() < self._locations[location])
                if location == 'Mumbai':
                    mumbai +=1
                    if not banner.getBannerClicked:
                        falsemum+=1
                    else:
                        truemum+=1
                elif location == 'Bangalore':
                    bangalore+=1
                    if not banner.getBannerClicked:
                        falseblr += 1
                    else:
                        trueblr += 1
                else:
                    pune+=1
                    if not banner.getBannerClicked:
                        falsepun += 1
                    else:
                        truepun += 1

                self._banners.append(banner)
                writer.writerow([banner.getPlatform,banner.getSlot,banner.getCustomerID,
                                 banner.getBannerID,banner.getLocation,banner.getBannerClicked,
                                 banner.getOperationTime])

            #Insert the records into cassandra
            if self._coldstart:
                result = self._model.saveBanners(self._banners)

            if result <=0 :
                print("DB update failed!")
            else:
                print("DB update successful")


            print("Cust:{}, Loc:{}, Clicked:{},imagekey:{}".format(customer,location,banner.getBannerClicked,banner.getBannerID))

            print("Overall Mumbai:{}-{}-{}, Bangalore:{}-{}-{}, Pune:{}-{}-{}".format(mumbai,truemum,falsemum,
                                                                                          bangalore,trueblr,falseblr,
                                                                                          pune,truepun,falsepun))

            print("Total clicks - {}".format(truepun+truemum+trueblr))


    def generateSampleData(self,customercount=1000,coldstart=False):
        '''
        We will get the slot configuration for the given day
        :return:
        '''
        self._coldstart = coldstart
        self._model = BannerModel()
        slots = self._model.getSlotBanners('ajio','hero',utils.currentimeInFormat())
        for slot in slots:
            self._imagekey.append(slot[4])

        self._initalizecustomer(customercount)


if __name__ == '__main__':
    testbanner = TestBannerGenerator()
    testbanner.generateSampleData(1000,True)