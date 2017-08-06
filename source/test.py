from cassandra.util import uuid_from_time
from cassandra.util import datetime_from_uuid1
from cassandra.util import datetime_from_timestamp
from datetime import datetime
from cassandra.cqltypes import UUID
from cassandra.cqltypes import BooleanType
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.connection import Connection
from cassandra.auth import PlainTextAuthProvider
import time
import datetime

from source.bannermodel import BannerModel
from source.bannercontext import BannerContext
import source.utils as utils
import pandas as pd

from pyspark.context import SparkContext,SparkConf

'''
b = BooleanType
b = 'true'
print(b)
time =  time.time()
print(time)
time = time + 18000
uuid = uuid_from_time(time)
print(uuid)
print(datetime_from_uuid1(uuid))
'''

import numpy as np

'''
#import random
true =0
false = 0
for index in range(1,10000):
    value = np.random.rand() < 0.35

    if value==True:
        true+=1
    else:
        false+=1

print("True - {}; False - {}".format(true,false))

    #print(random.getrandbits(1))
'''
'''
import random
_locations = {'Bangalore': 0.4,
              'Mumbai': 0.3,
              'Pune': 0.6
              }


for i in range(0,10):
    print(random.choice (list(_locations.keys())))
'''
'''

# load the recs and send the right value through spark


SparkConf.setMaster = "local[2]"
SparkConf.setAppName = "banners"
sc = SparkContext.getOrCreate()
bmodel = BannerModel()
rowresult = bmodel.getBanners("ajio", "hero", 720)



if rowresult:
    try:
        columns = rowresult.column_names
        rows = rowresult.current_rows
        rdd = sc.parallelize(rows)
        keys = rdd.filter(lambda X: "Bangalore" in X[0])
        values = keys.collect()
        df = pd.DataFrame(values)
        print(df.head())

    except Exception as ex:
        print(ex)
'''

import json
json_data= {"key" : "8"}
print(json.dumps(json_data))


