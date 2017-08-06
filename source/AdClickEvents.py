from flask import Flask,Request,render_template,url_for,request
#from flask_restful import Resource,Api,reqparse
from source.bannermodel import BannerModel
from source.bannercontext import BannerContext
import source.utils as utils
from pyspark.context import SparkContext,SparkConf
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import  pandas as pd
import random
import json


app = Flask(__name__)
#api = Api(app)
#parser = reqparse.RequestParser()

@app.route('/adclick/',methods=['POST'])
def postAds():
    if Request.args:
        arguments = Request.args
        banner = BannerContext(arguments["slot"],
                               arguments["location"],
                               arguments["bannerid"],
                               utils.currentimeInFormat(),
                           arguments["customerid"],
                           arguments["clicked"],
                           arguments["referral"],
                           arguments["platform"])

@app.route('/adclick/',methods=['GET'])
@app.route('/adclick/<string:platform>',methods=['GET'])
@app.route('/adclick/<string:platform>/<string:slot>',methods=['GET'])
@app.route('/adclick/<string:platform>/<string:slot>/<string:location>',methods=['GET'])
@app.route('/adclick/<string:platform>/<string:slot>/<string:location>/<string:pastmin>',methods=['GET'])
def getAds(platform='ajio',slot='hero',location='bangalore',pastmin=720):
    bmodel  = BannerModel()
    images = bmodel.getSlotBanners(platform, slot, utils.currentimeInFormat())
    rowresult = bmodel.getBanners(platform,slot,pastmin)

    json_data = json.dumps({})

    if rowresult:
        #Initialize Spark context
        SparkConf.setMaster = "local[2]"
        SparkConf.setAppName = "banners"
        sc = SparkContext.getOrCreate()
        rows = rowresult.current_rows
        rdd = sc.parallelize(rows)
        #filter by location
        keys = rdd.filter(lambda X: "Bangalore" in X[0])
        #collect the filtered values to list.
        values = keys.collect()
        #get a dataframe
        adclicks = pd.DataFrame(values)

        adname = _normalizeandReturnAd(adclicks,images=images)

        json_data = {"key": adname[1], "value": "{0}.png".format(adname[1])}

    else:
        json_data = {"key" :"", "errorcode":"401", "errordesc":"No object found!"}

    return json.dumps(json_data)


def _normalizeandReturnAd(df,images):
    #get count of dataframe
    samples = len(df)
    data = df.iloc[:, [1, 2]].values
    labelencodeImage = LabelEncoder()
    labelencodecity = LabelEncoder()
    data[:, 0] = labelencodeImage.fit_transform(data[:, 0])
    #data[:, 1] = labelencodecity.fit_transform(data[:, 1])

    onehotencoderimage = OneHotEncoder(categorical_features=[0])
    data = onehotencoderimage.fit_transform(data).toarray()


    #Initialize the images
    adimages=[]
    for slot in images:
        adimages.append(slot[4])

    # Depending on number of images for the slot we will initialize
    numberofrewards_1 = [0] * len(adimages)
    numberofrewards_0 = [0] * len(adimages)


    #now based on variate analysis return the ads.
    for sample in range(0, samples):
        selectedad = 0
        # this is required as we take the max random draw from each ads
        max_random = 0

        # for each ad image, calculate the randombeta
        for ad in range(0, len(adimages)):
            randombeta = random.betavariate(numberofrewards_1[ad] + 1,
                                            numberofrewards_0[ad] + 1)
            # as per the thompsonsampling, we need to take the maximum of the beta dist and set the ad which needs to showup.
            if randombeta > max_random:
                max_random = randombeta
                selectedad = ad

    return selectedad, adimages[selectedad]


if __name__=='__main__':
    app.run(host="127.0.0.1", port=int(5002),debug=True)