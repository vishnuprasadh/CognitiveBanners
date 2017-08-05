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
    _locations = {'Bangalore': 0.2,
                    'Mumbai':0.3,
                  'Pune':0.4
                  }

    _banners = list()

    def _initalizecustomer(self):
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
            for customer in range(1,1001):
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
            print("Cust:{}, Loc:{}, Clicked:{},imagekey:{}".format(customer,location,banner.getBannerClicked,banner.getBannerID))

            print("Overall Mumbai:{}-{}-{}, Bangalore:{}-{}-{}, Pune:{}-{}-{}".format(mumbai,truemum,falsemum,
                                                                                          bangalore,trueblr,falseblr,
                                                                                          pune,truepun,falsepun))


    def generateSampleData(self):
        #slotimages = SetSlotConfiguration()
        #df = slotimages.returnslotimages()
        model = BannerModel()
        slots = model.getSlotBanners('ajio','hero',"05-Aug-17 00:00:00")

        for slot in slots:
            self._imagekey.append(slot[4])

        self._initalizecustomer()


if __name__ == '__main__':
    testbanner = TestBannerGenerator()
    testbanner.generateSampleData()