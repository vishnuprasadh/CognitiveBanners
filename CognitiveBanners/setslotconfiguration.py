import pandas as pd
from pandas import DataFrame
from CognitiveBanners.bannermodel import BannerModel
import os

class SetSlotConfiguration:

    def __init__(self):
        self._df = pd.read_csv(os.path.join("../resources","slotconfig.csv"),sep=",",header=0)


    def loadslotimages(self):
        if type(self._df) == DataFrame:
            slotsetup = BannerModel()
            results = slotsetup.setSlotBanners(self._df)
            if results != -1:
                print("Records successfully set!")
            else:
                print("Some issue in parsing values of records, please check the same")

    def returnslotimages(self):
        return self._df

if __name__ == '__main__':
    slots = SetSlotConfiguration()
    slots.loadslotimages()
    print(slots.returnslotimages().head())
